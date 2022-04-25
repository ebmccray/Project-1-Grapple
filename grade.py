# ======================================
# FUNCTIONS
# ======================================
from asyncio.windows_events import NULL
import detail_course as dc

def set_grade(app,y='None'):
    assignment = str(input("Please enter the name of the assignment you wish to grade.\n>>>\t"))

    target=''

    for a in app.current_course.assignments:
        if a.name == assignment:
            target = a

    if target=='':
        if target in app.exit_commands:
            pass
        else:
            print("Sorry, no assignment of that name could be found. Please try again.")
            set_grade(app)
    else:
        print(' Student Name | %s '%assignment)
        for s in app.current_course.student_list:
            try:
                grade=input(" %s | "%s.name)
                s.grades[assignment]=grade
            except ValueError:
                s.grades[assignment]=NULL

    dc.view_course(app)

def edit_grade(app,y='None'):
    assignment = str(input("Please enter the name of the assignment you wish to grade.\n>>>\t"))

    target=''

    for a in app.current_course.assignments:
        if a.name == assignment:
            target = a

    if target=='':
        if target in app.exit_commands:
            dc.view_course(app)
        else:
            print("Sorry, no assignment of that name could be found. Please try again.")
            set_grade(app)
    else:
        print(' Student Name | %s '%assignment)
        for s in app.current_course.student_list:
            print('| %s | %i |'%(s.name,s.grades[assignment]))
        tgt_student(app,assignment)

def tgt_student(app,assignment='None'):

    student_name = str(input("Which student's grade would you like to edit?\n>>>\t"))

    target_student = ''
    
    for s in app.current_course.student_list:
        if s.name==student_name:
            target_student = s
    
    if target_student =='':
        if target_student in app.exit_commands:
            pass
        else:
            print("Sorry, no student with that name could be found. Please try again.")
            tgt_student(app)
    else:
        print(' Student Name | %s '%assignment)
        try:
            grade=int(input(" %s | "%target_student.name))
            target_student.grades[assignment]=grade
        except ValueError:
            target_student.grades[assignment]=NULL

    dc.view_course(app)