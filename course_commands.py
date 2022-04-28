# ======================================
# DESCRIPTION
# ======================================
# This script defines all the commands in the All Courses Menu and View, such as adding, renaming, and deleting courses.


# ======================================
# IMPORT PACKAGES
# ======================================
from classes import *
import detail_course as dc

# ======================================
# FUNCTIONS
# ======================================

# Print a list of all courses.
def all_courses(app,y='None'):
    # Set the view variables.
    app.course_details = False
    app.view_all = True

    # Print a list of all the course names.
    print('\nCourse Name:\n----------')
    for i in courses.find():
        print(i['Name'])
    print('----------\n')

# Add a course to the list of courses.
def add_course(app,y='None'):
    # Get a new title from the user.
    course_title=str(input("\nPlease enter the name of the course you wish to add.\n>>>\t"))

    # If it's one of our cancel comman synonyms, go back to the All Courses View.
    if course_title.lower() in app.exit_commands:
        pass
    # Otherwise, add the course to the list of courses, and inform the user this has occurred.
    else:
        course_title = course_title.strip()
        Course(course_title)

        print("%s successfully added to course list.\n"%course_title)

    all_courses(app)

# Rename a course already in the list of courses, and pass it to the new name function.
def rename_course(app,y='None'):
    # Get the old title from the user.
    old_title = str(input("Please enter the name of the course you wish to edit.\n>>>\t")).strip()

    # Find the Course object corresponding to our title, if it exists in our course list.
    target_course = find_relevant(courses,criteria_field='Name',search_criteria=old_title)

    # If there is no such course in the course list, check to see if the command was a back or exit command.
    if len(target_course) == 0:
        # If so, return to All Courses View.
        if old_title.lower() in app.exit_commands:
            all_courses(app)
        # Otherwise, inform the user we couldn't find a target with that name.
        else:
            print("\nSorry, no course of that name could be found. Please try again.")
            rename_course(app)

    # Otherwise, run the new_title function with our target course and old title.
    else:
        new_title(app,old_title)

# Rename a given course.
def new_title(app, old_title='x'):
    # If we're editing the course name from the course details view, we use the current course as our target.
    if app.course_details:
        for x in courses.find({'_id':app.current_course}):
            old_title = x['Name']

    # Get a new title from the user.
    new_title = str(input('Please enter the new name for "%s".\n>>>\t'%old_title))

    # Check to see if the input is actually a back command.
    if new_title.lower() in app.exit_commands:
        pass
    # Otherwise, set the course's title to the new title.
    else:
        new_title = new_title.strip()
        courses.update_one({'Name':old_title},{'$set': {'Name':new_title}})
    
    # If we were in the All Courses View, return to that.
    if app.view_all:
        all_courses(app)
    # Otherwise, if we were in the Course Details view, return to that.
    elif app.course_details:
        dc.view_course(app)
    # Otherwise, print a short error message and go to All Courses view.
    else:
        print("Sorry, there was an error.")
        all_courses(app)
    
# Remove a course from the list of courses.
def delete_course(app,y='None'):
    # Get the title of the course from the user.
    course_title=str(input("\nPlease enter the name of the course you wish to delete.\n>>>\t")).strip()

    # Find the Course object corresponding to our title, if it exists in our course list.
    target_course = find_relevant(courses,'_id','Name',course_title)
    
    # If we did not find any such title, check to see if it was a back command. Otherwise, print an error message.
    if len(target_course)==0:
        if course_title.lower() in app.exit_commands:
            pass
        else:
            print ("\nSorry, no course of that name could be found. Please try again.\n")
            delete_course(app)

    # If we found the course, remove it from the list of courses. The inform the user we've done so.
    else:
        response = str(input("Are you sure you wish to delete %s and all associated assignments?\n>>>\t"%course_title))
        if response.lower() in app.confirm_commands:
            deletion_criteria = {'CourseID':target_course[0]}
            courses.delete_one({'_id':target_course[0]})
            all_assignments.delete_many(deletion_criteria)
            all_students.update_many({},{'$pull': deletion_criteria})
            print ('\n%s and associated assignments successfully removed from course list.\n'%course_title)
        else:
            pass
    
    # Return to the All Courses View.
    all_courses(app)

def view_specific_course(app,course_name):
    
    target_course = [x['_id'] for x in courses.find({'Name':course_name})]
    try:
        app.current_course = target_course[0]
        app.course_details = True
        result = True
    except IndexError:
        result = False
    
    return result

    