# This module contains all the code requied to interact with the 
# sqlite3 database.

import sqlite3
import hashlib
import datetime

conn = sqlite3.connect('database.db',
                        detect_types=sqlite3.PARSE_DECLTYPES | 
                        sqlite3.PARSE_COLNAMES)

def init_db():
    """
    Creates a new database by using the schema it finds inside 
    the 'init.sql' SQL script. This function is only called if the
    init() function in main.py doesn't find a pre-existing database.
    """

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone()[0] != 1:           # tables aren't created
            file = open('init.sql')
            sql_string = file.read()
            cursor.executescript(sql_string)
    except Exception as e:
        print("Could not initialize database.\n", "Error: ", e)
    
    cursor.close()

def close():
    """
    Closes the connection to the database. This function is called 
    before exiting the application.
    """

    conn.close()


def query(query_str: str) -> list:
    cursor = conn.cursor()
    cursor.execute(query_str)
    rows = cursor.fetchall()
    return rows

def create_new_user():
    """
    Creates a new user to manage expenses for.
    """
    print("\n\t\tCREATE NEW USER")
    username = input("Choose an username: ").strip()
    password = input(f"Choose a password for '{username}': ").strip()
    password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"INSERT INTO users (username, password) \
            VALUES ('{username}', '{password_hash}')")
    
    except sqlite3.Error as error:
        print("Failed to create user. The username might already be taken, please choose another username.")
        # print(error.__class__, error.args)
    
    cursor.close()
    conn.commit()

def any_user_exists() -> bool:
    """
    Queries the 'users' table to check if there is at least one user.
    """

    query = "SELECT * from users"
    cursor = conn.cursor()
    cursor.execute(query)
    if cursor.fetchone():           # returns None if no next record
        return True
    else:
        return False

def validate_user(username: str, password: str) -> bool:
    """
    Validates the user entered credentials against credentials in the dataabase
    """

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
    row = cursor.fetchone() 
    if row == None:
        choice = input("This user does not exist. Would you like to create a new user? [y/n] ")
        if choice == 'y':
            create_new_user()
        elif choice == 'n':
            print("Okay.")
        else:
            print("Invalid choice.")
        return False

    elif hashlib.md5(password.encode('utf-8')).hexdigest() != row[2]:
            print("Username and Password do not match. Please try again.")
            return False
    
    return True

def get_userid(username: str) -> int:
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
    user = cursor.fetchone()
    return user[0]


def insert_transaction(userid: int, name: str, amount: float):
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO expenses (userid, name, amount, timestamp) \
            VALUES ('{userid}', '{name}', '{amount}', '{datetime.datetime.now()}')")
    except sqlite3.Error as e:
        print("Failed to add expense. Check input and try again.")
        print(e.__class__, e.args)
    finally:
        cursor.close()
        conn.commit()


def delete_expense(id: int):
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM expenses WHERE id={id}")
        
    except sqlite3.Error as e:
        print("Failed to delete expense.")
        print(e)
    finally:
        cursor.close()
        conn.commit()
        

