# trainer_module.py

import os
import datetime

def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def trainer_menu(trainer):
    while True:
        clear_screen()  # Clear the screen each time the menu loops
        print(f"Welcome, Trainer {trainer.first_name} {trainer.last_name}!\n")

        print("================================ MENU ====================================\n")
        print("1. View Profile                  2. Set Available Times")  
        print("3. Update Schedule               4. Look Up Member")
        print("5. View Schedule                 6. Remove Schedule Item")
        print("\n7. Logout")
        print("\n=========================================================================")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_profile(trainer)
        elif choice == '2':
            set_available_times(trainer)
        elif choice == '3':
            update_trainer_schedule(trainer)
        elif choice == '4':
            look_up_member(trainer)
        elif choice == '5':
            trainer.print_schedule()
        elif choice == '6':
            schedule_id = input("Enter the Schedule ID to remove: ")
            if schedule_id.isdigit():
                trainer.remove_schedule(schedule_id)
            else:
                print("Invalid Schedule ID. Please enter a numeric ID.")
        elif choice == '7':
            print("Exiting menu...")
            break  # Exit the while loop
        else:
            print("Invalid choice. Please select a valid option.")

        input("Press Enter to continue...")  # Pause before clearing the screen


def set_available_times(trainer):
    available_times = []
    print("Enter new available times (type 'done' to finish):")
    while True:
        start_time_input = input("Start Time (YYYY-MM-DD HH:MM): ")
        if start_time_input.lower() == 'done':
            break
        end_time_input = input("End Time (YYYY-MM-DD HH:MM): ")
        # Convert to TIMESTAMP format here if necessary
        available_times.append({'start_time': start_time_input, 'end_time': end_time_input})
    trainer.set_available_times(available_times)

def view_profile(trainer):
    profile = trainer.get_profile()
    if profile:
        # print("Trainer Profile:")
        # print(f"Trainer ID: {profile['TrainerID']}")
        # print(f"Name: {profile['FirstName']} {profile['LastName']}")
        # print(f"Email: {profile['Email']}")
        # print(f"Expertise: {profile['Expertise']}")
        profile_data = [profile['TrainerID'], profile['FirstName'], profile['LastName'], profile['Email'], profile['Expertise']]
        headers = ["ID", "First Name", "Last Name", "Email", "Expertise"]
        col_widths = [max(len(str(header)), len(str(profile_data[i]))) for i, header in enumerate(headers)]
        header_row = " | ".join(header.ljust(width) for header, width in zip(headers, col_widths))
        print(header_row)
        print("-" * len(header_row))
        data_row = " | ".join(str(item).ljust(width) for item, width in zip(profile_data, col_widths))
        print(data_row)

    else:
        print("Profile not found.")


def update_trainer_schedule(trainer):
    print("Current Schedule:")
    trainer.print_schedule()  # This method should print the current schedule.
    
    new_times = []
    print("Enter new available times (enter 'done' to finish):")
    while True:
        start_time_input = input("Start Time (YYYY-MM-DD HH:MM): ")
        if start_time_input.lower() == 'done':
            break
        if not validate_datetime(start_time_input):
            print("Invalid start time format. Please try again.")
            continue  # Skip to the next iteration of the loop

        end_time_input = input("End Time (YYYY-MM-DD HH:MM): ")
        if not validate_datetime(end_time_input):
            print("Invalid end time format. Please try again.")
            continue  # Skip to the next iteration of the loop

        new_times.append({'start_time': start_time_input, 'end_time': end_time_input})

    trainer.update_schedule(new_times)
    print("Schedule updated successfully.")


def add_trainer_to_database(trainer):
    trainer.add_to_database()

def look_up_member(trainer):
    member_name = input("Enter the member's first name to search: ")
    with trainer.conn.cursor() as curs:
        curs.execute("SELECT FirstName, LastName, Email FROM Members WHERE FirstName = %s", (member_name,))
        members = curs.fetchall()
        if members:
            print("Members found:")
            for member in members:
                print(f"Name: {member[0]} {member[1]}, Email: {member[2]}")
        else:
            print("No members found with that name.")

def validate_datetime(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False
