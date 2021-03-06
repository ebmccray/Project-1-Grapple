# ======================================
# DESCRIPTION
# ======================================
# This script defines the Assignment Details View and all functions having to do with assignment creation, deletion, and editing.


# ======================================
# IMPORT PACKAGES
# ======================================
from ast import Index
from classes import *
from database_handling import *
from configuration import *
import detail_course as dc
import datetime as dt

# ======================================
# FUNCTIONS
# ======================================
# Switch view to a different assignment.
def switch_assignments(app,y='None'):
    # If we already know the course we're looking at...
    if app.course_details:
        # Get input from the user regarding the name of the assignment.
        assignment_title = str(input("Please input the name of the assignment you'd like to view.\n>>>\t")).strip()

        # Check to see if the assignment title was actually an exit command. If so, run the default command for the current menu.
        if assignment_title.lower() in exit_commands:
            app.current_menu['default_command'](app)
        # Otherwise, get a list of all assignments matching that name in the current course.    
        else:
            matching_assignments = [x for x in all_assignments.find({'Name':assignment_title,'CourseID':app.current_course})]
            # If no such assignment is returned, print an error message and run the default command for the current menu.
            if len(matching_assignments) == 0:
                print ("Sorry, no assignment named '%s' could be found in the current course. Please try again."%assignment_title)
                app.current_menu['default_command'](app)

            # Otherwise, set the current assignment variable, the assignment details variable, and the current course variable, and view assignment details.
            else:
                app.current_assignment = matching_assignments[0]['_id']
                app.view_assignment_details = True
                app.current_course = matching_assignments[0]['CourseID']
                view_assignment_details(app)

    # Otherwise, choose a course to look at.
    else:
        app.view_assignment_details = True
        dc.switch_course(app)


# Print out information regarding the current assignment.
def view_assignment_details(app,y='None'):
    # If we know what assignment we're looking at...
    if app.view_assignment_details:
        # Set view variables
        app.view_grades = False

        # Get the list of matching assignments - there should be one returned.
        matching_assignments = [x for x in all_assignments.find({'_id':app.current_assignment})]
        
        # If one is returned, match up variables to the current assignment.
        if len(matching_assignments) > 0:
            assignment = matching_assignments[0]
            assignment_title = assignment['Name']
            date_split = assignment['Date Due'].split('-')
            points = assignment['Total Points']
            course_match = [x['Name'] for x in courses.find({'_id':assignment['CourseID']})]
            course_title = course_match[0]

            # Print assignment information and a small menu to the console.
            print('\n\nCourse:\t\t%s'%course_title)
            print('Assignment:\t\t%s'%assignment_title)
            print('Total Points:\t\t%i'%points)
            print('Due Date:\t\t%s-%s'%(date_split[1],date_split[2]))
            print('\nMenu:\tView Grades\tRename Assignment\tEdit Points\tEdit Due Date\tView All Assignments\n')

        # Otherwise, print an error message and run the default command for the current app.
        else:
            print("Sorry, that assignment could not be found.")
            app.current_menu['default_command'](app)

    # Otherwise, pick an assignment to view.        
    else:
        switch_assignments(app)


# Add an assignment to the list of assignments in the course.
def add_assignment(app,y='None'):
    # Get the name of the current course as part of a list, and all assignments that already have that name in the current course.
    course_title = find_relevant(courses,'Name','_id',app.current_course)
    matching_assignment = [x for x in all_assignments.find({'CourseID':app.current_course,'Name':course_title})]

    # Get a title input from the user.
    assignment_title=str(input("\nPlease enter the name of the new assignment.\n>>>\t")).strip()

    # Check to see if the input is one of our exit commands. If it is, run the default command for the current menu.
    if assignment_title.lower() in exit_commands:
        app.current_menu['default_command'](app)

    # Otherwise, if we have returned an assignment with that title in the current course, ask the user if they would like to view that assignment.
    elif len(matching_assignment) > 0:
        response = str(input("An assignment called %s already exists for %s. Would you like to view grades for this assignment?\n>>>\t"%(assignment_title,course_title[0]))).strip().lower()
        # If the answer is yes, set Event Handler variables accordingly and run the default command.
        if response in confirm_commands:
            app.view_assignment_details = True
            app.current_assignment = matching_assignment[0]['_id']
            app.current_course = matching_assignment[0]['CourseID']
            app.current_menu = app.menu_options['view_assignment']
            app.current_menu['default_command'](app)
        # Otherwise, run the default command for the current menu.
        else:
            app.current_menu['default_command'](app)

    # Otherwise...
    else:
        # Ask the user how many points the assignment is worth and when its due date is with the assign_points and assign_date functions.
        points_worth = assign_points(app, assignment_title)
        assigned_date = assign_date(app,assignment_title)

        # Create the assignment and print a message to that effect to the console.
        Assignment(assignment_title, app.current_course, points_worth, assigned_date)
        print ('%s successfully added to %s.\n'%(assignment_title,course_title[0]))

        # Run the default command for the current menu.
        app.current_menu['default_command'](app)


# Return the total point value of a given assignment.
def assign_points(app, assignment_title):
    # Get input from the user.
    points_input = str(input("How many points is %s worth?\n>>>\t"%assignment_title)).strip()

    # If the input is actually an exit command, run the default command for the current menu.
    if points_input.lower() in exit_commands:
        app.current_menu['default_command'](app)

    else:
        # Otherwise, try to return the input as a float.
        try:
            points_worth = float(points_input)
            return points_worth
        # If the input is not a float, print an error message and start over.
        except:
            print("Sorry, that was not a valid grade input. Please try again.")
            assign_points(app,assignment_title)


# Return the due date of a given assignment.
def assign_date(app, assignment_title):
    # Get input from the suer.
    date_input = str(input("When is %s due? Please input your answer in MM-DD format.\n>>>\t"%assignment_title)).strip()

    # If the input is actually an exit command, run the default command for the current menu.
    if date_input.lower() in exit_commands:
        app.current_menu['default_command'](app)
    else:
        # Otherwise, try to return the input as a datetime month and date.
        try:
            date = dt.datetime.strptime(date_input,"%m-%d").date()
            return date
        # If the input cannot be turned into a valid datetime, print an error message and start over.
        except:
            print("Sorry that was not a valid date. Please try again.")
            assign_date(app,assignment_title)


# Update the name of a given assignment.
def assign_new_name(app, old_title, assignment_id):
    # Get input from the user.
    new_title = str(input('Please enter the new name for "%s".\n>>>\t'%old_title)).strip()

    # Check to see if the input is one of the back commands.
    if new_title.lower() in exit_commands:
        pass

    # Otherwise, update the name of the assignment.
    else:
        all_assignments.update_one({'_id':assignment_id},{'$set':{'Name':new_title}})

    # Run the default command for the current menu.
    app.current_menu['default_command'](app)


# Update the total point value of a given assignment.
def edit_points(app,y='None'):
    # Get a list with the current assignment - it should return 1.
    matching_assignments = [x for x in all_assignments.find({'_id':app.current_assignment})]

    # If for some reason we don't return that assignment, print an error message and run the default command for the current menu.
    if len(matching_assignments) == 0:
        print("Sorry, there was an error.")
        app.current_menu['default_command'](app)

    # Otherwise, get the new points total with the assign_points function and update the current assignment to reflect this change.
    else:
        assignment_title = matching_assignments[0]['Name']
        new_points = assign_points(app, assignment_title)        
        all_assignments.update_many({'_id':app.current_assignment},{'$set':{'Total Points':new_points}})

        # Run the default command for the current menu.
        app.current_menu['default_command'](app)


def edit_date(app,y='None'):
    # Get a list with the current assignment - it should return 1.
    matching_assignments = [x for x in all_assignments.find({'_id':app.current_assignment})]

    # If for some reason we don't return that assignment, print an error message and run the default command for the current menu.
    if len(matching_assignments) == 0:
        print("Sorry, there was an error.")
        app.current_menu['default_command'](app)

    # Otherwise, get the new due date with the assign_date function and update the current assignment to reflect this change.
    else:
        assignment_title = matching_assignments[0]['Name']
        new_date = assign_date(app, assignment_title)        
        all_assignments.update_many({'_id':app.current_assignment},{'$set':{'Date Due':str(new_date)}})
        # Run the default command for the current menu.
        app.current_menu['default_command'](app)


# Rename an existing assignment in the course.
def rename_assignment(app,y='None'):
    # If we are already viewing an assignment, set the target assignment and the old title according to the current assignment's id.
    if app.view_assignment_details:
        matching_assignments = [x for x in all_assignments.find({'_id':app.current_assignment})]
        target_assignment = matching_assignments[0]
        old_title = target_assignment["Name"]

    # Otherwise...    
    else:
        # Get title input from the user.
        old_title = str(input("Please enter the name of the assignment you wish to edit.\n>>>\t")).strip()
        # Search for the assignment in the collection of all assignments, if it is associated with the current course.
        matching_assignments = [x for x in all_assignments.find({'CourseID':app.current_course,'Name':old_title})]
        try:
            target_assignment = matching_assignments[0]
        except IndexError:
            target_assignment = None

    # If we didn't find an assignment, check to see if it was actually a back command, and go back if it was. Otherwise, print an error and restart.
    if len(matching_assignments) == 0:
        if old_title.lower() in exit_commands:
            pass
        else:
            print("\nSorry, no assignment of that name could be found in the current course. Please try again.")
            rename_assignment(app)

    # If we found an Assignment, get input from the user for the new title and update it.
    else:
        assign_new_name(app,old_title, target_assignment['_id'])
    
    app.current_menu['default_command'](app)


# Remove an assignment from the course.
def delete_assignment(app,y='None'):
    # Get the name of the course as part of a list.
    course_title = find_relevant(courses,'Name','_id',app.current_course)
    
    # If we are already viewing an assignment, set the target assignment and the old title according to the current assignment's id.
    if app.view_assignment_details:
        target_assignment = [x for x in all_assignments.find({'_id':app.current_assignment})]
        title = target_assignment[0]['Name']
    # Otherwise...
    else:
        # Get title input from the user.
        title = str(input("\nPlease enter the name of the assignment you wish to delete.\n>>>\t")).strip()

        # Search for the assignment in the collection of all assignments, if it is associated with the current course.
        target_assignment =[x for x in all_assignments.find({'CourseID':app.current_course, 'Name':title})]

    # If we didn't find an assignment, check to see if it was actually a back command, and go back if it was. Otherwise, print an error and restart.
    if len(target_assignment) ==0:
        if title.lower() in exit_commands:
            pass
        else:
            print("Sorry, no assignment of that name could be found. Please try again.")
            delete_assignment(app)

    # Otherwise, remove the assignment from the collection of all assignments and set view variables accordingly.
    else:
        app.current_menu = app.menu_options['view_course']
        app.view_assignment_details = False
        app.current_assignment = None
        app.course_details = True
        all_assignments.delete_many({'_id':target_assignment[0]['_id']})
        print("%s was successfully deleted from the assignment list of %s."%(title,course_title[0]))

    # Run the default command for the current menu.
    app.current_menu['default_command'](app)