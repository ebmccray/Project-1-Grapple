# The command line interface


# --- IMPORT PACKAGES ---
import course_commands as cc
import detail_course as dc
import help
import grade
import configuration as config


# --- WELCOME ---
def welcome():
    print('Hello, welcome to %s!'%config.app_name)


# --- GET INPUT
def get_input():
    # Receive the user's input as a string.
    i = str(input('Please enter a command or type "help" to get started. >>>\t'))
    # Remove spaces and convert to lowercase.
    user_input = i.lower().replace(' ','')
    match_input(user_input)


# --- MATCH INPUT ---
# Checks the user's input against a variety of cases, and then runs associated commands.
def match_input(input):
    match input:
        case 'help':
            help.main_help()

        case 'coursehelp':
            help.course_help()

        case 'assignmenthelp':
            help.assignment_help()

        case 'courses':
            cc.all_courses()


        case 'addcourse':
            cc.add_course()
        
        case 'renamecourse':
            cc.rename_course()

        case 'deletecourse':
            cc.delete_course()

        case 'addassignment':
            cc.add_assignment()

        case 'renameassignment':
            cc.rename_assignment()
        
        case 'deleteassignment':
            cc.delete_assignment()

        case 'viewcourse':
            dc.view_course()
        
        case 'grade':
            grade.set_grade()

        case 'quit':
            print("\nGoodbye!\n")
            quit()

        case _ :
            print('\nSorry, that was not a recognized command. Try entering "help" for a list of available commands.\n')