# ======================================
# DESCRIPTION
# ======================================
# This script defines all functions associated with setting and changing student grades.


# ======================================
# FUNCTIONS
# ======================================
import detail_course as dc

# Sets all students' grades in a given assignment.
def set_grade(app,y='None'):
    assignment_title = str(input("Please enter the name of the assignment you wish to grade.\n>>>\t"))

    target_assignment=[x for x in app.current_course.assignments if x.title == assignment_title]

    if len(target_assignment)==0:
        if assignment_title in app.exit_commands:
            pass
        else:
            print("Sorry, no assignment of that name could be found. Please try again.")
            set_grade(app)
    else:
        print(' Student Name | %s '%assignment_title)
        for s in app.current_course.student_list:
            try:
                grade=int(input(" %s | "%s.name))
            except ValueError:
                grade=None
            s.grades[assignment_title]=grade

    dc.view_course(app)

# Choose an assignment_title and show the list of all students and their grade in the assignment_title.
def view_grade(app,y='None'):
    assignment_title = str(input("Please enter the name of the assignment you wish to view.\n>>>\t"))

    target_assignment=[x for x in app.current_course.assignments if x.title == assignment_title]

    if len(target_assignment)==0:
        if assignment_title in app.exit_commands:
            dc.view_course(app)
        else:
            print("Sorry, no assignment of that name could be found. Please try again.")
            set_grade(app)
    else:
        print(' Student Name | %s '%assignment_title)
        for s in app.current_course.student_list:
            print('| %s | %i |'%(s.name,s.grades[assignment_title]))

    return assignment_title

# Edit a student's grade in a given assignment_title.
def tgt_student(app,assignment_title='None'):

    student_name = str(input("Which student's grade would you like to edit?\n>>>\t"))

    target_student = [x for x in app.current_course.student_list if x.name == student_name]
    
    if len(target_student) ==0:
        if student_name in app.exit_commands:
            pass
        else:
            print("Sorry, no student with that name could be found. Please try again.")
            tgt_student(app)
    else:
        print(' Student Name | %s '%assignment_title)
        try:
            grade=int(input(" %s | "%target_student[0].name))
        except ValueError:
            grade=None
        target_student[0].grades[assignment_title]=grade

    dc.view_course(app)

# View all grades in an assignment_title, and then edit a specific student's grade.
def edit_grade(app,y='None'):
    assignment_title = view_grade(app)

    if assignment_title in app.exit_commands:
        dc.view_course(app)

    else:
        tgt_student(app,assignment_title)
