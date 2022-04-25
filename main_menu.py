# ======================================
# IMPORT PACKAGES
# ======================================
import configuration as config


# ======================================
# FUNCTIONS
# ======================================
def welcome(x='None',y='None'):
    print('Hello, welcome to %s!'%config.app_name)

def main_menu(app,y='None'):
    app.view_all = False
    app.course_details = False
    print("\nWelcome to the main menu! Please use one of the following commands:\n\tView Courses\n\tHelp\n\tQuit\n")