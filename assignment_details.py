# ======================================
# DESCRIPTION
# ======================================
# This script defines the Assignment Details View and all functions having to do with assignment creation, deletion, and editing.


# ======================================
# IMPORT PACKAGES
# ======================================
from classes import *
from database_handling import *
from configuration import *
import detail_course as dc
import grade
import datetime as dt

# ======================================
# FUNCTIONS
# ======================================
def switch_assignments(app,y='None'):
    if app.course_details:
        assignment_title = str(input("Please input the name of the assignment you'd like to view.\n>>>\t")).strip()

        if assignment_title.lower() in exit_commands:
            dc.view_course(app)
        else:
            matching_assignments = [x for x in all_assignments.find({'Name':assignment_title})]
            if len(matching_assignments) == 0:
                print ("Sorry, no assignment named '%s' could be found. Please try again."%assignment_title)
                dc.view_course(app)
            else:
                app.current_assignment = matching_assignments[0]['_id']
                app.view_assignment_details = True
                app.current_course = matching_assignments[0]['CourseID']
                view_assignment_details(app)
    else:
        app.view_assignment_details = True
        dc.switch_course(app)


def view_assignment_details(app,y='None'):
    if app.view_assignment_details:
        matching_assignments = [x for x in all_assignments.find({'_id':app.current_assignment})]

        if len(matching_assignments) > 0:
            assignment = matching_assignments[0]
            assignment_title = assignment['Name']
            date_split = assignment['Date Due'].split('-')
            points = assignment['Total Points']
            course_match = [x['Name'] for x in courses.find({'_id':assignment['CourseID']})]
            course_title = course_match[0]

            print('\n\nCourse:\t\t%s'%course_title)
            print('Assignment:\t\t%s'%assignment_title)
            print('Total Points:\t\t%i'%points)
            print('Due Date:\t\t%s-%s'%(date_split[1],date_split[2]))
            print('\nMenu:\tView Grades\tRename Assignment\tEdit Points\tEdit Due Date\tView All Assignments\n')

        else:
            print("Sorry, that assignment could not be found.")
            dc.view_course(app)
    else:
        switch_assignments(app)


# Add an assignment to the list of assignments in the course.
def add_assignment(app,y='None'):
    # Get the name of the current course as part of a list.
    course_title = find_relevant(courses,'Name','_id',app.current_course)
    matching_assignment = [x for x in all_assignments.find({'CourseID':app.current_course,'Name':course_title})]

    # Get a title input from the user.
    assignment_title=str(input("\nPlease enter the name of the new assignment.\n>>>\t")).strip()

    # Check to see if the input is one of our exit commands. If it is, do nothing.
    if assignment_title.lower() in exit_commands:
        app.current_menu['default_command'](app)

    elif len(matching_assignment) > 0:
        response = str(input("An assignment called %s already exists for %s. Would you like to view grades for this assignment?\n>>>\t"%(assignment_title,course_title[0]))).strip().lower()
        if response in confirm_commands:
            app.view_grades = True
            app.current_assignment = matching_assignment[0]['_id']
            grade.view_grade(app)
        else:
            app.current_menu['default_command'](app)
    # Otherwise, ask the user how many points they want the assignment to be worth, and then create the assignment, associated with the current course.
    else:
        points_worth = assign_points(app, assignment_title)
        ass_date = assign_date(app,assignment_title)
        create_assignment(app,assignment_title,course_title[0],points_worth,ass_date)
        app.current_menu['default_command'](app)


def assign_points(app, assignment_title):
    points_input = str(input("How many points is %s worth?\n>>>\t"%assignment_title)).strip()

    if points_input.lower() in exit_commands:
        app.current_menu['default_command'](app)
    else:
        try:
            points_worth = int(points_input)
            return points_worth
        except:
            print("Sorry, that was not a valid grade input. Please try again.")
            assign_points(app,assignment_title)


def assign_date(app, assignment_title):
    date_input = str(input("When is %s due? Please input your answer in MM-DD format.\n>>>\t"%assignment_title)).strip()

    if date_input.lower() in exit_commands:
        app.current_menu['default_command'](app)
    else:
        try:
            date = dt.datetime.strptime(date_input,"%m-%d").date()
            return date
        except:
            print("Sorry that was not a valid date. Please try again.")
            assign_date(app,assignment_title)


def assign_new_name(app, old_title, assignment_id):
    new_title = str(input('Please enter the new name for "%s".\n>>>\t'%old_title)).strip()

    # Check to see if the input is one of the back commands.
    if new_title.lower() in exit_commands:
        pass

    # Otherwise, update the name of the assignment.
    else:
        all_assignments.update_one({'_id':assignment_id},{'$set':{'Name':new_title}})

    app.current_menu['default_command'](app)


def create_assignment(app,assignment_title,course_title,points_worth,assigned_date):
    Assignment(assignment_title, app.current_course, points_worth, assigned_date)
    print ('%s successfully added to %s.\n'%(assignment_title,course_title))


def edit_points(app,y='None'):
    matching_assignments = [x for x in all_assignments.find({'_id':app.current_assignment})]
    assignment_title = matching_assignments[0]['Name']
    new_points = assign_points(app, assignment_title)        
    all_assignments.update_many({'_id':app.current_assignment},{'$set':{'Total Points':new_points}})
    view_assignment_details(app)


def edit_date(app,y='None'):
    matching_assignments = [x for x in all_assignments.find({'_id':app.current_assignment})]
    assignment_title = matching_assignments[0]['Name']
    new_date = assign_date(app, assignment_title)        
    all_assignments.update_many({'_id':app.current_assignment},{'$set':{'Date Due':str(new_date)}})
    view_assignment_details(app)


# Rename an existing assignment in the course.
def rename_assignment(app,y='None'):
    if app.view_assignment_details:
        matching_assignments = [x for x in all_assignments.find({'_id':app.current_assignment})]
        target_assignment = matching_assignments[0]
        old_title = target_assignment["Name"]
        
    else:
        # Get title input from the user.
        old_title = str(input("Please enter the name of the assignment you wish to edit.\n>>>\t")).strip()

        # Search for the assignment in the collection of all assignments, if it is associated with the current course.
        matching_assignments = [x for x in all_assignments.find({'CourseID':app.current_course,'Name':old_title})]
        target_assignment = matching_assignments[0]

    # If we didn't find an assignment, check to see if it was actually a back command, and go back if it was. Otherwise, print an error and restart.
    if len(matching_assignments) == 0:
        if old_title.lower() in exit_commands:
            pass
        else:
            print("\nSorry, no assignment of that name could be found in the current course. Please try again.")
            rename_assignment(app)

    # If we found an Assignment, get input from the user for the new title.
    else:
        assign_new_name(app,old_title, target_assignment['_id'])
    
    app.current_menu['default_command'](app)


# Remove an assignment from the course.
def delete_assignment(app,y='None'):
    # Get the name of the course as part of a list.
    course_title = find_relevant(courses,'Name','_id',app.current_course)
    # Get title input from the user.
    if app.view_assignment_details:
        target_assignment = [x for x in all_assignments.find({'_id':app.current_assignment})]
        title = target_assignment[0]['Name']
    else:
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

    # Otherwise, remove the assignment from the collection of all assignments.
    else:
        app.current_menu = app.menu_options['view_course']
        app.view_assignment_details = False
        app.current_assignment = None
        all_assignments.delete_many({'_id':target_assignment[0]['_id']})
        print("%s was successfully deleted from the assignment list of %s."%(title,course_title[0]))

    app.current_menu['default_command'](app)