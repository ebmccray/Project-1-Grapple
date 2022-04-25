# ======================================
# GLOBAL CLASSES
# ======================================
class Assignment():
    def __init__(self,name):
        self.name=name

class Student():
    def __init__(self,name):
        self.name=name
        self.grades = {
            'Quiz 1': 100,
            'Final': 98
        }

class Course():
    def __init__(self, name):
        self.name = name
        self.assignments = [Assignment('Quiz 1'),Assignment('Final')]
        self.student_list = [Student('Jessica Bird'),Student("Leo")]