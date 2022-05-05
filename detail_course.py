# ======================================
# DESCRIPTION
# ======================================
# This script defines the functions of the Course Details View, such as seeing all students and assignments, sorting students by various criteria, and editing, adding, and removing students.


# ======================================
# IMPORT
# ======================================
from classes import *
from database_handling import *
from configuration import *
import menu_options
import assignment_details as ad


# ======================================
# FUNCTIONS
# ======================================

# Choose which course to view.
def switch_course(app,y='None'):
    # Get course title from the user.
    course_title=str(input("\nPlease enter the name of the course.\n>>>\t")).strip()

    # Find a list of corresponding courses by name, if it exists in the course list.
    target_course = find_relevant(courses,'_id','Name',course_title)

    # If we did not find a course, check to see if the command was one of our exit commands.
    if len(target_course) == 0:
        # If so, return to the All Courses View and reset the view and menu variables in the Event Handler.
        if course_title.lower() in exit_commands:
            menu_options.view_courses_menu['view_all'](app)
            app.current_menu = menu_options.view_courses_menu
            app.course_details = False

        # Otherwise, inform the user their course could not be found.
        else:
            print ("\nSorry, no course of that name could be found. Please try again.")
            switch_course(app)
    
    #If we did find the course, set view variables and change the current course accordingly, then run the view_course function.
    else:
        app.course_details=True
        app.current_course = target_course[0]
        if app.view_assignment_details:
            ad.switch_assignments(app)
        else:
            view_course(app)


# View the Students, Assignments, and Grades associated with the currently-selected course.
def view_course(app, y='None'):
    # Set the view variables.
    app.view_all = False
    app.view_grades = False
    app.view_assignment_details = False

    # If we've already selected a course, display the details associated with it using the sort_by function.
    if app.course_details:
        sort_by(app)

    # Otherwise, run the switch_course function to choose a course to view.
    else:
        switch_course(app)


# Create a student list, sorted the by the correct criteria, in the right order.
def sort_student_list(app, y='None'):
    # Get the EventHandler's sort_view variable, and set variables accordingly.
    match app.sort_view:
        case 'last_name_asc':
            criteria='Last Name'
            i = 1
        case 'last_name_desc':
            criteria = 'Last Name'
            i = -1
        case 'grade_asc':
            criteria='Total Grade %s'%str(app.current_course)
            i = 1
        case 'grade_desc':
            criteria='Total Grade %s'%str(app.current_course)
            i = -1
        case _ :
            criteria='Last Name'
            i = 1

    # Return a list of students, sorted by the criteria specified above.
    student_list = [x for x in all_students.find({'CourseID':app.current_course}).sort(criteria,i)]

    return student_list


# Displays students and their grades in the correct order.
def sort_by(app, y='None'):
    # Print the headers, and return their names and the total length.
    headers_and_length = print_headers(app)
    column_headers = headers_and_length[0]
    header_length = headers_and_length[1]

    # Assign a sorting descriptor based on the current sorting view in the EventHandler. 
    sort_views = {
            'last_name_asc':'last name, alphabetical',
            'last_name_desc':'last name, reverse alphabetical',
            'grade_asc':'grade, lowest first',
            'grade_desc':'grade, highest first'
        }
    try:
        descriptor = sort_views[app.sort_view]
    except KeyError:
        descriptor = 'last name, alphabetical'


    # Assign the sorted student list via the sort_student_list function.
    student_list = sort_student_list(app)

    # For each student in the list, print their name and grades with the print_student_grades function.
    for s in student_list:
        print_student_grades(app,s,column_headers)

    # Print the final line of the table, a description of the sorting method, and some basic menu options..    
    print('-'*(len(header_length)+1)+'\n')
    print('Showing: All students by %s.'%descriptor)
    print("Menu:\tGrade Assignment   Edit Grade\tAdd Assignment\tDelete Assignment\tView Assignment\n\tEnroll Student\tDelete Student\n\tRename Assignment/Student/Course\n\tSort by:\tLast Name\tGrade\tHighest First\tLowest First\n\tView Failing")


# VARIOUS SORTING FUNCTIONS
# Set the sort view to last_name_asc and sort.
def sort_by_name(app, y = 'None'):
    app.sort_view = 'last_name_asc'
    sort_by(app)

# Set the sort view to last_name_desc and sort.
def sort_reverse_alphabetical(app,y='None',i=1):
    app.sort_view = 'last_name_desc'
    sort_by(app)

# Set the sort view to grade_asc and sort.
def sort_by_grade(app, y='None',i=1):
    app.sort_view = 'grade_asc'
    sort_by(app)

# Set the sort view to grade_desc and sort.
def sort_by_grade_descending(app,y='None'):
    app.sort_view = 'grade_desc'
    sort_by(app)

# Print the only names and grades of students who are below a certain total grade threshhold.
def view_failing(app,x='None'):
    # Get a minimum grade to compare from the user.
    min_grade_input = str(input("Please input a minimum grade threshold.\n>>>\t")).strip().lower()
    try:
        min_grade = float(min_grade_input)

        # Print the headers, and return their names and the total length.
        headers_and_length = print_headers(app)
        column_headers = headers_and_length[0]
        length = headers_and_length[1]

        # Get a sorted student list according to the current sorting view from sort_student_list.
        student_list = sort_student_list(app)

        # For each student in the list...
        for s in student_list:
            s_id = str(s['_id'])
            
            # Calculate their total grade with calculate_total_grade
            total_grade = calculate_total_grade(app,s_id)

            # If the total grade is less than the minimum grade, print the student's name and grade with print_student_grades.
            if total_grade < min_grade:
                print_student_grades(app,s,column_headers)

        # Print the final line of the table and a description of the information being shown. 
        print('-'*(len(length)+1)+'\n')

        print("Showing: Students with Total Grade below %i"%min_grade)

    except:
        # If the minimum grade is an exit command, return to sorting by last name alphabetical.
        if min_grade_input in exit_commands:
            sort_by_name(app)
        # Otherwise, print a short error message and start over.
        else:
            print("Sorry, that was not a valid grade input. Please try again.")
            view_failing(app)
    

# Calculate the mean grade out of all a given student's grades.
def calculate_total_grade(app,s_id):
    id_str = str(s_id)

    # Get all the assignments in the current course for which thist student has a recorded grade.
    grades = all_assignments.find({'CourseID':app.current_course, id_str: {'$exists': True}})

    # Set student_points and total_possible points to 0
    student_points = 0
    total_possible = 0

    # For each grade in the list, try to add both the student's grade and the assignment's total possible points to our variables. If the grade is not a number, do nothing.
    for x in grades:
        try:
            student_points += x[id_str]
            total_possible += x['Total Points']
        except TypeError:
            pass
    
    # If the total possible is not 0, calculate the percentage of the student's total grade, rounded to 2 decimal places.
    if total_possible != 0:
        result = round((student_points/total_possible)*100,1)
    # Otherwise, the student's grade is not calculable.
    else:
        result="N/A"

    # Update the student collection to indicate the student's current total grade in this course, and return the result.
    all_students.update_many({'_id':s_id},{'$set':{'Total Grade %s'%str(app.current_course):result}})

    return result


# Add a student to the course.
def add_student(app, y='None'):
    # Get a name input from the user.
    name = str(input("\nPlease enter the student's name.\n>>>\t")).strip()

    # If the input is an exit command, do nothing.
    if name.lower() in exit_commands:
        pass
    # Otherwise, search for that student using the find_or_create_student function.
    else:
        find_or_create_student(name,app.current_course)
    
    # Regardless, return to the Course Detail view.
    view_course(app)


# Add many students to the course at once.
def add_multiple_students(app,y='None'):
    # Create an empty list.
    new_students_list = []

    # Define finished commands.
    done_commands=['done','finished','complete','']

    # Print instructions.
    print('Input the name of each student on a new line. When finished, type "done" or press enter again.')

    # While inputting, allow the user to input names of students.
    inputting = True
    while inputting:
        name=str(input('>>>\t')).strip()
        # If the name is actually an exit command, stop inputting and break the loop.
        if name in exit_commands:
            inputting = False
            break

        # If the name is one of our done commands, add each student in our new student list to the course via find_or_create_student, stop inputting, and break the loop.
        elif name in done_commands:
            for s in new_students_list:
                find_or_create_student(s,app.current_course)
            inputting = False
            break

        # Otherwise, at the name to our list of new students.
        else:
            new_students_list.append(name)

    # View course details according to the current sort view.  
    sort_by(app)


# Edit the name of an existing student in the course.
def rename_student(app,y='None'):
    # Get input from the user for the student's old name.
    old_name = str(input("Please enter the name of the student you wish to edit.\n>>>\t")).strip()

    # Split the name into first and last names. If there is no last name, make it blank.
    name_split = old_name.split()

    old_first = name_split[0]
    try:
        old_last= name_split[1]
    except IndexError:
        old_last = ''

    # If more than two names were inputted, add the additional names to the last name.
    if len(name_split) > 2:
        for n in name_split[2:len(name_split)]:
            old_last += (' ' + n)

    # Get a list of all student ids which match the entered first and last name.
    target_student = [x for x in all_students.find({'First Name':old_first,'Last Name':old_last,'CourseID':app.current_course})]

    # If no students were found, check to see if the name was in our exit commands. If so, do nothing. Otherwise, print an error message and start over.
    if len(target_student) == 0:
        if old_name.lower() in exit_commands:
            view_course(app)
        else:
            print("\nSorry, no student of that name could be found in the current course. Please try again.")
            rename_student(app)
    
    # If more than one student with that name was found...
    elif len(target_student) > 1:
        print("There are %i students with that name found."%len(target_student))

        # Print each student's name and the courses they're currently enrolled in.
        for index, s in enumerate(target_student):
            print("%i: %s %s  -  Courses:\t"%(index,s['First Name'],s['Last Name']), end=' ')
            for c in s['CourseID']:
                student_courses = [x for x in courses.find({'_id':c})]
                print(student_courses[0]['Name'], end= ' ')
            print('')

        # Ask the user which student they're looking for, and assign a new name based on the student returned.    
        try:
            response = int(input("Which student would you like to select?\n>>>\t"))
            target_student = [target_student[response]]
            assign_new_student_name(app,old_name,target_student)

        # If the answer is not an integer or throws an IndexError, return to the Course Details View
        except :
            print("Sorry, that was not a valid answer. Please try again.")
            view_course(app)

    # Otherwise, get a new name for the student with the assign_new_student_name function.
    else:
        assign_new_student_name(app,old_name,target_student)


# Assign a new name to a given student based on their id.
def assign_new_student_name(app,old_name,target_student):
    # Get input from the user for a new name.
    new_name = str(input('Please enter the new name for "%s".\n>>>\t'%old_name)).strip()

    # Split the name into first and last names. If there is no last name, make it blank.
    name_split = new_name.split()
    new_first = name_split[0]
    try:
        new_last= name_split[1]
    except IndexError:
        new_last = ''

    # If there were more than 2 names given, add additional names to the last name.
    if len(name_split) > 2:
        for n in name_split[2:len(name_split)]:
            new_last += (' ' + n)


    # Check to see if the new name is in the list of exit commands. If so, do nothing.
    if new_name.lower() in exit_commands:
        pass

    # Otherwise, update the student collection to reflect this student's new name.
    else:
        all_students.update_one({'_id':target_student[0]['_id']},{'$set': {'First Name':new_first,'Last Name':new_last}})

    # Return to the course details view.
    view_course(app)


# Remove a student from the course.
def delete_student(app,y='None'):
    # Get the name of the current course.
    course_title = find_relevant(courses,'Name','_id',app.current_course)

    # Get input from the user for the student to be deleted.
    name = str(input("\nPlease enter the name of the student you wish to remove from the course.\n>>>\t")).strip()

    # Split the name into first and last names. If there is no last name, make it blank.
    name_split = name.split()
    first_name = name_split[0]

    try:
        last_name= name_split[1]
    except IndexError:
        last_name = ''

    # If more than 2 names were given, add any additional names to the last name.
    if len(name_split) > 2:
        for n in name_split[2:len(name_split)]:
            last_name += (' ' + n)

    # Get a list of all students who have that same first and last name and are enrolled in the current course.
    target_student = [x['_id'] for x in all_students.find({'First Name':first_name,'Last Name':last_name,'CourseID':app.current_course})]

    # If we didn't find any students, check to see if the name was an exit command. If so, do nothing. Otherwise, print an error message and start over.
    if len(target_student) == 0:
        if name.lower() in exit_commands:
            pass
        else:
            print("Sorry, no student of that name could be found in the current course. Please try again.")
            delete_student(app)
    
    # If we found the student, double-check with the user that they wish to unenroll the student.
    else:
        response = str(input("Are you sure you wish to delete %s and their grades for all assignments in this course?\n>>>\t"%name)).strip().lower()

        # If they say yes, remove the current course ID from their list of courses, remove their total grade in this course, and get rid of any grades they have in all assignments associated with the current course.
        if response in confirm_commands:
            all_students.update_one({'_id':target_student[0]},{'$pull': {'CourseID':app.current_course}})
            all_students.update_one({'_id':target_student[0]},{'$unset': {'Total Grade %s'%app.current_course:''}})
            all_assignments.update_many({'CourseID':app.current_course},{'$unset':{str(target_student[0]):""}})
            print("%s was successfully deleted from student list of %s."%(name,course_title[0]))
        # Otherwise, do nothing.
        else:
            pass

    # Regardless, return to the Course Details View
    view_course(app)


# Create the names of the column headers in our course table, and determine how wide the table will be.
def print_headers(app):
    # Create the basic headers for student name and total grade.
    column_headers = ['Student Name          ','Total Grade %']
    # Get the name of the current course.
    course_title = [x['Name'] for x in courses.find({'_id':app.current_course})]
    # Get a list of the names of all assignments associated with the current course, sorted by the date they are due.
    assignment_list = [a['Name'] for a in all_assignments.find({'CourseID':app.current_course}).sort('Date Due',1)]
    
    # Add assignment names to the column headers.
    column_headers += assignment_list

    # Calulate the number of characters in all the column headers.
    header_length = ''
    for e in column_headers:
        header_length += e + '|  '  
    
    # Print the title of the course and a line as long as the table is wide.
    print('\n'+course_title[0])
    print('-'*(len(header_length)+1))

    # Print each of the column names.
    for i in range(len(column_headers)):
        print('| %s'%column_headers[i], end =" ")
    print('|')

    # Print another line, and return the list of column headers and the total width of the table.
    print('|'+'-'*(len(header_length)-1)+'|')

    return (column_headers, header_length)


# Print the names and grades of a given student.
def print_student_grades(app,s,column_headers):
    s_id = s['_id']
    id_str = str(s_id)

    # Calculate the student's total grade in the class using the calculate_total_grade function, and get a string version as well.
    calculate_grade = calculate_total_grade(app, s_id)
    total_grade = str(calculate_grade)
    
    # Calculate how much blank space is needed to make the columns match up.
    name_space = len(column_headers[0])-(len(s['First Name'])+len(s['Last Name'])+1)+1
    grade_space = (len(column_headers[1])-len(total_grade))

    # Print the student's name and total grade.
    print('| '+ s['First Name'] + ' ' + s['Last Name'] + (' '*name_space)+'| '+ total_grade+(' '*grade_space), end=' ')

    # For each assignment associated with each student...
    for a in all_assignments.find({'CourseID':app.current_course}).sort('Date Due',1):
        # Try to find their grade for the given assignment.
        try:
            g = a[id_str]

            # If the grade is a None object, print a blank as long as the header.
            if g == None:
                print('|'+(' '*(len(a['Name'])+1)), end=' ')
            
            # If the grade is 0 or anything else...
            elif g == 0 or g:
                # Calculate the percentage grade based on the total points possible in the assignment.
                g_perc = str(float(g/a['Total Points'])*100.0)
                # Calculate how much blank spaces is necessary to make the columns match up, then print the grade and blank space.
                add = len(a['Name'])-len(g_perc)
                print('| '+g_perc+(' '*add), end=' ')
                
            # If there is no grade, print a blank as long as the header.
            else:
                print('|'+(' '*(len(a['Name'])+1)), end=' ')

        # If the student is not associated with this assignment, print a blank as long as the header.
        except KeyError:
            print('|'+(' '*(len(a['Name'])+1)), end=' ')
            
    # Print the final column line.
    print('|')