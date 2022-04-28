# ======================================
# DESCRIPTION
# ======================================
# This script defines the functions of the Course Details View, such as seeing all students and assignments, editing, adding, and removing assignments, and editing, adding, and removing students.


# ======================================
# IMPORT PACKAGES
# ======================================
from classes import *


# ======================================
# FUNCTIONS
# ======================================

# Choose which course to view the details of.
def switch_course(app,y='None'):
    # Get course title from the user.
    course_title=str(input("\nPlease enter the name of the course.\n>>>\t"))

    # Find the corresponding Course object, if it exists in the course list.
    target_course = find_relevant(courses,'_id','Name',course_title)

    # If we did not find the course object, check to see if the command was one of our exit or back commands.
    if len(target_course) == 0:
        # If so, return to the All Courses View and reset the view and menu variables in the Event Handler.
        if course_title.lower() in app.exit_commands:
            app.view_courses_menu['view_all'](app)
            app.current_menu = app.view_courses_menu
            app.course_details = False

        # Otherwise, inform the user their Course could not be found.
        else:
            print ("\nSorry, no course of that name could be found. Please try again.")
            switch_course(app)
    
    else:
        # Set view variables and change the current course in the Event Handler, then run the view_course function.
        app.course_details=True
        app.current_course = target_course[0]
        view_course(app)


# View the Students, Assignments, and Grades associated with the currently-selected course.
def view_course(app, y='None'):
    # Set the view variables.
    app.view_all = False

    # If we've already selected a course, display the details associated with it.
    if app.course_details:
        sort_by(app)

    # Otherwise, run the switch_course function to choose a course to view.
    else:
        switch_course(app)

def sort_student_list(app, y='None'):
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

    student_list = [x for x in all_students.find({'CourseID':app.current_course}).sort(criteria,i)]

    return student_list

def sort_by(app, y='None'):
    headers_and_length = print_headers(app)
    column_headers = headers_and_length[0]
    header_length = headers_and_length[1]

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

    # For each student in the course list...
    student_list = sort_student_list(app)

    for s in student_list:
        print_student_grades(app,s,column_headers)
    print('-'*(len(header_length)+1)+'\n')

    print('Showing: All students by %s.'%descriptor)

def sort_by_name(app, y = 'None'):
    app.sort_view = 'last_name_asc'
    sort_by(app)

def sort_by_grade(app, y='None',i=1):
    app.sort_view = 'grade_asc'
    sort_by(app)

def sort_by_grade_descending(app,y='None'):
    app.sort_view = 'grade_desc'
    sort_by(app)

def sort_reverse_alphabetical(app,y='None',i=1):
    app.sort_view = 'last_name_desc'
    sort_by(app)

def view_failing(app,x='None'):
    min_grade = float(input("Please input a minimum grade threshold.\n>>>\t"))

    headers_and_length = print_headers(app)
    column_headers = headers_and_length[0]
    length = headers_and_length[1]

    student_list = sort_student_list(app)

    for s in student_list:
        s_id = str(s['_id'])
        
        total_grade = calculate_total_grade(app,s_id)

        if total_grade < min_grade:
            print_student_grades(app,s,column_headers)

    print('-'*(len(length)+1)+'\n')

    print("Showing: Students with Total Grade below %i"%min_grade)
    

# Calculate the mean grade out of all a given student's grades.
def calculate_total_grade(app,s_id):
    id_str = str(s_id)
    grades = all_assignments.find({'CourseID':app.current_course, id_str: {'$exists': True}})
    overall = 0
    counted = 0
    for x in grades:
        try:
            overall += x[id_str]
            counted += 1
        except TypeError:
            pass
    
    if counted != 0:
        result = round((overall/counted),2)

    else:
        result="N/A"

    all_students.update_many({'_id':s_id},{'$set':{'Total Grade %s'%str(app.current_course):result}})

    return result


# Add an assignment to the list of assignments in the course.
def add_assignment(app,y='None'):
    course_title = find_relevant(courses,'Name','_id',app.current_course)
    # Get a title input from the user.
    assignment_title=str(input("\nPlease enter the name of the new assignment.\n>>>\t"))

    # Check to see if the input is one of our exit commands.
    if assignment_title.lower() in app.exit_commands:
        pass  
    # Otherwise, add the assignment to the list of all assignments in the course and inform the user we have done so.
    else:
        Assignment(assignment_title, app.current_course)
        print ('%s successfully added to %s.\n'%(assignment_title,course_title[0]))

    view_course(app)



# Rename an existing assignment in the course.
def rename_assignment(app,y='None'):
    # Get title input from the user.
    old_title = str(input("Please enter the name of the assignment you wish to edit.\n>>>\t"))

    # Search for a corresponding Assignment object, if it exists in our current course list.
    target_assignment =[x for x in all_assignments.find({'CourseID':app.current_course,'Name':old_title})]

    # If we didn't find an Assignment, check to see if it was actually a back command, and go back if it was. Otherwise, print an error and restart.
    if len(target_assignment) == 0:
        if old_title.lower() in app.exit_commands:
            pass
        else:
            print("\nSorry, no assignment of that name could be found in the current course. Please try again.")
            rename_assignment(app)

    # If we found an Assignment, get input from the user for the new title.
    else:
        new_title = str(input('Please enter the new name for "%s".\n>>>\t'%old_title))
        # Check to see if the input is one of the back commands.
        if new_title.lower() in app.exit_commands:
            pass
        # Otherwise, add the new assignment to student's grades, as a copy of the old grades. Get rid of the old grades, and give a new title to the Assignment object.
        else:
            all_assignments.update_one({'Name':old_title},{'$set':{'Name':new_title}})
    view_course(app)


# Remove an assignment from the course.
def delete_assignment(app,y='None'):
    course_title = find_relevant(courses,'Name','_id',app.current_course)
    # Get title input from the user.
    title = str(input("\nPlease enter the name of the assignment you wish to delete.\n>>>\t"))

    # Search for a corresponding Assignment object, if it exists in our current course list.
    target_assignment =[x['_id'] for x in all_assignments.find({'CourseID':app.current_course, 'Name':title})]

    # If we didn't find an Assignment, check to see if it was actually a back command, and go back if it was. Otherwise, print an error and restart.
    if len(target_assignment) ==0:
        if title.lower() in app.exit_commands:
            pass
        else:
            print("Sorry, no assignment of that name could be found. Please try again.")
            delete_assignment(app)
    # Otherwise, remove the Target Assignment from the list of courses and inform the user we have done so.
    else:
        all_assignments.delete_one({'_id':target_assignment[0]})
        print("%s was successfully deleted from the assignment list of %s."%(title,course_title[0]))

    view_course(app)


# Add a student to the course.
def add_student(app, y='None'):
    name = str(input("\nPlease enter the student's name.\n>>>\t"))

    if name.lower() in app.exit_commands:
        pass
    else:
        find_or_create_student(name,app.current_course)
    
    view_course(app)


def add_multiple_students(app,y='None'):
    new_students_list = []
    done_commands=['done','finished','complete','']
    print('Input the name of each student on a new line. When finished, type "done" or press enter again.')
    inputting = True
    while inputting:
        name=str(input('>>>\t'))
        if name in app.exit_commands:
            inputting = False
            break
        elif name in done_commands:
            for s in new_students_list:
                find_or_create_student(s,app.current_course)
            inputting = False
            break
        else:
            new_students_list.append(name)
    sort_by(app)


# Edit the name of an existing student in the course.
def rename_student(app,y='None'):
    old_name = str(input("Please enter the name of the student you wish to edit.\n>>>\t"))
    old_first = old_name.split()[0]
    try:
        old_last= old_name.split()[1]
    except IndexError:
        old_last = ''
    target_student = [x['_id'] for x in all_students.find({'First Name':old_first,'Last Name':old_last})]

    if len(target_student) == 0:
        if old_name.lower() in app.exit_commands:
            pass
        else:
            print("\nSorry, no student of that name could be found in the current course. Please try again.")
            rename_student(app)
    else:
        new_name = str(input('Please enter the new name for "%s".\n>>>\t'%old_name))
        new_first = new_name.split()[0]
        try:
            new_last= new_name.split()[1]
        except IndexError:
            new_last = ''
        if new_name.lower() in app.exit_commands:
            pass
        else:
            all_students.update_one({'_id':target_student[0]},{'$set': {'First Name':new_first,'Last Name':new_last}})
    view_course(app)


# Remove a student from the course.
def delete_student(app,y='None'):
    course_title = find_relevant(courses,'Name','_id',app.current_course)
    name = str(input("\nPlease enter the name of the student you wish to remove from the course.\n>>>\t"))
    first_name = name.split()[0]
    try:
        last_name= name.split()[1]
    except IndexError:
        last_name = ''

    target_student = [x['_id'] for x in all_students.find({'First Name':first_name,'Last Name':last_name})]

    if len(target_student) == 0:
        if name.lower() in app.exit_commands:
            pass
        else:
            print("Sorry, no student of that name could be found in the current course. Please try again.")
            delete_student(app)
    else:
        all_students.update_one({'_id':target_student[0]},{'$pull': {'CourseID':app.current_course}})
        all_assignments.update_many({},{'$unset':{str(target_student[0]):""}})
        print("%s was successfully deleted from student list of %s."%(name,course_title[0]))

    view_course(app)

def print_headers(app):
    # Create the names of the column headers in our table, and determine how wide the table will be.
    column_headers = ['Student Name          ','Total Grade']
    course_title = [x['Name'] for x in courses.find({'_id':app.current_course})]
    assignment_list = [a['Name'] for a in all_assignments.find({'CourseID':app.current_course})]
    
    column_headers += assignment_list

    header_length = ''
    for e in column_headers:
        header_length += e+'|  '
    
    # Print the title of the course.
    print('\n'+course_title[0])
    print('-'*(len(header_length)+1))

    # Print each of the column names.
    for i in range(len(column_headers)):
        print('| %s'%column_headers[i], end =" ")
    print('|')

    print('|'+'-'*(len(header_length)-1)+'|')

    return (column_headers, header_length)


def print_student_grades(app,s,column_headers):
    s_id = s['_id']
    id_str = str(s_id)

    # Print the student's name and total grade.
    name_space = len(column_headers[0])-(len(s['First Name'])+len(s['Last Name'])+1)+1
    calculate_grade = calculate_total_grade(app, s_id)
    total_grade = str(calculate_grade)
    grade_space = (len(column_headers[1])-len(total_grade))

    print('| '+ s['First Name'] + ' ' + s['Last Name'] + (' '*name_space)+'| '+ total_grade+(' '*grade_space), end=' ')

    # For each assignment associated with each student...
    for a in all_assignments.find({'CourseID':app.current_course}):
        # Try to find their grade for the given assignment, and print it as a string.
        try:
            g = str(a[id_str])

            if g:
                add = len(a['Name'])-len(g)
                print('| '+g+(' '*add), end=' ')
                
            else:
                print('|'+(' '*(len(a['Name'])+1)), end=' ')
        except KeyError:
            print('|'+(' '*(len(a['Name'])+1)), end=' ')

    print('|')