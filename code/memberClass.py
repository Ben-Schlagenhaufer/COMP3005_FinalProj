# Member.py

class Member:
    def __init__(self, conn, first_name, last_name, email, password, fitness_goals='', health_metrics=''):
        self.conn = conn
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # Storing password directly without hashing
        self.fitness_goals = fitness_goals
        self.health_metrics = health_metrics

    def refresh_connection(self, new_conn):
        """Updates the database connection for this member."""
        self.conn = new_conn


    def register(self):
        """Registers a new member into the database."""
        with self.conn.cursor() as curs:
            curs.execute("""
                INSERT INTO Members (FirstName, LastName, Email, Password, FitnessGoals, HealthMetrics)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (self.first_name, self.last_name, self.email, self.password, self.fitness_goals, self.health_metrics))
            self.conn.commit()
            print("Member registered successfully")

    def update_profile(self, updated_info):
        """Updates member's profile information based on a dictionary of new values."""
        with self.conn.cursor() as curs:
            for key, value in updated_info.items():
                curs.execute("UPDATE Members SET {} = %s WHERE Email = %s".format(key), (value, self.email))
            self.conn.commit()
            print("Profile updated successfully")

    def view_dashboard(self):
        """Fetches and displays member dashboard information in a simulated columnar table format."""
        with self.conn.cursor() as curs:
            curs.execute("""
                SELECT FirstName, LastName, Email FROM Members WHERE Email = %s
            """, (self.email,))
            member_info = curs.fetchone()

            if not member_info:
                print("Member not found.")
                return
            
            # Define categories
            categories = ["Exercise Routines", "Fitness Achievements", "Health Statistics"]
            dashboard_data = {category: [] for category in categories}
            
            # Fetch entries by category
            for category in categories:
                curs.execute("""
                    SELECT Description FROM MemberDashboard
                    WHERE MemberID = (SELECT MemberID FROM Members WHERE Email = %s)
                    AND Type = %s
                """, (self.email, category))
                dashboard_data[category] = [desc[0] for desc in curs.fetchall()]

            # Find the maximum number of entries in any category
            max_entries = max(len(entries) for entries in dashboard_data.values())
            
            # Print column headers
            for category in categories:
                print(f"{category}".center(30), end="")
            print("\n" + "=" * 90)

            # Print the entries for each category in 'columns'
            for i in range(max_entries):
                for category in categories:
                    entry = dashboard_data[category][i] if i < len(dashboard_data[category]) else ""
                    print(f"{entry}".center(30), end="")
                print()  # Newline after each 'row'

            print("=" * 90)




    def schedule_session(self, session_time, class_id):
        """Schedules a session for the member."""
        if self.check_trainer_availability(self.conn, session_time, class_id):
            with self.conn.cursor() as curs:
                curs.execute("""
                    INSERT INTO MemberSchedule (MemberID, ClassID, BookingTime)
                    SELECT MemberID, %s, %s FROM Members WHERE Email = %s
                """, (class_id, session_time, self.email))
                self.conn.commit()
                print("Session scheduled successfully")
        else:
            print("Trainer is not available at the chosen time.")

    @staticmethod
    def check_trainer_availability(conn, session_time, class_id):
        """Checks if the trainer is available at the given time."""
        with conn.cursor() as curs:
            curs.execute("SELECT * FROM ClassSchedule WHERE ClassID = %s AND StartTime <= %s AND EndTime >= %s",
                         (class_id, session_time, session_time))
            return curs.fetchone() is not None
        
    def pay_bill(self):
        """Pays off the member's entire bill and removes the bill record from the database."""
        with self.conn.cursor() as curs:
            # Fetch the current bill amount and its ID
            curs.execute("""
                SELECT BillingID, AmountDue FROM Billing 
                WHERE MemberID = (SELECT MemberID FROM Members WHERE Email = %s)
            """, (self.email,))
            bill_info = curs.fetchone()

            if bill_info:
                billing_id, amount_due = bill_info
                print(f"Total amount due: ${amount_due:.2f}")

                # Confirm full payment
                confirmation = input(f"Are you sure you want to pay the full amount? [y/n]: ").lower()
                if confirmation == 'y':
                    # Delete the bill record since it's paid off
                    curs.execute("DELETE FROM Billing WHERE BillingID = %s", (billing_id,))
                    self.conn.commit()
                    print("Bill paid in full and deleted successfully.")
                else:
                    print("Payment cancelled.")
            else:
                print("No outstanding bill found.")



    def get_dashboard_info(self):
        """Fetches the member's dashboard information."""
        with self.conn.cursor() as curs:
            curs.execute("""
                SELECT ExerciseRoutines, FitnessAchievements, HealthStatistics
                FROM MemberDashboard
                WHERE MemberID = (SELECT MemberID FROM Members WHERE Email = %s)
            """, (self.email,))
            return curs.fetchone()

# The actual connection and its creation are managed outside this file.
