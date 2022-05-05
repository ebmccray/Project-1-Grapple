# ======================================
# DESCRIPTION
# ======================================
# This script defines the various different menus available within the program, which commands each menu can handle, and what functions those commands perform.

# ======================================
# IMPORT
# ======================================
import main_menu as mm
import help
import course_commands as cc
import detail_course as dc
import grade
import assignment_details as ad
from command_handling import *


# Define actions for the different menus in Dictionaries. These can be accessed and executed later via the Key name.

# Main menu
main_menu_actions = {
    'default_command': mm.main_menu,
    'help': set_current_menu,
    'view_all':set_current_menu,
    'view_course':set_current_menu,
    'view_assignment':set_current_menu,
    'home': mm.main_menu,
    'back':set_current_menu,
    'quit': app_quit,
}

# Help menu
help_menu_actions = {
    'default_command': help.main_help,
    'help':help.main_help,
    'view_all': help.course_help,
    'view_course':help.course_detail_help,
    'view_assignment':help.assignment_detail_help,
    'info':help.app_info,
    'home':set_current_menu,
    'back': set_current_menu,
    'quit': app_quit,
}

# View All Courses menu
view_courses_menu = {
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

# Course Details menu
course_details_menu = {
    'default_command':dc.view_course,
    'switch_course':dc.switch_course,
    'view_course':dc.sort_by,
    'view_failing':dc.view_failing,
    'sort_by_last_name':dc.sort_by_name,
    'sort_reverse_alphabetical':dc.sort_reverse_alphabetical,
    'sort_by_grade':dc.sort_by_grade,
    'sort_by_grade_descending':dc.sort_by_grade_descending,
    'rename_course':cc.new_title,
    'view_assignment':set_current_menu,
    'add_assignment':ad.add_assignment,
    'rename_assignment':ad.rename_assignment,
    'delete_assignment':ad.delete_assignment,
    'add_student': dc.add_student,
    'add_multiple_students':dc.add_multiple_students,
    'rename_student':dc.rename_student,
    'delete_student':dc.delete_student,
    'set_grades':grade.set_all_grades,
    'view_grades':grade.view_grade,
    'edit_grade':grade.edit_grade,
    'view_all':set_current_menu,
    'help':help.course_detail_help,
    'home':set_current_menu,
    'back':set_current_menu,
    'quit': app_quit,
}

# Assignment Details menu
assignment_details_menu = {
    'default_command':ad.view_assignment_details,
    'view_assignment':ad.view_assignment_details,
    'switch_assignment':ad.switch_assignments,
    'rename_assignment':ad.rename_assignment,
    'edit_points':ad.edit_points,
    'edit_date':ad.edit_date,
    'view_grades':grade.view_grade,
    'set_grades':grade.set_all_grades,
    'edit_grade':grade.edit_grade,
    'help':help.assignment_detail_help,
    'view_course':set_current_menu,
    'home':set_current_menu,
    'back':set_current_menu,
    'quit': app_quit,
    }