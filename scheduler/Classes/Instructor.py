class Instructor:
    def __init__(self,name,courseName,group):
        self.priority = 0
        self.name = name
        self.courseName = courseName
        self.groups = []
        self.add_group(group)

    def add_group(self,group):
        self.groups.append(group)