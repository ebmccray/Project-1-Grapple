# ======================================
# FUNCTIONS
# ======================================

def main_help(app,y='None'):
    app.course_details = False
    app.view_all = False
    print('''\nGet help with:\n\tCourses View\n\tCourse Detail View\n''')

def course_help(app,y='None'):
    print('''\n\nHere are some common Course View commands:
\tcourses:\tView a list of all your currently available courses.
\tadd course:\tAdds a new course to your list of courses.
\trename course:\tTakes an existing course and renames it.
\tdelete course:\tDeletes a course from your list of courses.
\tview course:\tOpens a detail view of the course, students, assignments, and grades.''')
    if app.current_menu != app.help_menu_actions:
        app.prev_menu = app.current_menu

def assignment_help(x='None',y='None'):
    pass