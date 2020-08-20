# This module contains functions to deal with the commands that
# the user enters into the shell. There are a number of possible
# commands, and each command has a dedicated handler function 
# to handle it. Additionally, there is a router function 
# that receives the commands and routes it its relevent handler.

import database
import datetime

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
            check_budget(userid)
        elif cmd[0] == 'remove':
            remove_expense(userid, cmd)
            check_budget(userid)
        elif cmd[0] == 'budget':
            if len(cmd) == 1:
                check_budget(userid)
                print("To set/change budget, use -- budget x")
            else:
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


def check_budget(userid: int):
    budget = database.get_budget_for_user(userid)
    if budget == None:
        print("You can set a budget with the budget command.")
    else:
        print("budget: ", budget[0])
        
        rows = database.query(f"SELECT name, amount, timestamp FROM expenses \
            WHERE userid={userid}")
        
        this_weeks_expenses = list()
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=7)
        
        for row in rows:
            if row[2] > start_of_week:
                pretty_date = f"{row[2].day}-{row[2].month}-{row[2].year}"
                this_weeks_expenses.append((row[0], row[1], pretty_date))

        weekly_total = 0
        for expense in this_weeks_expenses:
            weekly_total += float(expense[1])
        
        budget = float(budget[0])
        if weekly_total > budget:
            print("WARNING: You have exceeded the weekly budget.")
            print(f"Amount spent over budget: {weekly_total - budget}")
        else:
            print("You are within your weekly budget.")
            print(f"Safe to spend: {budget - weekly_total}")
        


def set_budget(userid: int, cmd: list):
    assert len(cmd) == 2, "Please enter using the format -- budget x"
    try:
        new_budget = float(cmd[1])
        database.update_budget(userid, new_budget)
    except ValueError:
        print("Please enter a number as budget.")
    except Exception as e:
        print(e)


def remove_budget(userid: int, cmd: list):
    assert len(cmd) == 1, "Please enter using the format -- nobudget"
    try:
        database.make_budget_null(userid)
    except Exception as e:
        print(e)


def report(userid: int, cmd: list):
    rows = database.query(f"SELECT name, amount, timestamp FROM expenses \
            WHERE userid={userid}")
    
    if len(cmd) == 1:
        
        this_weeks_expenses = list()
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=6)
        pretty_now = f"{now.day}-{now.month}-{now.year}"
        pretty_start_of_week = f"{start_of_week.day}-{start_of_week.month}-{start_of_week.year}"
        for row in rows:
            if row[2] >= start_of_week:
                pretty_date = f"{row[2].day}-{row[2].month}-{row[2].year}"
                this_weeks_expenses.append((row[0], row[1], pretty_date))

        # print("Sr. No\tName\t\tAmount\tDate")
        # for index, expense in enumerate(this_weeks_expenses):
        #     print(f"{index}\t{expense[0]}\t\t{expense[1]}\t{expense[2]}")

        expenses_by_day = {}
        
        weekly_total = 0
        # iterating over the list of expenses
        for expense in this_weeks_expenses:
            # checking the expense date in the dict
            if expense[2] in expenses_by_day:
                # add the current expense to dict
                expenses_by_day[expense[2]].append(expense)
            else:
                # initiate the date with list of expenses
                expenses_by_day[expense[2]] = [expense]
        
        print(f"\n\t\tEXPENSE REPORT FOR THE WEEK: {pretty_start_of_week} to {pretty_now}")
        # printing the expenses_by_day
        for day in expenses_by_day:
            day_total = 0
            print("\nDate: ", day)
            for index, single_expense in enumerate(expenses_by_day[day]):
                day_total += float(single_expense[1])
                print(f"\t{index}\t{single_expense[0]}\t\t{single_expense[1]}\t{single_expense[2]}")
            print(f"Total expenditure on {day}: {day_total}")
            weekly_total += day_total
        
        print(f"\nTotal expenditure from this week: {weekly_total}")

    
    elif len(cmd) == 2:
        try:
            n = int(cmd[1])
            days = 6+((n-1)*7)
            
            now = datetime.datetime.now()
            start_of_period = now - datetime.timedelta(days=days)
            pretty_now = f"{now.day}-{now.month}-{now.year}"
            pretty_start_of_period = f"{start_of_period.day}-{start_of_period.month}-{start_of_period.year}"
            
            this_periods_expenses = list()
            for row in rows:
                if row[2] >= start_of_period:
                    pretty_date = f"{row[2].day}-{row[2].month}-{row[2].year}"
                    this_periods_expenses.append((row[0], row[1], pretty_date))

                       
            expenses_by_day = {}
            
            weekly_total = 0
            # iterating over the list of expenses
            for expense in this_periods_expenses:
                # checking the expense date in the dict
                if expense[2] in expenses_by_day:
                    # add the current expense to dict
                    expenses_by_day[expense[2]].append(expense)
                else:
                    # initiate the date with list of expenses
                    expenses_by_day[expense[2]] = [expense]
            
            print(f"\n\t\tEXPENSE REPORT FOR THE PERIOD: {pretty_start_of_period} to {pretty_now}")
            # printing the expenses_by_day
            for day in expenses_by_day:
                day_total = 0
                print("\nDate: ", day)
                for index, single_expense in enumerate(expenses_by_day[day]):
                    day_total += float(single_expense[1])
                    print(f"\t{index}\t{single_expense[0]}\t\t{single_expense[1]}\t{single_expense[2]}")
                print(f"Total expenditure on {day}: {day_total}")
                weekly_total += day_total
            
            print(f"\nTotal expenditure from this period: {weekly_total}")

        except ValueError:
            print("Please enter a valid number of weeks")
        except Exception as e:
            print(e.__class__, e.args)

        

