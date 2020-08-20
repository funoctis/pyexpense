# This is the main module of PyExpense and the entry into the app.

import database
import command_manager

import os


def login_user():
    """
    Logins the user in by taking their credentials and validating
    them against the database.
    Returns the username to be used for all further operations.
    """
    
    validated = False
    while not validated:
        try:
            print("\n\t\tLOGIN")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            if database.validate_user(username, password):
                validated = True
                return username
        except KeyboardInterrupt:
            print("\n\nExit.")
            database.close()
            exit()

def init():
    """
    Initialized the database if it doesn't exist already.
    Prints greeting.
    Checks if any user exists, if not then makes the user create new one. 
    """
    print("\nHello, welcome to PyExpense -- your personal expense manager!\n")
    print("Press Ctrl+C at any time to exit.\n")

    database.init_db()
    
    if not database.any_user_exists():
        print("We couldn't find any registered user. Please create a new user.")
        database.create_new_user()


def input_commands(username: str):
    """
    Runs an infinite loop for the logged in user to enter commands.
    """

    print(f"\nWelcome, {username}\n")
    print("For help on how to use PyExpense, type 'help'. To exit, type 'exit'.")

    userid = database.get_userid(username)   
    while True:
        try:
            command = input("> ").strip()
            if command == 'exit':
                exit()
            elif command == 'logout':
                break
            command_manager.route(userid, command)
        except KeyboardInterrupt:
            print("\nTo exit PyExpense, type 'exit'.")
        except AssertionError as e:
            print(e.args[0])
        except Exception as e:
            print(e)
    

if __name__ == "__main__":
    init()
    
    while True:
        try:
            print("Would you like to login or create a new user?\n1. Login\n2. Create New User")
            choice = input("Type '1' or '2', or 'exit':\n").strip()
            if choice == '1':
                username = login_user()
                input_commands(username)
            elif choice == '2':
                database.create_new_user()
            elif choice == 'exit':
                print("\nExit.")
                exit()
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nExit.")
            exit()
 