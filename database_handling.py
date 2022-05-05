# ======================================
# DESCRIPTION
# ======================================
# This script uses PyMongo to access the local MongoDB client and defines the primary database and major collections.


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
user_handler = db.test_user_handler
commands = db.commands_info