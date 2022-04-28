# ======================================
# DESCRIPTION
# ======================================
# This script defines all functions associated with setting and changing student grades.


# ======================================
# FUNCTIONS
# ======================================
import detail_course as dc
from classes import *

# Sets all students' grades in a given assignment.
def set_grade(app,y='None'):
    app.course_details = True
    assignment_title = str(input("Please enter the name of the assignment you wish to grade.\n>>>\t"))

    target_assignment=[x['_id'] for x in all_assignments.find({'CourseID':app.current_course, 'Name':assignment_title})]
    print(target_assignment)

    if len(target_assignment)==0:
        if assignment_title in app.exit_commands:
            pass
        else:
            print("Sorry, no assignment of that name could be found. Please try again.")
            set_grade(app)
    else:
        student_list = dc.sort_student_list(app)

        print('Student Name | %s '%assignment_title)    

        for s in student_list:
            name_length = len(s['First Name'])+len(s['Last Name'])+1
            try:
                grade=int(input(s['First Name']+ " " + s['Last Name'] +(" "*(len('Student Name ')-name_length)) + "| "))
            except ValueError:
                grade=None

            all_assignments.update_one({'_id':target_assignment[0]},{'$set':{str(s['_id']):grade}})

    dc.sort_by(app)

# Choose an assignment_title and show the list of all students and their grade in the assignment_title.
def view_grade(app,y='None'):
    app.course_details = True
    assignment_title = str(input("Please enter the name of the assignment you wish to view.\n>>>\t"))

    target_assignment=[x for x in all_assignments.find({'CourseID':app.current_course,'Name':assignment_title})]

    if len(target_assignment)==0:
        if assignment_title in app.exit_commands:
            dc.view_course(app)
        else:
            print("Sorry, no assignment of that name could be found. Please try again.")
            set_grade(app)
    else:
        student_list = dc.sort_student_list(app)

        print('Student Name | %s '%assignment_title)
        for s in student_list:
            s_id = str(s['_id'])
            print('| %s %s | %s |'%(s['First Name'],s['Last Name'],target_assignment[0][s_id]))

    return [assignment_title, target_assignment[0]['_id']]

# Edit a student's grade in a given assignment_title.
def tgt_student(app,assignment_title='None',assignment_id='None'):

    student_name = str(input("Which student's grade would you like to edit?\n>>>\t"))
    first_name = student_name.split()[0]
    try:
        last_name = student_name.split()[1]
    except IndexError:
        last_name = ''

    target_student = [x for x in all_students.find({'CourseID':app.current_course,'First Name':first_name, 'Last Name':last_name})]
    s = target_student[0]
    
    if len(target_student) ==0:
        if student_name in app.exit_commands:
            pass
        else:
            print("Sorry, no student with that name could be found. Please try again.")
            tgt_student(app)
    else:
        print('Student Name | %s '%assignment_title)
        name_length = len(s['First Name'])+len(s['Last Name'])+1
        try:
            grade=int(input(s['First Name']+ " " + s['Last Name'] +(" "*(len('Student Name ')-name_length)) + "| "))
        except ValueError:
            grade=None
        all_assignments.update_one({'_id':assignment_id},{'$set': {str(s['_id']):grade}})

    dc.view_course(app)

# View all grades in an assignment_title, and then edit a specific student's grade.
def edit_grade(app,y='None'):
    view_list = view_grade(app)

    if view_list[0] in app.exit_commands:
        dc.view_course(app)

    else:
        tgt_student(app,view_list[0],view_list[1])
