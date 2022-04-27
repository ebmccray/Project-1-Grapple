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
    print('Hello, welcome to %s!'%config.app_name+"\n"*10)

# Show the options on the main menu.
def main_menu(app,y='None'):
    # Set the view variables.
    app.view_all = False
    app.course_details = False

    # Print options.
    print("Welcome to the main menu! Please use one of the following commands:\n\tAll Courses\n\tView Course\n\tHelp\n\tQuit\n")