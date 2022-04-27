# ======================================
# DESCRIPTION
# ======================================
# This script defines most of the primary classes used by the program.


# ======================================
# IMPORT
# ======================================
from pymongo import *


# ======================================
# CONSTANTS
# ======================================
client = MongoClient()
db = client.grapple_database
courses = db.test_user_all_courses
all_assignments = db.test_user_all_assignments
all_students = db.test_user_all_students
all_grades = db.test_user_all_grades


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
    def __init__(self,name):
        self.name=name

# The Course class
class Course():
    def __init__(self, title):
        self.title = title

        course_label = title.lower().replace(' ','_')
        
        course_id = courses.insert_one({'Name':title}).inserted_id
