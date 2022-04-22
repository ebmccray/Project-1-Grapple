import course_commands as cc

def view_course():
    course=str(input("\nPlease enter the name of the course. >>>\t"))

    my_course=''
    for c in cc.courses:
        if c.name==course:
            my_course=c

    if my_course =='':
        print ("\nSorry, no course of that name could be found. Please try again.")
    
    else:
        print('\n%s\n----------'%course)

        x = ['Student Name','Overall Grade']
        for a in my_course.assignments:
            x.append(a.name)
        
        for i in range(len(x)):
            print('|\t'+x[i]+'\t', end =" ")
        print('|')

        for s in my_course.student_list:
            print('|\t'+ s)