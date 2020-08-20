# This module contains functions to deal with the commands that
# the user enters into the shell. There are a number of possible
# commands, and each command has a dedicated handler function 
# to handle it. Additionally, there is a router function 
# that receives the commands and routes it its relevent handler.

import database


def route(userid: int, command: str):
    """
    This function takes as parameter all the commands and forwards it
    to the respective handler functions for further processing.
    """

    if command == "help":
        show_helptext()
    else:
        cmd = command.split()
        if cmd[0] == 'add':
            add_expense(userid, cmd)
            check_if_budget_crossed(userid)
        elif cmd[0] == 'remove':
            remove_expense(userid, cmd)
            check_budget(userid)
        elif cmd[0] == 'budget':
            set_budget(userid, cmd)
        elif cmd[0] == 'nobudget':
            remove_budget(userid, cmd)
        elif cmd[0] == 'report':
            report(userid, cmd)
        else:
            print("Invalid command. Type 'help' to see available commands.")


def show_helptext():
    """
    Prints help text on user's screen. It contains a list of all
    the features and available commands and their options.
    """

    help_text = """
        Description: PyExpense is an expense manager that can keep 
        track of all your expenditure and helps you manage expenses
        better.

        Commands:
        add name amount     -   add a record of an expense, where 'name' can be 
                                what you spent on and 'amount' is how much you
                                spent
        remove name         -   remove a previously added expense named 'name'
        report              -   get a report of your expenses from the past week
        report n            -   get a report from previous 'n' weeks, grouped
                                by week
        budget x            -   set a weekly budget 'x', and PyExpense will
                                let you know if you cross it
        nobudget            -   remove a previously set budget
        exit                -   exit the application
        """
    print(help_text)


def add_expense(userid: int, cmd: list):
    assert len(cmd) == 3, "Please enter using the format --  add name amount"
    try: 
        name = cmd[1]
        amount = float(cmd[2])
        database.insert_transaction(userid, cmd[1], cmd[2])
    except ValueError:
        print("Please enter a number as amount.")
    except Exception as e:
        print(e)

def remove_expense(userid: int, cmd: list):
    assert len(cmd) == 2, "Please enter using the format -- remove name"
    
    name = cmd[1]
    rows = database.query(f"SELECT * FROM expenses WHERE userid='{userid}' AND name='{name}'")
    
    if len(rows) > 0:
        print("Following expenses match the name.")
        for index, row in enumerate(rows):
            date = f"{row[4].day}-{row[4].month}-{row[4].year}"
            print("Index\tName\tAmount\tTime")
            print(f"{index}\t{row[2]}\t{row[3]}\t{date}")
        choice = int(input("Enter the index of the expense you wish to delete: "))
        
        if choice >= 0 and choice < len(rows):
            database.delete_expense(rows[choice][0])
        else:
            print("Invalid index")
    else:
        print("No expense with such a name exists. Please check again.")
