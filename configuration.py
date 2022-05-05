# ======================================
# DESCRIPTION
# ======================================
# This script defines basic configuration variables for the app, such as its name, creator, and other information.
# It also defines some universally-used variables, such as the lists of command synonyms.

# ======================================
# CONFIGURATION VARIABLES
# ======================================
app_name = "Grapple"
app_copyright="Created in 2022 Erienne McCray, employee of Revature."


# ======================================
# COMMAND SYNONYMS
# ======================================

exit_commands = ['quit','cancel','back','exit','return','escape','none']
back_commands=['back','return','previous']
confirm_commands=['yes','y','true']
command_synonyms=[
    ['view_all','all_courses','my_courses','view_courses','all_courses_view','view_all_courses', 'courses'],
    ['add_course','new_course','add_new_course','create_course'],
    ['rename_course','change_course_name','change_course'],
    ['delete_course','remove_course','drop_course'],
    ['view_course','view_details','edit_course','course_details','view_course_details','course_details_view','course_detail','course_detail_view','view_course_detail','view_all_assignments','view_assignments'],
    ['switch_course','switch_view'],
    ['view_failing','failing','flag_failing','view_minimum','view_min','flag_min'],
    ['sort_by_last_name','sort_last_name','sort_name','sort_by_name','sort_alphabetical','sort_last_name_alphabetical','sort_name_alphabetical','sort_by_last_name_alphabetical','sort_by_name_alphabetical','sort_by_name_lowest_first','sort_by_last_name_lowest_first','sort_name_lowest_first','sort_last_name_lowest_first'],
    ['sort_by_grade','sort_by_total_grade','sort_grade','sort_total_grade','sort_by_grade_ascending','sort_by_grade_asc','sort_by_grade_1','sort_by_total_grade_ascending','sort_by_total_grade_asc','sort_by_total_grade_1','sort_grade_ascending','sort_grade_asc','sort_grade_1','sort_total_grade_ascending','sort_total_grade_asc','sort_total_grade_1','sort_by_grade_lowest_first','sort_grade_lowest_first','sort_total_grade_lowest_first','sort_by_total_grade_lowest_first','sort_by_grade_lowest','sort_grade_lowest','sort_total_grade_lowest','sort_by_total_grade_lowest'],
    ['sort_by_grade_descending','sort_by_grade_desc','sort_by_grade_-1','sort_by_total_grade_descending','sort_by_total_grade_desc','sort_by_total_grade_-1','sort_grade_descending','sort_grade_desc','sort_grade_-1','sort_total_grade_descending','sort_total_grade_desc','sort_total_grade_-1','sort_by_grade_highest_first','sort_grade_highest_first','sort_total_grade_highest_first','sort_by_total_grade_highest_first','sort_by_grade_highest','sort_grade_highest','sort_total_grade_highest','sort_by_total_grade_highest'],
    ['sort_reverse_alphabetical','sort_reverse','sort_by_reverse','sort_by_reverse_alphabetical','sort_by_name_highest_first','sort_by_last_name_highest_first','sort_name_highest_first','sort_last_name_highest_first','sort_by_name_reverse_alphabetical','sort_by_last_name_reverse_alphabetical','sort_by_name_reverse','sort_name_reverse','sort_last_name_reverse'],
    ['view_assignment','view_assignment_details','assignment_details','assignment_details_view','assignment_detail','assignment_detail_view'],
    ['switch_assignment','switch_assignments','view_other_assignment'],
    ['add_assignment','new_assignment','add_new_assignment','create_assignment'],
    ['rename_assignment','edit_assignment'],
    ['delete_assignment','remove_assignment','drop_assignment'],
    ['edit_points','change_points','edit_point_value','change_point_value','edit_weight'],
    ['edit_date','change_date','edit_due_date','change_due_date'],
    ['add_student','new_student','add_new_student','enroll_student','enroll_new_student'],
    ['add_multiple_students','add_many_students','add_students'],
    ['rename_student','change_student_name'],
    ['delete_student','remove_student','drop_student','kick_student','expel_student'],
    ['view_grades','view_assignment_grades'],
    ['set_grades','grade_assignment','grade_all','grade'],
    ['edit_grade','set_grade','change_grade','edit_student_grade'],
    ['info','app_info','about','about_app','copyright','copyright_info'],
    ['home','main'],
    ['back','return'],
    ['quit','exit']
    ]