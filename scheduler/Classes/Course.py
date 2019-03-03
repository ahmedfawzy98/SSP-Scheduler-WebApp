class Course:
    def __init__(self, name, instructor=None, termNum=0, crHrs=0):
        self.priority = 0
        self.name = name
        self.instructors = []
        if instructor is not None:
            self.add_instructor(instructor)
        self.term = termNum
        self.creditHours = crHrs

    def add_instructor(self, instructor):
        self.instructors.append(instructor)
