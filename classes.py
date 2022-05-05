# ======================================
# DESCRIPTION
# ======================================
# This script defines most of the primary classes used by the program, and also defines several of the MongoDB databases.


# ======================================
# IMPORT
# ======================================
from database_handling import *

# ======================================
# CLASSES
# ======================================

# The Assignment class.
class Assignment():
    def __init__(self,title,courseID,points,assigned_date):
        self.title=title
        # Upon creation of the class, insert the assignment into the list of all assignments.
        all_assignments.insert_one({'Name':title,'CourseID':courseID,'Total Points':points,'Date Due':str(assigned_date)})

# The Student class
class Student():
    def __init__(self,first_name, last_name,course_id):
        self.name = first_name + last_name
        # Upon creation of the class, insert the student into the list of all students.
        all_students.insert_one({'First Name':first_name, 'Last Name':last_name,'CourseID':[course_id]})


# The Course class
class Course():
    def __init__(self, title):
        self.title = title
        # Upon creation of the class, insert the course into the list of all courses.
        courses.insert_one({'Name':title}).inserted_id


# Find a list based off the given criteria, and return that list.
def find_relevant(database, get_field='', criteria_field='', search_criteria=''):
    if criteria_field == '':
        if get_field=='':
            relevant_list = [x for x in database.find()]
        else:
            relevant_list = [x[get_field] for x in database.find()]
    else:
        if get_field=='':
            relevant_list = [x for x in database.find({criteria_field:search_criteria})]
        else:
            relevant_list = [x[get_field] for x in database.find({criteria_field:search_criteria})]
    return relevant_list


# Look for a student in the all students collection, or create a new one if no such student exists.
def find_or_create_student(name,course_id):
    # Split the name entry into first and last names - if there is only one name, make the last name blank.
    split_names = name.split()
    first_name = name.split()[0]
    try:
        last_name= name.split()[1]
    except IndexError:
        last_name = ''
    
    if len(split_names) > 2:
        for n in split_names[2:len(split_names)]:
            last_name += (' ' + n)

    # Define lists of commands and command synonyms.
    enroll_commands = ['enroll','enroll_this','this_student','enroll_student','this_one','this',name]
    new_commands = ['new','create','create_new','enroll_new','create_student','new_student','create_new_student','add_student','add_new_student','enroll_new_student']

    # Get a list of all student ids with the same first and last names as our inputted name.
    my_student = [x['_id'] for x in all_students.find({'First Name':first_name, 'Last Name':last_name})]

    # If no such student exists, create a new student with the given first and last name.
    if len(my_student)== 0:
        Student(first_name, last_name, course_id)

    # Otherwise, inform the user that a student with that name already exists, and as if they would like to add that student, or create a new student with the same name.
    else:
        response = str(input('A student named "%s" already exists in the student database.\nWould you like to enroll this student, or create a new student?\n>>>\t'%name)).lower().replace(' ','_')
        # If they say they want to enroll that student, add the current course id to that student's list of ids.
        if response in enroll_commands:
            all_students.update_many({'_id':my_student[0]},{'$push':{'CourseID':course_id}})
        # If they say they want to create a new student, create a new student with the given first and last name.
        elif response in new_commands:
            Student(first_name, last_name,course_id)
        # If the response is not in either command list, do nothing.
        else:
            pass