# PyExpense

PyExpense is a basic command-line based expense and budget manager.

## System Requirements

Tested on Python 3.8.1. Requires Python 3.6 or higher.
No external dependency required. PyExpense is built using only the Python stdlib.

## How To Run

Clone this repository with

    git clone https://github.com/funoctis/pyexpense.git

To start PyExpense, run

    python3 main.py

The command can differ based on your system. If you're on Windows, use `python main.py`.

## Features

- Supports multiple users
- Secure login for each user before accessing the portal
- Add a new expense
- Remove a previously added expense
- Set a weekly budget
- Remove the previously set budget
- Get an warning if your weekly expenses go over the set budget
- Get a weekly report, i.e., of the last 7 days
- Get a report for 'n' number of week, for e.g., get a report of the last 21 days by specifying 3 weeks

## How To Use

The app will greet you with an option to login to an existing user or create a new user. If running app for the first time, it will detect that no users are present in the database and will prompt you to create a new user.

Once you've registed as a user, login using the username and password to continue. The passwords are stored securely using an hash. *(Others can still access your data as the sqlite3 database doesn't require credentials to be connected to)*

After you're logged in, you will see the PyExpense shell which lets you use the available commands. 

### Available Commands for the PyExpense Shell

`add name amount`    -   add a record of an expense, where 'name' can be what you spent on and 'amount' is how much you spent

`remove name`   -   remove a previously added expense named 'name'

`report`    -   get a report of your expenses from the past week

`report n`  -   get a report from previous 'n' weeks, grouped by week

`budget`    -   see your current budget

`budget x`  -   set a weekly budget 'x', and PyExpense will let you know if you cross it

`nobudget`  -   remove a previously set budget

`logout`    -   logout from current account

`exit`  -   exit the application

    