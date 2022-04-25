# ======================================
# IMPORT PACKAGES
# ======================================
from classes import *


# ======================================
# FUNCTIONS
# ======================================
def switch_course(app,y='None'):
    course=str(input("\nPlease enter the name of the course.\n>>>\t"))

    my_course=''
    for c in app.courses:
        if c.name==course:
            my_course=c

    if my_course =='':
        if course.lower() in app.exit_commands:
            app.view_courses_menu['view_all'](app)
            app.current_menu = app.view_courses_menu
            app.course_details = False
        else:
            print ("\nSorry, no course of that name could be found. Please try again.")
            switch_course(app)
    
    else:
        app.course_details=True
        app.current_course = my_course
        view_course(app)

def view_course(app, y='None'):
    app.view_all = False

    if app.course_details:
        

        x = ['Student Name          ']
        ass = []
        for a in app.current_course.assignments:
            ass.append(a.name)
        
        x += ass

        j = ''
        for e in x:
            j += e+'|  '
        
        print('\n'+app.current_course.name)
        print('-'*(len(j)+1))

        for i in range(len(x)):
            print('| %s'%x[i], end =" ")
        print('|')

        print('|'+'-'*(len(j)-1)+'|')

        for s in app.current_course.student_list:
            space = (len(x[0])-len(s.name))

            print('| '+ s.name + (' '*space), end=' ')

            for a in ass:
                try:
                    g = str(s.grades[a])
                    add = len(a)-len(g)
                    print('| '+g+(' '*add), end=' ')
                except KeyError:
                    print('|'+(' '*(len(a)+1)), end=' ')
            print('|')
        
        print('-'*(len(j)+1)+'\n')
    else:
        switch_course(app)


def add_assignment(app,y='None'):
    assignment_title=str(input("\nPlease enter the name of the new assignment.\n>>>\t"))

    if assignment_title.lower() in app.exit_commands:
        pass  
    else:
        app.current_course.assignments.append(Assignment(assignment_title))
        print ('%s successfully added to %s.\n'%(assignment_title, app.current_course.name))

    view_course(app)

def rename_assignment(app,y='None'):
    old_name = str(input("Please enter the name of the assignment you wish to edit.\n>>>\t"))
    target =''
    for c in app.current_course.assignments:
        if c.name == old_name:
            target=c

    if target =='':
        if old_name.lower() in app.exit_commands:
            pass
        else:
            print("\nSorry, no assignment of that name could be found in the current course. Please try again.")
            rename_assignment(app)
    else:
        new_name = str(input('Please enter the new name for "%s".\n>>>\t'%old_name))
        if new_name.lower() in app.exit_commands:
            pass
        else:
            target.name = new_name
    view_course(app)

def delete_assignment(app,y='None'):
    title = str(input("\nPlease enter the name of the assignment you wish to delete.\n>>>\t"))

    target = ''
    for c in app.current_course.assignments:
        if c.name == title:
            target=c

    if target =='':
        if title.lower() in app.exit_commands:
            pass
        else:
            print("Sorry, no assignment of that name could be found. Please try again.")
            delete_assignment(app)
    else:
        app.current_course.assignments.remove(target)
        print("%s was successfully deleted from the assignment list of %s."%(title,app.current_course.name))

    view_course(app)

def add_student(app, y='None'):
    name= str(input("\nPlease enter the student's name.\n>>>\t"))

    if name.lower() in app.exit_commands:
        pass
    else:
        app.current_course.student_list.append(Student(name))
    
    view_course(app)

def rename_student(app,y='None'):
    old_name = str(input("Please enter the name of the student you wish to edit.\n>>>\t"))
    target =''
    for c in app.current_course.student_list:
        if c.name == old_name:
            target=c

    if target =='':
        if old_name.lower() in app.exit_commands:
            pass
        else:
            print("\nSorry, no student of that name could be found in the current course. Please try again.")
            rename_student(app)
    else:
        new_name = str(input('Please enter the new name for "%s".\n>>>\t'%old_name))
        if new_name.lower() in app.exit_commands:
            pass
        else:
            target.name = new_name
    view_course(app)

def delete_student(app,y='None'):
    name = str(input("\nPlease enter the name of the student you wish to remove from the course.\n>>>\t"))

    target = ''
    for c in app.current_course.student_list:
        if c.name == name:
            target=c

    if target =='':
        if name.lower() in app.exit_commands:
            pass
        else:
            print("Sorry, no student of that name could be found in the current course. Please try again.")
            delete_student(app)
    else:
        app.current_course.student_list.remove(target)
        print("%s was successfully deleted from student list of %s."%(name,app.current_course.name))

    view_course(app)