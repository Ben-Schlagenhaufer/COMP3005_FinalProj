class Trainer:
    def __init__(self, conn, first_name, last_name, email, expertise):
        self.conn = conn
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.expertise = expertise  # Simple string representing trainer's expertise

    def refresh_connection(self, new_conn):
        """Updates the database connection for this member."""
        self.conn = new_conn


    def add_to_database(self):
        """Adds a new trainer to the database."""
        with self.conn.cursor() as curs:
            curs.execute("""
                INSERT INTO Trainers (FirstName, LastName, Email, Expertise)
                VALUES (%s, %s, %s, %s)
            """, (self.first_name, self.last_name, self.email, self.expertise))
            self.conn.commit()
            print("Trainer added successfully")


    def get_profile(self):
        """Fetches and returns the trainer's profile information."""
        with self.conn.cursor() as curs:
            curs.execute("SELECT TrainerID, FirstName, LastName, Email, Expertise FROM Trainers WHERE Email = %s", (self.email,))
            profile = curs.fetchone()
            if profile:
                # Create a dictionary with profile details for ease of access
                profile_info = {
                    'TrainerID': profile[0],
                    'FirstName': profile[1],
                    'LastName': profile[2],
                    'Email': profile[3],
                    'Expertise': profile[4]
                }
                return profile_info
            else:
                return None
            
    def print_schedule(self):
        """Prints the trainer's schedule."""
        with self.conn.cursor() as curs:
            curs.execute("""
                SELECT ScheduleID, StartTime, EndTime 
                FROM TrainerSchedule 
                WHERE TrainerID = (SELECT TrainerID FROM Trainers WHERE Email = %s)
                ORDER BY StartTime
            """, (self.email,))
            schedule = curs.fetchall()
            if schedule:
                headers = ["ID", "Start Time", "End Time"]
                col_widths = [max(len(str(entry[i])) for entry in schedule) for i in range(len(headers))]
                header_row = " | ".join(header.ljust(width) for header, width in zip(headers, col_widths))
                print(header_row)
                print("-" * len(header_row))

                for entry in schedule:
                    row = " | ".join(str(item).ljust(width) for item, width in zip(entry, col_widths))
                    print(row)
            else:
                print("No schedule found.")

    def remove_schedule(self, schedule_id):
        """Removes a specified schedule entry based on ScheduleID."""
        with self.conn.cursor() as curs:
            curs.execute("""
                DELETE FROM TrainerSchedule
                WHERE ScheduleID = %s AND TrainerID = (SELECT TrainerID FROM Trainers WHERE Email = %s)
            """, (schedule_id, self.email))
            self.conn.commit()
            if curs.rowcount > 0:
                print(f"Schedule ID {schedule_id} removed successfully.")
            else:
                print(f"Schedule ID {schedule_id} not found or could not be removed.")

    def set_available_times(self, available_times):
        """Sets available times for this trainer."""
        with self.conn.cursor() as curs:
            # Ensure we have the trainer's ID
            curs.execute("SELECT TrainerID FROM Trainers WHERE Email = %s", (self.email,))
            trainer_id_result = curs.fetchone()
            if not trainer_id_result:
                print("Trainer not found.")
                return

            trainer_id = trainer_id_result[0]
            
            # Insert the new available times using TIMESTAMP
            for schedule in available_times:
                curs.execute("""
                    INSERT INTO TrainerSchedule (TrainerID, StartTime, EndTime)
                    VALUES (%s, %s, %s)
                """, (trainer_id, schedule['start_time'], schedule['end_time']))
            self.conn.commit()
            print("Available times set successfully.")

    def update_schedule(self, new_times):
        """Updates the trainer's available times."""
        with self.conn.cursor() as curs:
            # Ensure we have the trainer's ID
            curs.execute("SELECT TrainerID FROM Trainers WHERE Email = %s", (self.email,))
            trainer_id_result = curs.fetchone()
            if not trainer_id_result:
                print("Trainer not found.")
                return
            
            trainer_id = trainer_id_result[0]

            # Clear the existing schedule
            curs.execute("DELETE FROM TrainerSchedule WHERE TrainerID = %s", (trainer_id,))
            self.conn.commit()
            
            # Insert new available times using TIMESTAMP
            for schedule in new_times:
                curs.execute("""
                    INSERT INTO TrainerSchedule (TrainerID, StartTime, EndTime)
                    VALUES (%s, %s, %s)
                """, (trainer_id, schedule['start_time'], schedule['end_time']))
            self.conn.commit()
            print("Schedule updated successfully.")
