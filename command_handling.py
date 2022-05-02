# ======================================
# DESCRIPTION
# ======================================
# This script handles all user input and correctly executes it, according to the menu the user is currently in.


# ======================================
# IMPORT
# ======================================
from classes import *
from database_handling import *
from configuration import *

# ======================================
# MAIN FUNCTIONS
# ======================================

# Recieve user input and excecute it as an order.
# Note: get_input, parse_order, and execute_menu_order are separated here in order to facilitate easy execution of orders, even when the user has not specified an input.
def get_input(app):
    order = str(input('>>> \t')).strip()
    o = order.replace(' ','_')
    parse_order(app, o)


# Try to understand the different components of the order.
def parse_order(app, o):
    # If the user entered nothing, run the default command on the current menu.
    if o == "":
        app.current_menu['default_command'](app)
    
    # Otherwise try to understand the components of the command.
    else:
        # Split the order to find the first word.
        split_order = o.split('_')

        first_word = split_order[0].lower()

        match first_word:
            case 'view':
                # If the first word is view, take remaining words in the command and turn it into a single string.
                course_name = ''

                i = 1
                while i < len(split_order):
                    course_name += split_order[i]+' '
                    i += 1
                course_name = course_name.strip()
                
                # Run the view_specific_course function, using the remainder of the order as our command, which returns a True or False value.
                result = view_specific_course(app,course_name)

                # If True, go directly to viewing that course.
                if result:
                    app.current_menu['default_command'](app)

                # Otherwise, try to execute the view command on the current menu.
                else:
                    order= o.lower()
                    execute_menu_order(app,order)

            # If the first word is not one of the above commands, execute the command.   
            case _:
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


# Exit the program.
def app_quit(app,y='none'):
    print("\nGoodbye!\n")
    app.running=False
    quit()