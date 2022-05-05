# ======================================
# DESCRIPTION
# ======================================
# This script defines the functions of the main menu.


# ======================================
# IMPORT PACKAGES
# ======================================
import configuration as config


# ======================================
# FUNCTIONS
# ======================================
# Print a welcome message to the console.
def welcome(x='None',y='None'):
    print('\n'*8 + 'Hello, welcome to %s!\n'%config.app_name)


# Print the options on the main menu.
def main_menu(app,y='None'):
    # Set the view variables.
    app.view_all = False
    app.course_details = False
    app.view_assignment_details = False
    app.view_grades = False

    # Print main menu options.
    print('''Welcome to the main menu! Please enter one of following options:
    View All:\t\tShow a list of all your available courses
    View Course:\tShow students and grades of a specific course.
    View Assignment:\tShow the details of a particular assignment.
    Help:\t\tView help topics.
    Quit:\t\tExit the program.\n''')