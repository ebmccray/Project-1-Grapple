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
from database_handling import *
from configuration import *

# ======================================
# EVENT HANDLER
# ======================================
class EventHandler():
    def __init__(self):
        # Define boolean values for the Event Handler.
        self.running = True
        self.view_all = False
        self.course_details = False
        self.sort_view = 'last_name_asc'

        # Define actions for the different menus in Dictionaries. These can be accessed and executed later via the Key name.
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
            'home':set_current_menu,
            'back':set_current_menu,
            'quit': app_quit,
        }

        # Course detail menu
        self.course_details_menu = {
            'default_command':dc.view_course,
            'switch_course':dc.switch_course,
            'view_course':dc.sort_by,
            'view_failing':dc.view_failing,
            'sort_by_last_name':dc.sort_by_name,
            'sort_reverse_alphabetical':dc.sort_reverse_alphabetical,
            'sort_by_grade':dc.sort_by_grade,
            'sort_by_grade_descending':dc.sort_by_grade_descending,
            'rename_course':cc.new_title,
            'add_assignment':dc.add_assignment,
            'rename_assignment':dc.rename_assignment,
            'delete_assignment':dc.delete_assignment,
            'add_student': dc.add_student,
            'add_multiple_students':dc.add_multiple_students,
            'rename_student':dc.rename_student,
            'delete_student':dc.delete_student,
            'set_grades':grade.set_grade,
            'view_grades':grade.view_grade,
            'edit_grade':grade.edit_grade,
            'view_all':set_current_menu,
            'help':help.course_detail_help,
            'home':set_current_menu,
            'back':set_current_menu,
            'quit': app_quit,
        }

        # Define which menu a command switches to.
        self.menu_options = {
            'home':self.main_menu_actions,
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
# Note: get_input, parse_order, and execute_menu_order are separated here in order to facilitate easy execution of orders, even when the user has not specified an input.
def get_input(app):
    order = str(input('>>> \t'))
    o = order.replace(' ','_')
    parse_order(app, o)


# Try to understand the different components of the order.
def parse_order(app, o):
    # If the user entered nothing, run the default command on the current menu.
    if o == "":
        app.current_menu['default_command'](app)
    
    # Otherwise try to understand the components of the command.
    else:
        # Split the order to see if the first word is "view"
        split_order = o.split('_')

        if split_order[0].lower() =='view':
            course_name = ''

            # If so, take remaining words in the command and turn it into a single string.
            i = 1
            while i < len(split_order):
                course_name += split_order[i]+' '
                i += 1
            course_name = course_name.strip()
            
            # Run the view_specific_course function, using the remainder of the order as our command, and return a True or False value.
            result = view_specific_course(app,course_name)

            # If so, go directly to viewing that course.
            if result:
                dc.view_course(app)
            # Otherwise, try to execute the view command.    
            else:
                order= o.lower()
                execute_menu_order(app,order)

        # If the first word is not view, execute the command.   
        else:
            order = o.lower()
            execute_menu_order(app,order)


# Execute an order on the current menu.
def execute_menu_order(app,order):
    try:
        # If the order is one of the command synonmyns, then set the order to the default version of the synonym.
        for x in command_synonyms:
            if order in x:
                order=x[0]

        # Execute the order
        app.current_menu[order](app,order)

    # If we run into a KeyError exception because the order is not one of the command synonyms, print an error message and reset to the current menu.
    except KeyError:
        print('\nSorry, "%s" was not a recognized command. Try entering "help" for a list of available commands.\n'%order)
        app.current_menu['default_command'](app)


# Look for a specific course, based on its name.
def view_specific_course(app,course_name):
    # Get a list of all courses in the current course list to see if it matches the name we've been given.
    target_course = [x['_id'] for x in courses.find({'Name':course_name})]

    # If no such course exists, the result is false.
    if len(target_course) == 0:
        result = False

    # Otherwise, the result is true, and we will switch the properties of the event manage to indicate that we are viewing that course now.
    else:
        result = True
        app.course_details = True
        app.current_menu = app.menu_options['view_course']
        app.current_course = target_course[0]

    # Return the result.
    return result

    

# Exit the program.
def app_quit(app,y='none'):
    print("\nGoodbye!\n")
    app.running=False
    quit()


# Change which menu to use when executing orders.
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
    execute_menu_order(app,'default_command')