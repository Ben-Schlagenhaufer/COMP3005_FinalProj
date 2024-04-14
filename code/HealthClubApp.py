import psycopg2
import json
import time

# Importing classes
from memberClass import Member
from trainerClass import Trainer
from adminClass import Admin

#Importing modules
from admin_module import admin_menu
from trainer_module import trainer_menu
from member_module import member_menu, register_member

import os

def clear_screen():
    # Clear the console screen based on the operating system
    if os.name == 'nt':  # for Windows
        _ = os.system('cls')
    else:  # for Mac 
        _ = os.system('clear')


# Load database configuration from a file
with open('databaseInfo.json', 'r') as f:
    config = json.load(f)

DB_NAME = config['database']['DB_NAME']
DB_USER = config['database']['DB_USER']
DB_PASS = config['database']['DB_PASS']
DB_HOST = config['database']['DB_HOST']
DB_PORT = config['database']['DB_PORT']

def get_connection():
    return psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)

def authenticate_user(conn, role):
    print("================================ LOGIN ====================================\n")

    if role == "member":
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        query = "SELECT FirstName, LastName, Email, Password, FitnessGoals, HealthMetrics FROM Members WHERE Email = %s AND Password = %s"
        parameters = (email, password)
        with conn.cursor() as curs:
            curs.execute(query, parameters)
            result = curs.fetchone()
        if result:
            print("Login successful.")
            return Member(conn, *result)  # Creating Member instance
        else:
            print("Login failed.")
            return None

    elif role == "trainer":
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        query = "SELECT FirstName, LastName, Email, Expertise FROM Trainers WHERE FirstName = %s AND LastName = %s"
        parameters = (first_name, last_name)
        with conn.cursor() as curs:
            curs.execute(query, parameters)
            result = curs.fetchone()
        if result:
            print("Login successful.")
            return Trainer(conn, *result)  # Creating Trainer instance
        else:
            print("Login failed.")
            return None
        
    elif role == "admin":
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        query = "SELECT FirstName, LastName, Email FROM administrativestaff WHERE FirstName = %s AND LastName = %s"
        parameters = (first_name, last_name)
        with conn.cursor() as curs:
            curs.execute(query, parameters)
            result = curs.fetchone()
        if result:
            print("Login successful.")
            return Admin(conn)
        

    else:
        print("Invalid role specified.")
        return None


def main():
    conn = get_connection()  # Ensure this is your method to establish a DB connection

    while True:
        clear_screen()

        print("========================== FITNESS CLUB ==============================\n")
        print("Welcome to the Health Club App!\n")
        print("State your role to proceed.")
        print("1. Member")
        print("2. Trainer")
        print("3. Admin")
        print("4. Quit")
        print("\n======================================================================")
        role = input("Enter option: ").lower()

        if role == "1":
            role = "member"
        elif role == "2":
            role = "trainer"
        elif role == "3":
            role = "admin"
        elif role == '4':
            print("Exiting...")
            break
        else:   
            print("Invalid option. Please select a valid role.")
            time.sleep(1)
            continue
        

        clear_screen()
        if role == "member":
            answer = input("Do you have an account with us? (yes/no): ")
            if answer.lower() == "no":
                register_member(conn)
        
        while True:
            clear_screen()
            user = authenticate_user(conn, role)
            if user:
                if isinstance(user, Member):
                    member_menu(user)
                    break
                elif isinstance(user, Trainer):
                    trainer_menu(user)
                    break
                elif isinstance(user, Admin):
                    admin_menu(user)  # Assume admin does not need data transfer
                    break
            else:
                print("\nAuthentication failed. Please try again.")
                input("\nPress Enter to continue...")
        
        input("\nPress Enter to continue...")  # Pause before clearing the screen

if __name__ == "__main__":
    main()

