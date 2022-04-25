# ======================================
# IMPORT PACKAGES
# ======================================
from classes import *
import detail_course as dc


# ======================================
# FUNCTIONS
# ======================================
def all_courses(app,y='None'):
    app.course_details = False
    app.view_all = True
    print('\nCourse Name:\n----------')
    i = 0
    while i < len(app.courses):
        print(app.courses[i].name)
        i+=1
    print('----------\n')

def add_course(app,y='None'):
    course_title=str(input("\nPlease enter the name of the course you wish to add.\n>>>\t"))
    if course_title.lower() in app.exit_commands:
        pass
    else:
        app.courses.append(Course(course_title))
        print("%s successfully added to course list.\n"%course_title)
    all_courses(app)

def rename_course(app,y='None'):
    old_name = str(input("Please enter the name of the course you wish to edit.\n>>>\t"))
    target =''
    for c in app.courses:
        if c.name == old_name:
            target=c

    if target =='':
        if old_name.lower() in app.exit_commands:
            all_courses(app)
        else:
            print("\nSorry, no course of that name could be found. Please try again.")
            rename_course(app)
    else:
        new_name(app,target,old_name)

def new_name(app,target='x',old_name='x'):
    if app.course_details:
        target=app.current_course
        old_name = app.current_course.name

    new_name = str(input('Please enter the new name for "%s".\n>>>\t'%old_name))

    if old_name.lower() in app.exit_commands:
        pass
    else:
        target.name = new_name
    if app.view_all:
        all_courses(app)
    elif app.course_details:
        dc.view_course(app)
    else:
        print("Sorry, there was an error.")
        all_courses(app)
    

def delete_course(app,y='None'):
    course_title=str(input("\nPlease enter the name of the course you wish to delete.\n>>>\t"))

    removed=[]
    for c in app.courses:
        if c.name == course_title:
            app.courses.remove(c)
            removed.append(c)
    
    if len(removed)==0:
        if course_title.lower() in app.exit_commands:
            pass
        else:
            print ("\nSorry, no course of that name could be found. Please try again.\n")
            delete_course(app)
    else:
        print ('\n%s successfully removed from course list.\n'%course_title)
    
    all_courses(app)