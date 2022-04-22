from classes import *

courses = [Course('Course 1'),Course('Course 2')]

# --- VIEW ALL COURSES ---

def all_courses():
    print('\nCourse Name:\n----------')
    i = 0
    while i < len(courses):
        print(courses[i].name)
        i+=1
    print('----------\n')

# --- EDIT COURSES ---
def add_course():
    course_title=str(input("\nPlease enter the name of the course you wish to add. >>>\t"))
    courses.append(Course(course_title))
    print("%s successfully added to course list.\n\n"%course_title)

def rename_course():
    pass

def delete_course():
    # This command should also delete/remove all assignments associated with the course.
    course_title=str(input("\nPlease enter the name of the course you wish to delete. >>>\t"))

    removed=[]
    for c in courses:
        if c.name == course_title:
            courses.remove(c)
            removed.append(c)
    
    if len(removed)==0:
        print ("\nSorry, no course of that name could be found. Please try again.\n\n")
    else:
        print ('\n%s successfully removed from course list.\n\n'%course_title)

# --- ASSIGNMENT COMMANDS ---

def add_assignment():
    course_title=str(input("\nPlease enter the name of the course. >>>\t"))

    added=[]
    for c in courses:
        if c.name == course_title:
            added.append(c)
    
    if len(added)==0:
        print ("Sorry, no course of that name could be found. Please try again.\n\n")
    else:
        assignment_title=str(input("\nPlease enter the name of the new assignment. >>>\t"))
        added[0].assignments.append(Assignment(assignment_title))
        print ('%s successfully added to %s.\n\n'%(assignment_title, course_title))

def rename_assignment():
    pass

def delete_assignment():
    pass