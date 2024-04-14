# Admin.py
class Admin:
    def __init__(self, conn):
        self.conn = conn

    def manage_room_booking(self, room_name, booking_time):
        """Add or update room booking."""
        with self.conn.cursor() as curs:
            curs.execute("""
                INSERT INTO RoomBookings (RoomName, BookingTime)
                VALUES (%s, %s)
                ON CONFLICT (RoomName, BookingTime) DO UPDATE SET
                BookingTime = EXCLUDED.BookingTime
            """, (room_name, booking_time))
            self.conn.commit()
            print("Room booking managed successfully")

    def update_room_booking(self, booking_id, new_room_name, new_booking_time):
        with self.conn.cursor() as curs:
            curs.execute("""
                UPDATE RoomBookings
                SET RoomName = %s, BookingTime = %s
                WHERE BookingID = %s
            """, (new_room_name, new_booking_time, booking_id))
            self.conn.commit()
            print("Booking updated successfully.")


    def monitor_equipment_maintenance(self):
        """Check the equipment maintenance schedule for any entries set to 'NOW'."""
        with self.conn.cursor() as curs:
            curs.execute("SELECT EquipmentID, Name, MaintenanceSchedule FROM Equipment WHERE MaintenanceSchedule = 'NOW'")
            equipment_needs = curs.fetchall()
            if equipment_needs:
                print("Equipment needing immediate maintenance:")
                for equipment in equipment_needs:
                    print(f"Equipment ID: {equipment[0]}, Name: {equipment[1]}, Scheduled Maintenance: {equipment[2]}")
            else:
                print("No immediate maintenance needed.")


    def update_class_schedule(self, class_id, new_schedule):
        """Update the schedule of a class."""
        with self.conn.cursor() as curs:
            curs.execute("""
                UPDATE ClassSchedule SET StartTime = %s, EndTime = %s
                WHERE ClassID = %s
            """, (new_schedule['start_time'], new_schedule['end_time'], class_id))
            self.conn.commit()
            print("Class schedule updated successfully")

    def process_billing(self, member_id, amount_due=None, due_date=None):
        """Updates or creates a billing record for a member. Deletes if amount_due is None."""
        with self.conn.cursor() as curs:
            if amount_due is not None:
                # Check if the billing record exists
                curs.execute("SELECT BillingID FROM Billing WHERE MemberID = %s", (member_id,))
                if curs.fetchone():
                    # Update existing billing record
                    curs.execute("""
                        UPDATE Billing
                        SET AmountDue = %s, DueDate = %s
                        WHERE MemberID = %s
                    """, (amount_due, due_date, member_id))
                else:
                    # Create a new billing record
                    curs.execute("""
                        INSERT INTO Billing (MemberID, AmountDue, DueDate)
                        VALUES (%s, %s, %s)
                    """, (member_id, amount_due, due_date))
                print("Billing processed successfully.")
            else:
                # Remove billing record if no amount is given
                curs.execute("DELETE FROM Billing WHERE MemberID = %s", (member_id,))
                print("Billing record removed successfully.")
            self.conn.commit()


    def print_billing(self):
        """Prints all members with outstanding bills."""
        with self.conn.cursor() as curs:
            curs.execute("""
                SELECT Members.FirstName, Members.LastName, Billing.MemberID, Billing.AmountDue, Billing.DueDate
                FROM Billing
                INNER JOIN Members ON Billing.MemberID = Members.MemberID
                WHERE Billing.AmountDue > 0
                ORDER BY Billing.DueDate ASC
            """)
            bills = curs.fetchall()
            if bills:
                print("Outstanding Bills:")
                for bill in bills:
                    print(f"Member ID: {bill[2]}, Name: {bill[0]} {bill[1]}, Amount Due: ${bill[3]:.2f}, Due Date: {bill[4]}")
            else:
                print("No outstanding bills found.")

