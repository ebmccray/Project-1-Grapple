# ======================================
# IMPORT
# ======================================
from pymongo import *

client = MongoClient()

db = client.grapple_database

courses = db.course_collection
students = db.student_collection