from operator import attrgetter
from scheduler.Classes.Node import Node
from scheduler.Classes.Schedule import Schedule
from scheduler.Controller.Input import Input


class Controller:
    schedule = Schedule()
    alternatives = []
    levels = []
    level = []
    completed = []
    completedPriorityDuplicate = []

    def makeSchedule(self):
        database = Input()
        courses = database.courses
        # instructors = database.instructors
        courses[2].priority = 5
        courses[2].insturctors[1].priority = 5
        courses.sort()
        for course in courses:
            course.instructors.sort(key=attrgetter('priority'), reverse=True)
        for i in range(len(courses[0].instructors)):
            for j in range(len(courses[0].instructors[i].groups)):
                n = Node(courses[0].instructors[i].groups[j])
                n.schedule.add_to_priority(courses[0].instructors[i].priority)
                self.level.append(n)
        self.levels.append(self.level)
        for i in range(1, len(courses)):
            self.levels.append(list())
            for j in range(len(courses[i].instructors)):
                for k in range(len(courses[i].instructors[j].gruops)):
                    for o in range(len(self.levels[i-1])):
                        if not self.levels[i-1][o].check_clash(courses[i].instructors[j].groups[k],
                                                               self.levels[i-1][0].schedule):
                            self.levels[i-1][o].shcedule.add_to_priority(courses[i].instructors[j].priority)
                            self.levels[i-1][o].add_child(courses[i].instructors[j].groups[k])
                            self.levels[i].append(self.levels[i-1][o].children[len(self.levels[i-1][o].children)-1])
                            if i == len(courses)-1:
                                self.completed.append(self.levels[i-1][o].children[len(self.levels[i-1][o].children)-1])
        self.completed.sort(key=attrgetter('schedule.priority'), reverse=True)
        i = 1
        tempPriority = self.completed[i].schedule.priority
        self.completedPriorityDuplicate.append(self.completed[0])
        while self.completed[0].schedule.priority == tempPriority:
            self.completedPriorityDuplicate.append(self.completed[i])
            i += 1
            if i == len(self.completed):
                break
            tempPriority = self.completed[i].schedule.priority
        self.completedPriorityDuplicate.sort(key=attrgetter('schedule.daysTaken'), reverse=True)
        self.schedule = self.completedPriorityDuplicate[0].schedule
        perfect = self.completedPriorityDuplicate[0]
        for i in range(len(courses)):
            self.completedPriorityDuplicate.clear()
            if i != 0:
                perfect = perfect.parent
            perfect.data.available = False
            for j in range(len(self.completed)):
                if self.completed[j].all_available():
                    self.completedPriorityDuplicate.append(self.completed[j])
                    ii = 1
                    tempPriority = self.completed[j+ii].shcedule.priority
                    while self.completed[j].shcedule.priority == tempPriority:
                        if self.completed[j+ii].all_available():
                            self.completedPriorityDuplicate.append(self.completed[j+ii])
                        ii += 1
                        if j+ii == len(self.completed):
                            break
                        tempPriority = self.completed[j+i].shcedule.priority
                    break
            if len(self.completedPriorityDuplicate) != 0:
                self.completedPriorityDuplicate.sort(key=attrgetter('schedule.daysTaken'), reverse=True)
                self.alternatives.append(self.completedPriorityDuplicate[0].shcedule)
            perfect.data.available = True
