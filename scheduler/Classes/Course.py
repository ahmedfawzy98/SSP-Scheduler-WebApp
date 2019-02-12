class Course:
    def __init__(self,name,instructor):
        self.name = name
        self.instructors = []
        self.add_instructor(instructor)

    def add_instructor(self,instructor):
        self.instructors.append(instructor)