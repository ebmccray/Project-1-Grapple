# ======================================
# DESCRIPTION
# ======================================
# This script defines most of the primary classes used by the program, and also defines several of the MongoDB databases.


# ======================================
# IMPORT
# ======================================
from pymongo import *


# ======================================
# DATABASE CONFIGURATION
# ======================================
client = MongoClient()
db = client.grapple_database
courses = db.test_user_all_courses
all_assignments = db.test_user_all_assignments
all_students = db.test_user_all_students


# ======================================
# CLASSES
# ======================================

# The Assignment class.
class Assignment():
    def __init__(self,title,courseID):
        self.title=title
        all_assignments.insert_one({'Name':title,'CourseID':courseID})

# The Student class
class Student():
    def __init__(self,first_name, last_name,course_id):
        self.name = first_name + last_name

        all_students.insert_one({'First Name':first_name, 'Last Name':last_name,'CourseID':[course_id]})


# The Course class
class Course():
    def __init__(self, title):
        self.title = title
        
        courses.insert_one({'Name':title}).inserted_id


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


def find_or_create_student(name,course_id):
    first_name = name.split()[0]
    try:
        last_name= name.split()[1]
    except IndexError:
        last_name = ''

    enroll_commands = ['enroll','enroll_this','this_student','enroll_student','this_one','this',name]
    new_commands = ['new','create','create_new','enroll_new','create_student','new_student','create_new_student','add_student','add_new_student','enroll_new_student']

    my_student = [x['_id'] for x in all_students.find({'First Name':first_name, 'Last Name':last_name})]

    if len(my_student)== 0:
        Student(first_name, last_name, course_id)
    else:
        response = str(input('A student named "%s" already exists in the student database.\nWould you like to enroll this student, or create a new student?\n>>>\t'%name)).lower().replace(' ','_')
        if response in enroll_commands:
            all_students.update_many({'_id':my_student[0]},{'$push':{'CourseID':course_id}})
        elif response in new_commands:
            Student(first_name, last_name,course_id)
        else:
            pass