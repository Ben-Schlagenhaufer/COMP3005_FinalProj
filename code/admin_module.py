# admin_module.py

import os


def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def admin_menu(admin):

    while True:
        clear_screen()  # Clears the console screen each time the menu is shown
        print("Welcome Admin!\n")
        
        print("================================ MENU ====================================\n")
        print("1. Manage Room Booking              2. Monitor Equipment Maintenance")
        print("3. Update Class Schedule            4. Manage Members")
        print("5. Manage Trainers") 
        print("\n6. Logout")
        print("\n=========================================================================")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            clear_screen()
            manage_room_booking(admin)
        elif choice == '2':
            clear_screen()
            manage_equipment(admin) 
        elif choice == '3':
            clear_screen()
            update_class_schedule(admin)
        elif choice == '4':
            clear_screen()
            member_management_handler(admin)
        elif choice == '5':
            clear_screen()
            manage_trainers(admin)
        elif choice == '6':
            print("Exiting menu...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

        input("Press Enter to continue...")  # Pause before clearing the screen again

# ======================== Helper Print Functions ========================

def print_all_members(admin):
    with admin.conn.cursor() as curs:
        # Join Members with Billing to get the AmountDue and DueDate
        curs.execute("""
            SELECT m.MemberID, m.FirstName, m.LastName, m.Email, 
                   b.AmountDue, b.DueDate
            FROM Members m
            LEFT JOIN Billing b ON m.MemberID = b.MemberID
            ORDER BY m.LastName, m.FirstName;
        """)
        members = curs.fetchall()
        if members:
            # Define column headers
            headers = ["Member ID", "Name", "Email", "Amount Due", "Due Date"]
            # Determine the maximum width for each column
            col_widths = {
                "Member ID": max(len(str(member[0])) for member in members),
                "Name": max(len(f"{member[1]} {member[2]}") for member in members),
                "Email": max(len(member[3]) for member in members),
                "Amount Due": max(len(str(member[4])) if member[4] is not None else 0 for member in members),
                "Due Date": max(len(member[5].strftime('%Y-%m-%d') if member[5] is not None else '') for member in members)
            }
            # Set minimum column widths based on headers
            col_widths = {key: max(len(value), col_widths[key]) for key, value in zip(headers, headers)}
            # Adding extra space for padding
            col_paddings = 2

            # Calculate total width for the table
            total_width = sum(col_widths.values()) + len(col_widths)*3 + (col_paddings * 2 * len(col_widths)) + 1
            
            # Print the header of the table with padding
            print("=" * total_width)
            print("|", end=" ")
            for header in headers:
                print(f"{header.center(col_widths[header]+(col_paddings*2))}|", end=" ")
            print("\n" + "=" * total_width)
            
            # Print each member's details formatted to column width with padding
            for member in members:
                member_details = [
                    member[0], 
                    f"{member[1]} {member[2]}", 
                    member[3], 
                    f"${member[4]:,.2f}" if member[4] is not None else "N/A", 
                    member[5].strftime('%Y-%m-%d') if member[5] is not None else "N/A"
                ]
                print("|", end=" ")
                for index, detail in enumerate(member_details):
                    col_name = headers[index]
                    print(f"{str(detail).center(col_widths[col_name]+(col_paddings*2))}|", end=" ")
                print()
            print("=" * total_width)
        else:
            print("No members found.")

def print_all_trainers(admin):
    with admin.conn.cursor() as curs:
        curs.execute("SELECT * FROM Trainers")
        trainers = curs.fetchall()
        if trainers:
            # Define column headers
            headers = ["Trainer ID", "Name", "Email", "Expertise"]
            # Determine the maximum width for each column
            col_widths = {
                "Trainer ID": max(len(str(trainer[0])) for trainer in trainers),
                "Name": max(len(f"{trainer[1]} {trainer[2]}") for trainer in trainers),
                "Email": max(len(trainer[3]) for trainer in trainers),
                "Expertise": max(len(trainer[4]) for trainer in trainers)
            }
            # Set minimum column widths based on headers
            col_widths = {key: max(len(value), col_widths[key]) for key, value in zip(headers, headers)}
            # Adding extra space for padding
            col_paddings = 2
            
            # Calculate total width for the table
            total_width = sum(col_widths.values()) + len(col_widths)*3 + (col_paddings * 2 * len(col_widths)) + 1
            
            # Print the header of the table with padding
            print("=" * total_width)
            print("|", end=" ")
            for header in headers:
                print(f"{header.center(col_widths[header]+(col_paddings*2))}|", end=" ")
            print("\n" + "=" * total_width)
            
            # Print each trainer's details formatted to column width with padding
            for trainer in trainers:
                trainer_details = [trainer[0], f"{trainer[1]} {trainer[2]}", trainer[3], trainer[4]]
                print("|", end=" ")
                for index, detail in enumerate(trainer_details):
                    col_name = headers[index]
                    print(f"{str(detail).center(col_widths[col_name]+(col_paddings*2))}|", end=" ")
                print()
            print("=" * total_width)
        else:
            print("No trainers found.")

def print_room_bookings(cursor):
    cursor.execute("SELECT BookingID, RoomName, BookingTime FROM RoomBookings ORDER BY BookingTime")
    bookings = cursor.fetchall()
    if bookings:
        # Define column headers
        headers = ["Booking ID", "Room", "Time"]
        # Determine the maximum width for each column
        col_widths = {
            "Booking ID": max(len(str(booking[0])) for booking in bookings),
            "Room": max(len(booking[1]) for booking in bookings),
            "Time": max(len(booking[2].strftime('%Y-%m-%d %H:%M:%S')) for booking in bookings)
        }
        # Set minimum column widths based on headers
        col_widths = {key: max(len(value), col_widths[key]) for key, value in zip(headers, headers)}
        # Adding extra space for padding
        col_paddings = 2
        
        # Calculate total width for the table
        total_width = sum(col_widths.values()) + len(col_widths)*3 + (col_paddings * 2 * len(col_widths)) + 1
        
        # Print the header of the table with padding
        print("=" * total_width)
        print("|", end=" ")
        for header in headers:
            print(f"{header.center(col_widths[header]+(col_paddings*2))}|", end=" ")
        print("\n" + "=" * total_width)
        
        # Print each booking's details formatted to column width with padding
        for booking in bookings:
            booking_details = [booking[0], booking[1], booking[2].strftime('%Y-%m-%d %H:%M:%S')]
            print("|", end=" ")
            for index, detail in enumerate(booking_details):
                col_name = headers[index]
                print(f"{str(detail).center(col_widths[col_name]+(col_paddings*2))}|", end=" ")
            print()
        print("=" * total_width)
    else:
        print("No current bookings.")

def print_class_schedules(cursor):
    cursor.execute("""
        SELECT ClassID, ClassName, StartTime, EndTime, TrainerID
        FROM ClassSchedule
        ORDER BY StartTime
    """)
    schedules = cursor.fetchall()
    if schedules:
        # Define column headers
        headers = ["Class ID", "Class Name", "Start Time", "End Time", "Trainer ID"]
        # Determine the maximum width for each column
        col_widths = {
            "Class ID": max(len(str(schedule[0])) for schedule in schedules),
            "Class Name": max(len(schedule[1]) for schedule in schedules),
            "Start Time": max(len(schedule[2].strftime('%Y-%m-%d %H:%M:%S')) for schedule in schedules),
            "End Time": max(len(schedule[3].strftime('%Y-%m-%d %H:%M:%S')) for schedule in schedules),
            "Trainer ID": max(len(str(schedule[4])) for schedule in schedules)
        }
        # Set minimum column widths based on headers
        col_widths = {key: max(len(value), col_widths[key]) for key, value in zip(headers, headers)}
        # Adding extra space for padding
        col_paddings = 2

        # Calculate total width for the table
        total_width = sum(col_widths.values()) + len(col_widths)*3 + (col_paddings * 2 * len(col_widths)) + 1
        
        # Print the header of the table with padding
        print("=" * total_width)
        print("|", end=" ")
        for header in headers:
            print(f"{header.center(col_widths[header]+(col_paddings*2))}|", end=" ")
        print("\n" + "=" * total_width)
        
        # Print each class schedule's details formatted to column width with padding
        for schedule in schedules:
            schedule_details = [
                schedule[0], 
                schedule[1], 
                schedule[2].strftime('%Y-%m-%d %H:%M:%S'), 
                schedule[3].strftime('%Y-%m-%d %H:%M:%S'), 
                schedule[4]
            ]
            print("|", end=" ")
            for index, detail in enumerate(schedule_details):
                col_name = headers[index]
                print(f"{str(detail).center(col_widths[col_name]+(col_paddings*2))}|", end=" ")
            print()
        print("=" * total_width)
    else:
        print("No class schedules available to display.")

def print_class_info(admin, class_id):
    with admin.conn.cursor() as curs:
        # Fetch class name, schedule, and trainer details
        curs.execute("""
            SELECT cs.ClassName, t.FirstName, t.LastName, cs.StartTime, cs.EndTime
            FROM ClassSchedule cs
            JOIN Trainers t ON cs.TrainerID = t.TrainerID
            WHERE cs.ClassID = %s
        """, (class_id,))
        class_info = curs.fetchone()
        if not class_info:
            print("No class found with that ID.")
            return
        
        # Fetch list of enrolled members
        curs.execute("""
            SELECT m.MemberID, m.FirstName, m.LastName
            FROM MemberSchedule ms
            JOIN Members m ON ms.MemberID = m.MemberID
            WHERE ms.ClassID = %s
        """, (class_id,))
        members = curs.fetchall()

        # Print class information
        print(f"\nClass Name: {class_info[0]}")
        print(f"Trainer: {class_info[1]} {class_info[2]}")
        print(f"Class ID: {class_id}")
        print(f"Class Schedule: {class_info[3].strftime('%Y-%m-%d %H:%M:%S')} to {class_info[4].strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Print members table header
        print("\nEnrolled Members:")
        if members:
            # Calculate the width of the table based on member names
            name_width = max(len(f"{member[1]} {member[2]}") for member in members)
            line = "=" * (13 + name_width)  # Adjust the line length to match the table width
            print(line)
            print(f"| {'Member ID':<10} | {'Name':<{name_width}} |")
            print(line)
            for member in members:
                member_name = f"{member[1]} {member[2]}"
                print(f"| {member[0]:<10} | {member_name:<{name_width}} |")
            print(line)
        else:
            print("No members are currently enrolled in this class.")

def print_schdule_handler(admin,class_id):
    while True:
        print_class_info(admin, class_id)

        print("\n================================ MENU ====================================\n")
        print("1. Add Member                2. Remove Member")
        print("3. Change Trainer            4. Edit Class Time")
        print("5. Remove Class")
        print("\n6. Back to Main Menu")
        print("\n=========================================================================")
        choice = input("\nEnter Option: ")  

        
        if choice == '1':
            add_member_to_class(admin, class_id)
        elif choice == '2':
            delete_member_from_class(admin, class_id)
        elif choice == '3':
            clear_screen()
            change_trainer_for_class(admin, class_id)
        elif choice == '4':
            edit_class_time(admin, class_id)
        elif choice == '5':
            remove_class(admin, class_id)
        elif choice == '6':
            clear_screen()
            return
        else:
            print("Invalid choice. Please select a valid option.")
            input("Press Enter to continue...")  # Pause before clearing the screen

def member_management_handler(admin):
    while True:
        
        clear_screen()
        print_all_members(admin)
        print("\n============================= Member Management =============================\n")
        print("1. Add Member                 2. Remove Member")
        print("3. Bill Member")
        print("\n4. Back to Main Menu")
        print("\n================================================================================")
        choice = input("\nEnter Option: ")

        if choice == '1':
            add_member(admin)
            continue
        elif choice == '2':
            member_id = input("\nEnter the Member ID to remove: ")
            remove_member(admin, member_id)
            continue
        elif choice == '3':
            member_id = input("\nEnter the Member ID to bill: ")
            manage_billing(admin, member_id)
            continue
        elif choice == '4':
            clear_screen()
            break
        else:
            print("Invalid choice. Please select a valid option.")
            input("Press Enter to continue...")  # Pause before clearing the screen

def manage_trainers(admin):
    while True:
        clear_screen()
        print_all_trainers(admin)

        print("\n================================ Trainer Management ====================================\n")
        print("1. Add Trainer                2. Remove Trainer")
        print("\n3. Back to Main Menu")
        print("\n======================================================================================")
        choice = input("\nEnter Option: ")  

        if choice == '1':
            add_trainer(admin)
        elif choice == '2':
            trainer_id = input("Enter the Trainer ID to remove: ")
            remove_trainer(admin, trainer_id)
        elif choice == '3':
            clear_screen()
            return
        else:
            print("Invalid choice. Please select a valid option.")
        input("Press Enter to continue...")  # Pause before clearing the screen

def print_all_equipment(admin):
    with admin.conn.cursor() as curs:
        curs.execute("SELECT EquipmentID, Name, MaintenanceSchedule FROM Equipment ORDER BY EquipmentID")
        equipment = curs.fetchall()
        if equipment:
            print("\nList of All Equipment:\n")
            print("|{:<12}|{:<30}|{:<20}|".format("Equipment ID", "Name", "Maintenance Schedule"))
            print("-" * 64)
            for item in equipment:
                print("|{:<12}|{:<30}|{:<20}|".format(item[0], item[1], item[2]))
            print("-" * 64)
        else:
            print("No equipment found.")

def manage_equipment(admin):
    while True:
        clear_screen()
        print_all_equipment(admin)

        print("\n================================ Equipment Management =================================\n")
        print("1. Add Equipment                2. Remove Equipment")
        print("3. Change Maintenance Schedule")
        print("\n4. Back to Main Menu")
        print("\n======================================================================================")
        choice = input("\nEnter Option: ")

        if choice == '1':
            add_equipment(admin)
        elif choice == '2':
            delete_equipment(admin)
        elif choice == '3':
            change_equipment_maintenance(admin)
        elif choice == '4':
            clear_screen()
            return
        else:
            print("Invalid choice. Please select a valid option.")
        input("Press Enter to continue...")  # Pause before re-displaying the menu


# ======================== Helper for Admin Functions ========================

def add_member_to_class(admin, class_id):
    
    while True:
        clear_screen()
        print_all_members(admin)
        member_id = input("Enter the Member ID to enroll or 'q' to quit: ")
        
        # Allow the admin to quit the process
        if member_id.lower() == 'q':
            clear_screen()
            break
        
        with admin.conn.cursor() as curs:
            # Check if the member ID is valid
            curs.execute("SELECT MemberID FROM Members WHERE MemberID = %s", (member_id,))
            if not curs.fetchone():
                print("Invalid Member ID. Please try again.")
                input("\nPress Enter to continue...")
                continue

            # Check if the member is already enrolled in the class
            curs.execute("""
                SELECT 1 FROM MemberSchedule
                WHERE MemberID = %s AND ClassID = %s
            """, (member_id, class_id))
            if curs.fetchone():
                print("Member is already enrolled in this class.")
                input("\nPress Enter to continue...")
                return

            # Get the StartTime from the ClassSchedule for the given class_id
            curs.execute("SELECT StartTime FROM ClassSchedule WHERE ClassID = %s", (class_id,))
            start_time = curs.fetchone()

            if start_time:
                # Insert the new booking into MemberSchedule with the retrieved StartTime
                curs.execute("""
                    INSERT INTO MemberSchedule (MemberID, ClassID, BookingTime)
                    VALUES (%s, %s, %s)
                """, (member_id, class_id, start_time[0]))
                admin.conn.commit()
                print("Member added to class successfully.")
                input("\nPress Enter to continue...")
                clear_screen()
                return
            else:
                print("Class ID not found or has no start time.")
                input("\nPress Enter to continue...")  # Pause before clearing the screen
                return
    
def delete_member_from_class(admin, class_id):
    while True:
        clear_screen()
        print_all_members(admin)
        
        member_id = input("Enter the Member ID to unenroll or 'q' to quit: ")
        if member_id.lower() == 'q':
            clear_screen()
            break  

        with admin.conn.cursor() as curs:
            # Check if the member is actually enrolled in the class
            curs.execute("""
                SELECT 1 FROM MemberSchedule
                WHERE MemberID = %s AND ClassID = %s
            """, (member_id, class_id))
            if not curs.fetchone():
                print("Member is not enrolled in this class.")
                input("\nPress Enter to continue...")
                continue

            # Delete the booking from MemberSchedule
            curs.execute("""
                DELETE FROM MemberSchedule
                WHERE MemberID = %s AND ClassID = %s
            """, (member_id, class_id))
            admin.conn.commit()
            print("Member removed from class successfully.")
            input("\nPress Enter to continue...")
            clear_screen()
            break  

def change_trainer_for_class(admin, class_id):
    print("Available Trainers:")
    print_all_trainers(admin)
    
    new_trainer_id = input("Enter the Trainer ID to assign to the class: ")

    with admin.conn.cursor() as curs:
        try:
            # Update the trainer for the class
            curs.execute("""
                UPDATE ClassSchedule
                SET TrainerID = %s
                WHERE ClassID = %s
            """, (new_trainer_id, class_id))

            # Commit the changes
            admin.conn.commit()
            print(f"Trainer {new_trainer_id} has been assigned to class {class_id} successfully.")
        except Exception as e:
            admin.conn.rollback()  # Rollback the transaction if an error occurs
            print(f"An error occurred: {e}")
        finally:
            input("\nPress Enter to continue...")

def edit_class_time(admin, class_id):
    # Collect new times for updating
    start_time = input("Enter new start time (YYYY-MM-DD HH:MM:SS): ")
    end_time = input("Enter new end time (YYYY-MM-DD HH:MM:SS): ")
    # Update the class schedule in the database
    with admin.conn.cursor() as curs:
        curs.execute("""
            UPDATE ClassSchedule
            SET StartTime = %s, EndTime = %s
            WHERE ClassID = %s
        """, (start_time, end_time, class_id))
        admin.conn.commit()

def remove_class(admin, class_id):
    # Delete the class schedule from the database
    with admin.conn.cursor() as curs:
        curs.execute("DELETE FROM ClassSchedule WHERE ClassID = %s", (class_id,))
        curs.execute("DELETE FROM MemberSchedule WHERE ClassID = %s", (class_id,))
        admin.conn.commit()
        print("Class schedule and related member schedules deleted successfully.")
        input("\nPress Enter to continue...")  # Pause before clearing the screen

def add_member(admin):
    clear_screen()
    print("Add New Member:\n")
    first_name = input("Enter member's first name: ")
    last_name = input("Enter member's last name: ")
    email = input("Enter member's email: ")
    password = input("Enter member's password: ")  # This should be hashed in a production environment
    fitness_goals = input("Enter member's fitness goals (optional, can be left blank): ")
    health_metrics = input("Enter member's health metrics (optional, can be left blank): ")

    with admin.conn.cursor() as curs:
        # Add the new member to the database
        curs.execute("""
            INSERT INTO Members (FirstName, LastName, Email, Password, FitnessGoals, HealthMetrics)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, password, fitness_goals, health_metrics))
        admin.conn.commit()
        print("New member added successfully.")

def remove_trainer(admin, trainer_id):
    if trainer_id.lower() == 'q':
        return

    with admin.conn.cursor() as curs:
        try:
            # Start a transaction
            curs.execute("BEGIN;")

            # Check if the trainer exists
            curs.execute("SELECT TrainerID FROM Trainers WHERE TrainerID = %s", (trainer_id,))
            if not curs.fetchone():
                print("Trainer ID does not exist.")
                input("\nPress Enter to continue...")
                curs.execute("ROLLBACK;")
                return

            # Check if the trainer is assigned to any classes
            curs.execute("SELECT ClassID FROM ClassSchedule WHERE TrainerID = %s", (trainer_id,))
            if curs.fetchone():
                print("This trainer is currently assigned to classes.")
                # Prompt for reassignment
                if not reassign_classes_to_another_trainer(admin, trainer_id):
                    print("Classes must be reassigned before removing the trainer.")
                    input("\nPress Enter to continue...")
                    curs.execute("ROLLBACK;")
                    return

            # Delete the trainer from the database
            curs.execute("DELETE FROM Trainers WHERE TrainerID = %s", (trainer_id,))
            
            # Commit the transaction
            curs.execute("COMMIT;")
            print("Trainer removed successfully.")
        except Exception as e:
            curs.execute("ROLLBACK;")  # Rollback the transaction if an error occurs
            print("An error occurred while removing the trainer:", str(e))
        finally:
            input("\nPress Enter to continue...")

def remove_member(admin, member_id):
    if member_id.lower() == 'q':
        return

    try:
        with admin.conn.cursor() as curs:
            # Begin a transaction
            curs.execute("BEGIN;")

            # Check if the member exists
            curs.execute("SELECT MemberID FROM Members WHERE MemberID = %s", (member_id,))
            if not curs.fetchone():
                print("Member ID does not exist.")
                input("\nPress Enter to continue...")
                return

            # Delete references from MemberSchedule
            curs.execute("DELETE FROM MemberSchedule WHERE MemberID = %s", (member_id,))

            # If the member has any billing records, they should be deleted as well
            curs.execute("DELETE FROM Billing WHERE MemberID = %s", (member_id,))

            # Delete the member from the database
            curs.execute("DELETE FROM Members WHERE MemberID = %s", (member_id,))
            
            # Commit the transaction
            admin.conn.commit()
            print("Member removed successfully.")
    except Exception as e:
        admin.conn.rollback()  # Rollback the transaction if an error occurs
        print("An error occurred while removing the member:", str(e))
    finally:
        input("\nPress Enter to continue...")

def reassign_classes_to_another_trainer(admin, trainer_id):
    with admin.conn.cursor() as curs:
        # Find available trainers excluding the one to be deleted
        curs.execute("SELECT TrainerID FROM Trainers WHERE TrainerID != %s", (trainer_id,))
        available_trainers = curs.fetchall()
        
        if not available_trainers:
            print("No other trainers available to reassign classes to. Can't remove the only trainer.")
            return False
        
        # Allow admin to select which trainer to reassign classes to
        print("Available Trainers:")
        for trainer in available_trainers:
            print(f"Trainer ID: {trainer[0]}")
        new_trainer_id = input("Enter the ID of the trainer to reassign classes to: ")
        
        # Reassign the classes
        curs.execute("""
            UPDATE ClassSchedule
            SET TrainerID = %s
            WHERE TrainerID = %s
        """, (new_trainer_id, trainer_id))
        
        return True

def remove_trainer(admin, trainer_id):
    if trainer_id.lower() == 'q':
        return

    with admin.conn.cursor() as curs:
        try:
            # Check if the trainer exists
            curs.execute("SELECT TrainerID FROM Trainers WHERE TrainerID = %s", (trainer_id,))
            if not curs.fetchone():
                print("Trainer ID does not exist.")
                input("\nPress Enter to continue...")
                return

            # Check if the trainer is currently assigned to any classes
            curs.execute("SELECT ClassID FROM ClassSchedule WHERE TrainerID = %s", (trainer_id,))
            if curs.fetchone():
                print("Trainer cannot be removed because they are currently assigned to classes.")
                print("Please reassign or remove classes before deleting the trainer.")
                input("\nPress Enter to continue...")
                return

            # Delete the trainer from the database
            curs.execute("DELETE FROM Trainers WHERE TrainerID = %s", (trainer_id,))
            admin.conn.commit()  # Explicitly commit the changes
            print("Trainer removed successfully.")
        except Exception as e:
            admin.conn.rollback()  # Rollback any changes if an error occurs
            print("An error occurred while removing the trainer:", str(e))
        finally:
            input("\nPress Enter to continue...")

def add_trainer(admin):
    clear_screen()
    print("Add New Trainer:\n")
    first_name = input("Enter trainer's first name: ")
    last_name = input("Enter trainer's last name: ")
    email = input("Enter trainer's email: ")
    expertise = input("Enter trainer's expertise: ")

    with admin.conn.cursor() as curs:
        # Add the new trainer to the database
        curs.execute("""
            INSERT INTO Trainers (FirstName, LastName, Email, Expertise)
            VALUES (%s, %s, %s, %s)
        """, (first_name, last_name, email, expertise))
        admin.conn.commit()
        print("New trainer added successfully.")

def add_equipment(admin):
    clear_screen()
    print("Add New Equipment:\n")
    name = input("Enter equipment name: ")
    maintenance_schedule = input("Enter maintenance schedule (e.g., 'Every 6 months'): ")

    with admin.conn.cursor() as curs:
        curs.execute("""
            INSERT INTO Equipment (Name, MaintenanceSchedule)
            VALUES (%s, %s)
        """, (name, maintenance_schedule))
        admin.conn.commit()
        print("New equipment added successfully.")

def delete_equipment(admin):
    equipment_id = input("Enter the Equipment ID to remove: ")

    with admin.conn.cursor() as curs:
        curs.execute("DELETE FROM Equipment WHERE EquipmentID = %s", (equipment_id,))
        admin.conn.commit()
        print("Equipment removed successfully.")

def change_equipment_maintenance(admin):
    equipment_id = input("Enter the Equipment ID to update the maintenance schedule: ")
    new_schedule = input("Enter the new maintenance schedule (e.g., 'Every 12 months'): ")

    with admin.conn.cursor() as curs:
        curs.execute("""
            UPDATE Equipment
            SET MaintenanceSchedule = %s
            WHERE EquipmentID = %s
        """, (new_schedule, equipment_id))
        admin.conn.commit()
        print("Equipment maintenance schedule updated successfully.")

# ======================== Admin Functions ========================

def manage_room_booking(admin):
    print("Current Room Bookings:\n")
    with admin.conn.cursor() as curs:
        print_room_bookings(curs)  # Print room bookings in table format

    change = input("\nWould you like to change any booking? (yes/no): ")
    if change.lower() == 'yes':
        choose_booking_id = input("Enter the Booking ID to update: ")

        if not choose_booking_id.isdigit():
            print("Invalid Booking ID. Please enter a valid Booking ID.")
            return

        with admin.conn.cursor() as curs:
            curs.execute("SELECT RoomName, BookingTime FROM RoomBookings WHERE BookingID = %s", (choose_booking_id,))
            booking = curs.fetchone()
            if not booking:
                print("Booking ID not found.")
                return
            print(f"Current Room: {booking[0]}, Current Booking Time: {booking[1].strftime('%Y-%m-%d %H:%M:%S')}")

        new_room_name = input("Enter new room name (leave blank to keep current): ")
        if not new_room_name:  # If no new room name is entered, keep the old one
            new_room_name = booking[0]
        
        new_booking_time = input("Enter new booking time (YYYY-MM-DD HH:MM:SS, leave blank to keep current): ")
        if not new_booking_time:  # If no new time is entered, keep the old one
            new_booking_time = booking[1].strftime('%Y-%m-%d %H:%M:%S')

        admin.update_room_booking(choose_booking_id, new_room_name, new_booking_time)
        print("Booking updated successfully.")
    else:
        print("No changes made.")

def monitor_equipment(admin):
    equipment_records = admin.monitor_equipment_maintenance()
    if equipment_records:
        for record in equipment_records:
            print(f"Equipment ID: {record[0]}, Name: {record[1]}, Maintenance Due: {record[2]}")
    else:
        print("All equipment is up to date.")

def update_class_schedule(admin):
   

    # Option to print class info
    while True:
         # Display all class schedules
        with admin.conn.cursor() as curs:
            print_class_schedules(curs)


        info_choice = input("Would you like to view change any classes? (yes/no): ")
        if info_choice.lower() == 'yes':
            class_id = input("Enter the Class ID to view details: ")
            clear_screen()

            print_schdule_handler(admin,class_id)
        else:
            # User choice for updating or deleting
            return
        
def manage_billing(admin, member_id):
    while True:
        clear_screen()
        print("1. Add or Update Bill")
        print("2. Remove Bill")
        print("3. Back to Main Menu")
        choice = input("\nEnter Option: ")

        if choice == '1':
            amount_due = input("Enter the amount due: ")
            due_date = input("Enter the due date (YYYY-MM-DD): ")
            admin.process_billing(member_id, amount_due, due_date)
        elif choice == '2':
            # Proceed with removing the bill
            admin.process_billing(member_id)
        elif choice == '3':
            return  # Exit the billing management
        else:
            print("Invalid choice. Please select a valid option.")
        input("Press Enter to continue...")  # Pause before re-displaying the menu
