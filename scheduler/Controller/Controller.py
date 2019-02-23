from operator import attrgetter
from scheduler.Classes.Node import Node
from scheduler.Classes.Schedule import Schedule
from scheduler.Controller.Input import Input


class Controller:
    def __init__(self):
        self.schedule = Schedule()
        self.alternatives = []
        self.levels = []
        self.level = []
        self.completed = []
        self.completedPriorityDuplicate = []
        self.courses = []

    def makeSchedule(self):
        # database = Input()
        # self.courses = database.courses
        # self.courses[2].priority = 5
        # self.courses[2].instructors[1].priority = 5
        self.courses.sort(key=attrgetter('priority'), reverse=True)
        for course in self.courses:
            course.instructors.sort(key=attrgetter('priority'), reverse=True)
        for i in range(len(self.courses[0].instructors)):
            for j in range(len(self.courses[0].instructors[i].groups)):
                n = Node(self.courses[0].instructors[i].groups[j])
                n.schedule.add_to_priority(self.courses[0].instructors[i].priority)
                self.level.append(n)
        self.levels.append(self.level)
        for i in range(1, len(self.courses)):
            self.levels.append(list())
            for j in range(len(self.courses[i].instructors)):
                for k in range(len(self.courses[i].instructors[j].groups)):
                    for o in range(len(self.levels[i - 1])):
                        if not self.levels[i - 1][o].check_clash(self.courses[i].instructors[j].groups[k],
                                                                 self.levels[i - 1][o].schedule):
                            # self.levels[i-1][o].schedule.add_to_priority(self.courses[i].instructors[j].priority)
                            self.levels[i - 1][o].add_child(self.courses[i].instructors[j].groups[k])
                            self.levels[i - 1][o].children[-1].schedule.add_to_priority(
                                self.courses[i].instructors[j].priority +
                                self.levels[i - 1][o].children[-1].parent.schedule.priorityValue)
                            self.levels[i].append(self.levels[i - 1][o].children[-1])
                            if i == len(self.courses) - 1:
                                self.completed.append(self.levels[i - 1][o].children[-1])
        self.completed.sort(key=attrgetter('schedule.priorityValue'), reverse=True)
        i = 1
        tempPriority = self.completed[i].schedule.priorityValue
        self.completedPriorityDuplicate.append(self.completed[0])
        while self.completed[0].schedule.priorityValue == tempPriority:
            self.completedPriorityDuplicate.append(self.completed[i])
            i += 1
            if i == len(self.completed):
                break
            tempPriority = self.completed[i].schedule.priorityValue
        self.completedPriorityDuplicate.sort(key=attrgetter('schedule.daysTaken'))
        self.schedule = self.completedPriorityDuplicate[0].schedule
        perfect = self.completedPriorityDuplicate[0]
        for i in range(len(self.courses)):
            self.completedPriorityDuplicate.clear()
            if i != 0:
                perfect = perfect.parent
            perfect.data.available = False
            for j in range(len(self.completed)):
                if self.completed[j].all_available():
                    self.completedPriorityDuplicate.append(self.completed[j])
                    ii = 1
                    tempPriority = self.completed[j + ii].schedule.priorityValue
                    while self.completed[j].schedule.priorityValue == tempPriority:
                        if self.completed[j + ii].all_available():
                            self.completedPriorityDuplicate.append(self.completed[j + ii])
                        ii += 1
                        if j + ii == len(self.completed):
                            break
                        tempPriority = self.completed[j + ii].schedule.priorityValue
                    break
            if len(self.completedPriorityDuplicate) != 0:
                self.completedPriorityDuplicate.sort(key=attrgetter('schedule.daysTaken'))
                self.alternatives.append(self.completedPriorityDuplicate[0].schedule)
            perfect.data.available = True
