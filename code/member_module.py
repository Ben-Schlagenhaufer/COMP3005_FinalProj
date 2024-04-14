# member_module.py

import os
from memberClass import Member

def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def member_menu(member):
    while True:
        clear_screen()  # Clears the console screen each time the menu is shown
        print(f"Welcome, {member.first_name}!\n")
        print("================================ MENU ====================================\n")
        print("1. View Dashboard                   2. Update Profile")
        print("3. View Schedule                    4. Pay Bill")
        print("\n6. Logout")
        print("\n=========================================================================")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            dashboard_menu(member)
        elif choice == '2':
            update_profile(member)
        elif choice == '3':
            class_schedule_handler(member)
        elif choice == '4':
            pay_bill(member)
        elif choice == '6':
            print("Exiting menu...")
            break  # Exit the while loop
        else:
            print("Invalid choice. Please select a valid option.")

        input("Press Enter to continue...")  # Pause before clearing the screen again

def print_user_schedule(member):
    print("Fetching your current schedule...")
    if not hasattr(member, 'conn') or not member.conn:
        print("Database connection is not properly set up.")
        return

    try:
        with member.conn.cursor() as curs:
            curs.execute("""
                SELECT cs.ClassName, ms.BookingTime, cs.StartTime, cs.EndTime
                FROM MemberSchedule ms
                JOIN ClassSchedule cs ON ms.ClassID = cs.ClassID
                JOIN Members m ON ms.MemberID = m.MemberID
                WHERE m.Email = %s
                ORDER BY cs.StartTime
            """, (member.email,))
            schedule = curs.fetchall()

            if schedule:
                headers = ["Class", "Booking Time", "Starts", "Ends"]
                col_widths = [max(len(str(entry[i])) for entry in schedule) for i in range(len(headers))]
                header_row = " | ".join(header.ljust(width) for header, width in zip(headers, col_widths))
                print(header_row)
                print("-" * len(header_row))

                for entry in schedule:
                    row = " | ".join(str(item).ljust(width) for item, width in zip(entry, col_widths))
                    print(row)

            else:
                print("You have no classes scheduled.")
    except Exception as e:
        print(f"An error occurred: {e}")


def edit_dashboard(member):
    print("Edit your dashboard. Choose an option:")
    print("1. Clear Specific Dashboard Items")
    print("2. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        clear_dashboard_items(member)
    elif choice == '2':
        print("Exiting dashboard editor.")
    else:
        print("Invalid option selected.")

def clear_dashboard_items(member):
    clear_screen()
    member.view_dashboard()  # Display current dashboard
    print("Clear specific items from your dashboard:")
    print("1. Exercise Routines")
    print("2. Fitness Achievements")
    print("3. Health Statistics")
    print("4. Exit")

    option = input("Enter the item number to clear: ")
    category_dict = {
        '1': 'Exercise Routines',
        '2': 'Fitness Achievements',
        '3': 'Health Statistics'
    }

    if option == '4':
        return
    elif option in category_dict:
        category_to_clear = category_dict[option]
        with member.conn.cursor() as curs:
            curs.execute("""
                DELETE FROM MemberDashboard
                WHERE MemberID = (SELECT MemberID FROM Members WHERE Email = %s) AND Type = %s
            """, (member.email, category_to_clear))
            member.conn.commit()
            print(f"All entries for {category_to_clear} cleared successfully.")
    else:
        print("Invalid option selected.")

def add_to_dashboard(member):
    print("================================ Add to Dashboard ===============================\n")
    exercise_routines = input("Enter Exercise Routines (press Enter to skip): ")
    fitness_achievements = input("Enter Fitness Achievements (press Enter to skip): ")
    health_statistics = input("Enter Health Statistics (press Enter to skip): ")

    with member.conn.cursor() as curs:
        # Insert new entries to the dashboard
        if exercise_routines:
            curs.execute("""
                INSERT INTO MemberDashboard (MemberID, Type, Description)
                VALUES ((SELECT MemberID FROM Members WHERE Email = %s), 'Exercise Routines', %s)
            """, (member.email, exercise_routines))
            print("New Exercise Routines added successfully.")

        if fitness_achievements:
            curs.execute("""
                INSERT INTO MemberDashboard (MemberID, Type, Description)
                VALUES ((SELECT MemberID FROM Members WHERE Email = %s), 'Fitness Achievements', %s)
            """, (member.email, fitness_achievements))
            print("New Fitness Achievements added successfully.")

        if health_statistics:
            curs.execute("""
                INSERT INTO MemberDashboard (MemberID, Type, Description)
                VALUES ((SELECT MemberID FROM Members WHERE Email = %s), 'Health Statistics', %s)
            """, (member.email, health_statistics))
            print("New Health Statistics added successfully.")

        member.conn.commit()

def dashboard_menu(member):
    while True:
        
        clear_screen()
        member.view_dashboard()
        print("\n============================= Member Management =============================\n")
        print("1. Edit Dashboard                 1. Add to Dashboard")
        print("\n3. Back to Main Menu")
        print("\n================================================================================")
        choice = input("\nEnter Option: ")

        if choice == '1':
            clear_screen()
            member.view_dashboard()
            edit_dashboard(member)
            continue
        elif choice == '2':
            clear_screen()
            member.view_dashboard()
            add_to_dashboard(member)
            continue
        elif choice == '3':
            clear_screen()
            break
        else:
            print("Invalid choice. Please select a valid option.")
            input("Press Enter to continue...")  # Pause before clearing the screen



def add_class_to_member_schedule(member):
    # Display available classes
    print("Fetching available class sessions...")
    with member.conn.cursor() as curs:
        curs.execute("""
            SELECT ClassID, ClassName, StartTime, EndTime
            FROM ClassSchedule
            ORDER BY StartTime
        """)
        classes = curs.fetchall()
        if not classes:
            print("No available class sessions to display.")
            return
        
        print("Available Classes:")
        for cls in classes:
            print(f"Class ID: {cls[0]}, Name: {cls[1]}, Starts: {cls[2]}, Ends: {cls[3]}")
        
        # Ask the member to choose a class to add to their schedule
        class_id = input("Enter the Class ID to add to your schedule: ")
        try:
            class_id = int(class_id)  # Convert input to integer
            # Insert the class into the MemberSchedule
            curs.execute("""
                INSERT INTO MemberSchedule (MemberID, ClassID, BookingTime)
                VALUES ((SELECT MemberID FROM Members WHERE Email = %s), %s, NOW())
            """, (member.email, class_id))
            member.conn.commit()
            print("Class added to your schedule successfully.")
        except ValueError:
            print("Invalid input. Please enter a numeric Class ID.")
        except Exception as e:
            member.conn.rollback()  # Rollback the transaction if an error occurs
            print(f"An error occurred while adding the class to your schedule: {e}")



def pay_bill(member):
    """Interface for members to pay their bill, showing amount due and allowing partial payments."""
    try:
        member.pay_bill()
    except Exception as e:
        print("An error occurred while processing the payment:", str(e))
    finally:
        input("Press Enter to continue...")

def register_member(conn):
    clear_screen()
    print("========================== SIGN UP ==============================\n")
    print("Please provide your details to register.\n")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    while True:
        email = input("Email: ")
        # Check if the email already exists in the database
        with conn.cursor() as curs:
            curs.execute("SELECT Email FROM Members WHERE Email = %s", (email,))
            if curs.fetchone():
                print("An account with this email already exists. Please use a different email.")
                continue  # Prompt for another email input
            else:
                break  # Exit the loop when a unique email is entered
            
    password = input("Password: ")
    fitness_goals = input("Fitness Goals (optional): ")
    health_metrics = input("Health Metrics (optional): ")

    # Instantiate the Member class now that we have a unique email
    new_member = Member(conn, first_name, last_name, email, password, fitness_goals, health_metrics)
    try:
        new_member.register()  # This method adds the member to the database
        print("\nRegistration successful. Please proceed to login.")
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"Failed to register due to an error: {e}")

def remove_from_schedule(member):
    clear_screen()
    print("Fetching your booked class sessions...")
    with member.conn.cursor() as curs:
        curs.execute("""
            SELECT ms.ScheduleID, cs.ClassID, cs.ClassName, cs.StartTime, cs.EndTime
            FROM MemberSchedule ms
            JOIN ClassSchedule cs ON ms.ClassID = cs.ClassID
            WHERE ms.MemberID = (SELECT MemberID FROM Members WHERE Email = %s)
            ORDER BY cs.StartTime
        """, (member.email,))
        booked_sessions = curs.fetchall()
        
        if not booked_sessions:
            print("You have no booked class sessions.")
            return
        
        # Print booked sessions with ClassID for easier identification
        print("Your Booked Class Sessions:")
        for session in booked_sessions:
            print(f"Booking ID: {session[0]}, Class ID: {session[1]}, Class: {session[2]}, Starts: {session[3]}, Ends: {session[4]}")

        # Ask the user which session they'd like to remove
        schedule_id = input("Enter the Booking ID of the session you want to remove: ")

        try:
            schedule_id = int(schedule_id)  # Convert input to integer
            # Check if the session ID is part of the booked sessions
            if any(session[0] == schedule_id for session in booked_sessions):
                # Delete the booking from MemberSchedule
                curs.execute("DELETE FROM MemberSchedule WHERE ScheduleID = %s", (schedule_id,))
                member.conn.commit()
                print("Class session removed successfully.")
            else:
                print("Invalid Booking ID. Please enter a valid selection.")
        except ValueError:
            print("Invalid input. Please enter a numeric Booking ID.")


def class_schedule_handler(member):
    while True:
        clear_screen()
        print_user_schedule(member)
        print("\n========================== Class Schedule Management =========================\n")
        print("1. Add Class Schedule          2. Remove Class Schedule")
        print("\n4. Back to Main Menu")
        print("\n================================================================================")
        choice = input("\nEnter Option: ")

       
        if choice == '2':
            remove_from_schedule(member)    
            continue
        elif choice == '1':
            add_class_to_member_schedule(member)
            continue
        elif choice == '4':
            clear_screen()
            break
        else:
            print("Invalid choice. Please select a valid option.")
            input("Press Enter to continue...")  # Pause before clearing the screen

def update_profile(member):
    updated_info = {}
    print("Enter new details (leave blank to skip):")
    for field in ['FirstName', 'LastName', 'Email', 'Password', 'FitnessGoals', 'HealthMetrics']:
        new_value = input(f"New {field}: ")
        if new_value:
            updated_info[field.lower()] = new_value
    if updated_info:
        member.update_profile(updated_info)