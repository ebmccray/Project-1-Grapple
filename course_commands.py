# ======================================
# DESCRIPTION
# ======================================
# This script defines the functions of the All Courses view, such as adding, renaming, and deleting courses.


# ======================================
# IMPORT PACKAGES
# ======================================
from classes import *
from database_handling import *
from configuration import *
import detail_course as dc
import menu_options


# ======================================
# FUNCTIONS
# ======================================

# Print a list of all courses.
def all_courses(app,y='None'):
    # Set the view variables to reflect the face that we are looking at the list of all courses.
    app.course_details = False
    app.view_all = True

    # Print the course names for each course in the courses collection.
    print('\nCourse Name:\n----------')
    for i in courses.find():
        print(i['Name'])
    print('----------\n')

    # Print a small menu with command options.
    print('Menu:\tNew Course\tRename Course\tDelete Course\tView Course')


# Add a course to the list of courses.
def add_course(app,y='None'):
    # Get a new title from the user.
    course_title=str(input("\nPlease enter the name of the course you wish to add.\n>>>\t")).strip()
    matching_courses = [x for x in courses.find({'Name':course_title})]

    # If it's one of our cancel command synonyms, go back to the All Courses View.
    if course_title.lower() in exit_commands:
        all_courses(app)

    # Otherwise, check to see if a course with that title already exists.
    elif len(matching_courses) > 0 :
        # Ask the user if they would like to view the course.
        response = str(input("%s already exists. Would you like to view this course?\n>>>\t"%course_title)).strip().lower()

        # If the response is yes, switch the EventHandler variables accordingly and set the current menu to the Course Details menu.
        if response in confirm_commands:
            app.current_course = matching_courses[0]['_id']
            app.current_menu = menu_options.course_details_menu
            app.course_details = True
            dc.view_course(app)

        # Otherwise, return to the All Courses view.   
        else:
            all_courses(app)

    # Otherwise, add the course to the list of courses, and inform the user this has occurred.
    else:
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
        if old_title.lower() in exit_commands:
            all_courses(app)
        # Otherwise, inform the user we couldn't find a target with that name and restart the command.
        else:
            print("\nSorry, no course of that name could be found. Please try again.")
            rename_course(app)

    # Otherwise, run the new_title function with our old title.
    else:
        new_title(app,old_title)


# Rename a given course.
def new_title(app, old_title='x'):
    # If we're editing the course name from the course details view, we use the current course as our target.
    if app.course_details:
        for x in courses.find({'_id':app.current_course}):
            old_title = x['Name']

    # Get a new title from the user.
    new_title = str(input('Please enter the new name for "%s".\n>>>\t'%old_title)).strip()

    # Check to see if the input is actually a back command.
    if new_title.lower() in exit_commands:
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
        if course_title.lower() in exit_commands:
            pass
        else:
            print ("\nSorry, no course of that name could be found. Please try again.\n")
            delete_course(app)

    # If we found the course, double check with the user to make sure they wish to delete the course..
    else:
        response = str(input("Are you sure you wish to delete %s and all associated assignments?\n>>>\t"%course_title)).strip()

        # If so, delete the course from the list of courses, delete all assignments associated with the course, pull the course out of all students' course lists, and remove all students' total grades in the course.
        if response.lower() in confirm_commands:
            deletion_criteria = {'CourseID':target_course[0]}
            courses.delete_one({'_id':target_course[0]})
            all_assignments.delete_many(deletion_criteria)
            all_students.update_many({},{'$pull': deletion_criteria})
            all_students.update_many({},{'$unset': {'Total Grade %s'%target_course[0]:''}})
            print ('\n%s and associated assignments successfully removed from course list.\n'%course_title)

        # Otherwise, do nothing.
        else:
            pass
    
    # Return to the All Courses View.
    all_courses(app)



    