# ======================================
# DESCRIPTION
# ======================================
# This script defines the functions of the help menu, as well as defining the help messages.

# ======================================
# IMPORT
# ======================================
import configuration as config

# ======================================
# HELP MESSAGES
# ======================================
help_message = '''\nGet help with:\n\tAll Courses View\n\tCourse Detail View\n\tApp Info
If you need additional help, please see the README document or contact the creator with your questions.'''

course_message = '''\nThe All Courses view shows a list of all your courses.
Here are some common All Courses View commands:
\tcourses:\tView a list of all your currently available courses.
\tadd course:\tAdds a new course to your list of courses.
\trename course:\tChanges the name of an existing course.
\tdelete course:\tDeletes a course from your list of courses.
\tview course:\tOpens a detail view of the course, students, assignments, and grades.
Press enter to return.'''

course_detail_message = '''\n The Course Detail View shows the students and assignments currently in the course.
Here are some common Course Detail View commands:
\tswitch course:\t\tChanges your view to a different course.
\tview failing:\t\tShows only students whose total grade is below a minimum threshold.
\trename course:\t\tChanges the name of the course you are currently viewing.
\tadd assignment:\t\tAdds an assignment to your course.
\trename assignment:\tChanges the name of an existing assignment.
\tdelete assignment:\tRemoves an assignment from the current course.
\tadd student:\t\tAdds a new student to the current course.
\trename student:\t\tChange the name of an existing student in the current course.
\tremove student:\t\tRemove a student from the current course.
\tenter grades:\t\tEnter the grades for all students in a given assignment.
\tedit grade:\t\tChange or enter a grade for a specific student in a given assignment.
Press enter to return.'''

info_message = "%s"%config.app_copyright

# ======================================
# FUNCTIONS
# ======================================

def main_help(app,y='None'):
    app.course_details = False
    app.view_all = False
    print(help_message)

def course_help(app,y='None'):
    print(course_message)

def course_detail_help(app,y='None'):
    print(course_detail_message)

def app_info(app,y='None'):
    print(info_message)