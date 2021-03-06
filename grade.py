# ======================================
# DESCRIPTION
# ======================================
# This script defines all functions associated with setting and changing student grades.


# ======================================
# IMPORT
# ======================================
import detail_course as dc
from classes import *
from database_handling import *
from configuration import *


# ======================================
# FUNCTIONS
# ======================================

# Choose an assignment and show the list of all students and their grade in the assignment.
def view_grade(app,y='None'):
    # Set view variables accordingly.
    app.course_details = True

    # If we are already looking at a specific assignment, set the assignment title and target assignment accordingly.
    if app.view_grades or app.view_assignment_details:
        target_assignment = [x for x in all_assignments.find({'_id':app.current_assignment})]
        assignment_title = target_assignment[0]['Name']
    # Otherwise...
    else:
        # Get input from the user regardling what assignment to show.
        assignment_title = str(input("Please enter the name of the assignment you wish to view.\n>>>\t")).strip()
        # Get a list of all assignments with the given title associated with the current course.
        target_assignment=[x for x in all_assignments.find({'CourseID':app.current_course,'Name':assignment_title})]
        

    # If no assignment was found, see if the input was an exit command. If so, run the default command for the current menu. Otherwise, print an error message and start over.
    if len(target_assignment)==0:
        if assignment_title in exit_commands:
            app.current_menu['default_command'](app)
        else:
            print("Sorry, no assignment of that name could be found. Please try again.")
            view_grade(app)

    # If an assignment was found, get the correctly-sorted student list, and print the column headers.
    else:
        app.view_grades = True
        app.current_assignment = target_assignment[0]['_id']

        a = target_assignment[0]

        student_list = dc.sort_student_list(app)
        print('\n| Student Name           | %s '%assignment_title)

        # For each student in the list...
        for s in student_list:
            s_id = str(s['_id'])
            name_length = len(s['First Name'])+len(s['Last Name'])+1

            # Try to calculate the percentage grade based on the total points possible in the assignment. If the grade is not a number, the grade is
            try:
                g_perc = str((round(a[s_id]/a['Total Points'],2))*100)
            except:
                g_perc = ''

            # Print their first and last name
            print('| %s %s %s| %s '%(s['First Name'],s['Last Name'],(' '*(len('Student Name          ')-name_length)),g_perc))

    # Return the title of the assignment, its id, and the total points associated with it.
    return [assignment_title, a['_id'], a['Total Points']]


# Return a specific student.
def tgt_student(app, y='None'):
    # Get input from the user for the name of the student.
    student_name = str(input("Which student's grade would you like to edit?\n>>>\t")).strip()

    # Split the name into first and last names. If there is no last name, make it blank.
    name_split = student_name.split()
    first_name = name_split[0]
    try:
        last_name = name_split[1]
    except IndexError:
        last_name = ''

    # If more than 2 names were given, add any additional names to the last name.
    if len(name_split) > 2:
        for n in name_split[2:len(name_split)]:
            last_name += (' ' + n)

    # Get a list of all students associated with the given course with the provided first and last names.
    target_student = [x for x in all_students.find({'CourseID':app.current_course,'First Name':first_name, 'Last Name':last_name})]
    
    # If no students were found, check to see if the name was an exit command. If so, run the default command for the current menu. Otherwise, print an error message and start over.
    if len(target_student) == 0:
        if student_name in exit_commands:
           app.current_menu['default_command'](app) 
        else:
            print("Sorry, no student with that name could be found. Please try again.")
            tgt_student(app)
    
    # If a student was found, set the target student to the first returned item, and run the change_specific_grade_value function.
    else:
        return target_student[0]

# Pick whether to enter grades as a percentage or points out of the total.
def percent_or_points(app, y='None'):
    # Get input from the user
    perc_or_points = str(input("Would you like to enter grades as a percentage, or as points out of the total?\n>>>\t")).strip()

    # If the input was in the exit commands, return to the course details view.
    if perc_or_points in exit_commands:
        app.current_menu['default_command'](app)
    # If the input was either percentage or points, run the associated function.
    elif perc_or_points == 'percentage' or perc_or_points == 'points':
        return perc_or_points

    # Otherwise, print an error message and start over.
    else:
        print("Sorry, I didn't understand that. Please try again.")
        percent_or_points(app)


# Choose an assignment and pick whether to input as points or percentage.
def set_all_grades(app,y='None'):
    # If we are already looking at a specific assignment, set the assignment title and target assignment list accordingly.
    if app.view_assignment_details or app.view_grades:
        target_assignment = [x for x in all_assignments.find({'_id':app.current_assignment})]
        assignment_title = target_assignment[0]['Name']

    # Otherwise...
    else:
        # Get an input for the assignment name from the user.
        assignment_title = str(input("Please enter the name of the assignment you wish to grade.\n>>>\t")).strip()
        # Get a list of all assignments with that name associated with the current course.
        target_assignment=[x for x in all_assignments.find({'CourseID':app.current_course, 'Name':assignment_title})]

    # If no such assignment was found, check to see if the name was an exit command. If so, do nothing. Otherwise, print an error message and start over.
    if len(target_assignment)==0:
        if assignment_title in exit_commands:
            pass
        else:
            print("Sorry, no assignment of that name could be found. Please try again.")
            set_all_grades(app)

    # If the assignment was found, ask the user for percentage or points input and run the assign grades function.
    else:
        points = target_assignment[0]['Total Points']
        perc_or_points = percent_or_points(app)
        assign_grades(app,assignment_title, target_assignment,perc_or_points,points)


# For a given assignment, set grades for each student in the current course.
def assign_grades(app, assignment_title, target_assignment, perc_or_points, points):
    # Get the total points for the assignment and a sorted student list.
    student_list = dc.sort_student_list(app)

    # Print the header
    print('Student Name | %s | %i Total Points '%(assignment_title, points))    

    # For each student in the list...
    for s in student_list:
        # Calculate the amount of blank space necessary to create even columns, and print their name and a bar.
        name_length = len(s['First Name'])+len(s['Last Name'])+1
        print(s['First Name']+ " " + s['Last Name'] +(" "*(len('Student Name ')-name_length)) + "| ", end=' ')

        # Get an inputted grade from the user.
        grade=input().strip()

        # If the grade was in the list of exit commands, break the loop.
        if grade in exit_commands:
                break
        else:
            # Otherwise, try to turn the grade into a float.
            try:
                grade = float(grade)

                # Calculate the correct grade input based on whether it is a percentage, or points.
                if perc_or_points == 'percentage':
                    grade_input = float((grade/100.0)*points)
                elif perc_or_points == 'points':
                    grade_input = grade
                else:
                    break
            # If the grade can't be converted to a float, the grade input is a None type object.
            except ValueError:
                grade_input = None

            # Update the list of all assignments to reflect the student's grade in that assignment.
            all_assignments.update_one({'_id':target_assignment[0]['_id']},{'$set':{str(s['_id']):grade_input}})

    # Run the default command for the current menu.
    app.current_menu['default_command'](app)


# Change the grade of a given student for a given assignment.
def change_specific_grade_value(app,s, assignment_title, assignment_id, perc_or_points,points):
    # Print column headers.
    print('Student Name          | %s | Total Points %i'%(assignment_title,points))

    # Calculate blank space necessary to make even columns.
    name_length = len(s['First Name'])+len(s['Last Name'])+1

    # Get grade input from the user
    g=str(input(s['First Name']+ " " + s['Last Name'] +(" "*(len('Student Name          ')-name_length)) + "| ")).strip()

    try:
        # Try to turn the input into a float.
        grade = float(g)

        # Calculate the correct grade input based on whether it is a percentage, or points.
        if perc_or_points == 'percentage':
            grade_input = float((grade/100.0)*points)
        elif perc_or_points == 'points':
            grade_input = grade
        else:
            grade_input = None

    # If we can't return a float, set the grade input to a None type object.
    except ValueError:
        grade_input=None

    # Update the assignment collection to indicate the student's grade in that assignment.
    all_assignments.update_one({'_id':assignment_id},{'$set': {str(s['_id']):grade_input}})

    # Return to the Course Details View.
    app.current_menu['default_command'](app)


# View all student grades in an assignment, and then edit a specific student's grade.
def edit_grade(app,y='None'):
    # Run the view_grade function and return a list.
    view_list = view_grade(app)

    # Set variables accordingly.
    assignment_title = view_list[0]
    try:
        assignment_id = view_list[1]
    except IndexError:
        assignment_id = ''
    try:
        points = view_list[2]
    except IndexError:
        points = ''

    # If the assignment title was an exit command, return to the Course Details View
    if assignment_title in exit_commands:
        app.current_menu['default_command'](app)

    # Otherwise, run the percent_or_points function.
    else:
        perc_or_points = percent_or_points(app)
        student = tgt_student(app)
        change_specific_grade_value(app,student,assignment_title,assignment_id,perc_or_points,points)