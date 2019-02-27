class Course:
    def __init__(self, name, instructor):
        self.priority = 0
        self.name = name
        self.instructors = []
        self.add_instructor(instructor)
        self.term = 0

    def add_instructor(self, instructor):
        self.instructors.append(instructor)
