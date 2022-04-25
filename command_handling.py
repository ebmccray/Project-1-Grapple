# ======================================
# IMPORT PACKAGES
# ======================================
from asyncio.windows_events import NULL
import main_menu as mm
import help
import course_commands as cc
import detail_course as dc
import grade
from classes import *


# ======================================
# MAIN FUNCTIONS
# ======================================
def get_input(app):
    order = str(input('>>> \t'))
    o = order.lower().replace(' ','_')
    execute_order(app, o)


def execute_order(app, o):

    if o == "":
        app.current_menu['default_command'](app)
    
    else:
        try:
            app.current_menu[o](app,o)
        except KeyError:
            print('\nSorry, "%s" was not a recognized command. Try entering "help" for a list of available commands.\n'%o)
            app.current_menu['default_command'](app)


def app_quit(app,y='None'):
    print("Goodbye!\n")
    app.running=False
    quit()


def set_current_menu(app,menu):
    if menu == 'back' or menu == 'return':
        app.new_menu = app.prev_menu
        app.prev_menu = app.current_menu

    else:
        try:
            app.new_menu = app.menu_options[menu]
            app.prev_menu = app.current_menu
        except KeyError:
            app.new_menu = app.current_menu

    app.current_menu = app.new_menu
    execute_order(app,'default_command')


# ======================================
# CLASSES
# ======================================
class EventHandler():
    def __init__(self):
        self.running = True

        self.view_all = False
        self.course_details = False

        self.main_menu_actions = {
            'default_command': mm.main_menu,
            'help': set_current_menu,
            'view_courses':set_current_menu,
            'view_all':set_current_menu,
            'my_courses':set_current_menu,
            'main': mm.main_menu,
            'home': mm.main_menu,
            'back': set_current_menu,
            'return':set_current_menu,
            'quit': app_quit,
            'exit': app_quit,
        }

        self.help_menu_actions = {
            'default_command': help.main_help,
            'courses': help.course_help,
            'main': set_current_menu,
            'home':set_current_menu,
            'back': set_current_menu,
            'return':set_current_menu,
            'quit': app_quit,
            'exit': app_quit,
        }

        self.view_courses_menu ={
            'default_command':cc.all_courses,
            'help':help.course_help,
            'view_all':cc.all_courses,
            'view_courses':cc.all_courses,
            'add_course': cc.add_course,
            'new_course': cc.add_course,
            'rename': cc.rename_course,
            'rename_course': cc.rename_course,
            'delete_course': cc.delete_course,
            'remove_course': cc.delete_course,
            'view_course': set_current_menu,
            'view_details': set_current_menu,
            'edit_course': set_current_menu,
            'main':set_current_menu,
            'home':set_current_menu,
            'back':set_current_menu,
            'return':set_current_menu,
            'quit':app_quit,
            'exit': app_quit,
        }

        self.course_details_menu ={
            'default_command':dc.view_course,
            'rename_course':cc.new_name,
            'edit_course':cc.new_name,
            'add_assignment':dc.add_assignment,
            'new_assignment':dc.add_assignment,
            'rename_assignment':dc.rename_assignment,
            'delete_assignment':dc.delete_assignment,
            'remove_assignment':dc.delete_assignment,
            'add_student': dc.add_student,
            'new_student': dc.add_student,
            'rename_student':dc.rename_student,
            'delete_student':dc.delete_student,
            'remove_student':dc.delete_student,
            'grade':grade.set_grade,
            'enter_grades':grade.set_grade,
            'set_grade':grade.set_grade,
            'edit_grade':grade.edit_grade,
            'main':set_current_menu,
            'home':set_current_menu,
            'back':set_current_menu,
            'return':set_current_menu,
            'quit':app_quit,
            'exit': app_quit,
        }

        self.menu_options = {
            'main':self.main_menu_actions,
            'home':self.main_menu_actions,
            'help':self.help_menu_actions,
            'view_courses':self.view_courses_menu,
            'view_all':self.view_courses_menu,
            'my_courses':self.view_courses_menu,
            'view_course':self.course_details_menu,
            'edit_course':self.course_details_menu,
            'view_details':self.course_details_menu
        }

        self.exit_commands = ['quit','cancel','back','exit','return','escape']

        self.current_menu = self.main_menu_actions
        self.prev_menu = self.main_menu_actions
        self.new_menu = self.main_menu_actions

        self.current_course = NULL

        self.courses = [Course('Course 1'),Course('Course 2')]


# ======================================
# EXECUTE
# ======================================
app = EventHandler()

mm.welcome()

mm.main_menu(app)

while app.running:
    get_input(app)