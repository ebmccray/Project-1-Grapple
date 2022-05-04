# ======================================
# DESCRIPTION
# ======================================
# This script defines the Event Handler, an object which controls a given session.


# ======================================
# IMPORT
# ======================================
from menu_options import *


# ======================================
# EVENT HANDLER
# ======================================
class EventHandler():
    def __init__(self):
        # Define boolean values for the Event Handler.
        self.running = True
        self.view_all = False
        self.course_details = False
        self.view_grades = False
        self.sort_view = 'last_name_asc'

        # Set Event Handler variables.
        self.current_menu = main_menu_actions
        self.prev_menu = main_menu_actions
        self.new_menu = main_menu_actions

        self.current_course = None
        self.current_assignment = None

        # Define which menu a command switches to.
        self.menu_options = {
            'home':main_menu_actions,
            'help':help_menu_actions,
            'view_all':view_courses_menu,
            'view_course':course_details_menu,
        }