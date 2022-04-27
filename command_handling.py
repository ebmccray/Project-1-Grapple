# ======================================
# DESCRIPTION
# ======================================
# This script handles all user input and correctly executes it, according to the menu the user is currently in.
#
# This script also defines the "EventHandler" class, an object which manages the session.


# ======================================
# IMPORT
# ======================================
import main_menu as mm
import help
import course_commands as cc
import detail_course as dc
import grade
from classes import *


# ======================================
# EVENT HANDLER
# ======================================
class EventHandler():
    def __init__(self):
        # Define boolean values for the Event Handler.
        self.running = True
        self.view_all = False
        self.course_details = False


        # Define lists of commands and their synonyms.
        self.exit_commands = ['quit','cancel','back','exit','return','escape','none']
        self.back_commands=['back','return','previous']
        self.command_synonyms=[
                ['view_all','all_courses','my_courses','view_courses','all_courses_view'],
                ['add_course','new_course','add_new_course','create_course'],
                ['rename_course','change_course_name','change_course'],
                ['delete_course','remove_course','drop_course'],
                ['view_course','view_details','edit_course','course_details','view_course_details','course_details_view'],
                ['add_assignment','new_assignment','add_new_assignment','create_assignment'],
                ['rename_assignment','edit_assignment'],
                ['delete_assignment','remove_assignment','drop_assignment'],
                ['add_student','new_student','add_new_student','enroll_student','enroll_new_student'],
                ['rename_student','change_student_name'],
                ['delete_student','remove_student','drop_student','kick_student','expel_student'],
                ['view_grades','view_assignment_grades'],
                ['set_grades','grade_assignment','grade_all','grade'],
                ['edit_grade','set_grade','change_grade'],
                ['home','main'],
                ['back','return'],
                ['quit','exit']
                ]


        # Define actions for the different menus in Dictionaries. These can be accessed and executed later view the Key name.

        # Main menu actions.
        self.main_menu_actions = {
            'default_command': mm.main_menu,
            'help': set_current_menu,
            'view_all':set_current_menu,
            'view_course':set_current_menu,
            'home': mm.main_menu,
            'back':set_current_menu,
            'quit': app_quit,
        }

        # Help menu actions
        self.help_menu_actions = {
            'default_command': help.main_help,
            'help':help.main_help,
            'view_all': help.course_help,
            'view_course':help.course_detail_help,
            'home':set_current_menu,
            'back': set_current_menu,
            'quit': app_quit,
        }

        # View courses menu
        self.view_courses_menu = {
            'default_command':cc.all_courses,
            'view_all':cc.all_courses,
            'add_course': cc.add_course,
            'rename_course': cc.rename_course,
            'delete_course': cc.delete_course,
            'view_course': set_current_menu,
            'help':help.course_help,
            'main':set_current_menu,
            'back':set_current_menu,
            'quit': app_quit,
        }

        # Course detail menu
        self.course_details_menu = {
            'default_command':dc.view_course,
            'switch_course':dc.switch_course,
            'rename_course':cc.new_title,
            'add_assignment':dc.add_assignment,
            'rename_assignment':dc.rename_assignment,
            'delete_assignment':dc.delete_assignment,
            'add_student': dc.add_student,
            'rename_student':dc.rename_student,
            'delete_student':dc.delete_student,
            'set_grades':grade.set_grade,
            'view_grades':grade.view_grade,
            'edit_grade':grade.edit_grade,
            'view_all':dc.view_course,
            'help':help.course_detail_help,
            'home':set_current_menu,
            'back':set_current_menu,
            'quit': app_quit,
        }


        # Define which menu a command switches to.
        self.menu_options = {
            'main':self.main_menu_actions,
            'help':self.help_menu_actions,
            'view_all':self.view_courses_menu,
            'view_course':self.course_details_menu,
        }
        

        # Set Event Handler variables.
        self.current_menu = self.main_menu_actions
        self.prev_menu = self.main_menu_actions
        self.new_menu = self.main_menu_actions

        self.current_course = None


# ======================================
# MAIN FUNCTIONS
# ======================================

# Recieve user input and excecute it as an order.
# Note: get_input and execute_order are separated here in order to facilitate easy execution of orders, even when the user has not specified an input.
def get_input(app):
    order = str(input('>>> \t'))
    o = order.lower().replace(' ','_')
    execute_order(app, o)


# Execute an order, based on the EventHandling class.
def execute_order(app, o):
    # If the user entered nothing, run the default command on the current menu.
    if o == "":
        app.current_menu['default_command'](app)
    
    # Otherwise, try to execute the order.
    else:
        try:
            order = o
            # If the order is one of the command synonmyns, then set the order to the default version of the synonym.
            for x in app.command_synonyms:
                if o in x:
                    order=x[0]

            # Exceute the order
            app.current_menu[order](app,order)
    
        # If we run into a KeyError exception because the order is not one of the command synonyms, print an error message and reset to the current menu.
        except KeyError:
            print('\nSorry, "%s" was not a recognized command. Try entering "help" for a list of available commands.\n'%o)
            app.current_menu['default_command'](app)


# Exit the program.
def app_quit(app,y='None'):
    print("\nGoodbye!\n")
    app.running=False
    quit()


# Switch the current menu to use when executing orders.
def set_current_menu(app,menu):
    # If the user wishes to go back, set the new menu to the previous menu and set our current menu as the previous menu.
    if menu =='back':
        app.new_menu = app.prev_menu
        app.prev_menu = app.current_menu

    # Otherwise, try to switch to the given menu. If the menu does not exist in the menu_options dictionary, keep the current menu.
    else:
        try:
            app.new_menu = app.menu_options[menu]
            app.prev_menu = app.current_menu
        except KeyError:
            app.new_menu = app.current_menu

    # Set the current menu to the new menu, and run the default menu command.
    app.current_menu = app.new_menu
    execute_order(app,'default_command')