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
                        # check if the current group doesn't clash with the current tree branch
                        if not self.levels[i - 1][o].check_clash(self.courses[i].instructors[j].groups[k],
                                                                 self.levels[i - 1][o].schedule):
                            # add the group to the current branch
                            self.levels[i - 1][o].add_child(self.courses[i].instructors[j].groups[k])
                            # update the last added child total schedule's priority
                            self.levels[i - 1][o].children[-1].schedule.add_to_priority(
                                self.courses[i].instructors[j].priority +
                                self.levels[i - 1][o].children[-1].parent.get_total_priority())
                            # add the last added child to the current level
                            self.levels[i].append(self.levels[i - 1][o].children[-1])
                            # if the current course is the last add the last added child to the completed array
                            if i == len(self.courses) - 1:
                                self.completed.append(self.levels[i - 1][o].children[-1])
        self.completed.sort(key=attrgetter('schedule.priorityValue'), reverse=True)
        self.completedPriorityDuplicate = [self.completed[i] for i in range(0,len(self.completed))
                                           if self.completed[0].get_total_priority()
                                           == self.completed[i].get_total_priority()]

        self.completedPriorityDuplicate.sort(key=attrgetter('schedule.daysTaken'))
        self.schedule = self.completedPriorityDuplicate[0].schedule
        perfect = self.completedPriorityDuplicate[0]
        # getting alternative schedules
        for i in range(len(self.courses)):
            self.completedPriorityDuplicate.clear()
            if i != 0:
                perfect = perfect.parent
            perfect.data.available = False
            # iterate until a schedule without an unavailable group is found
            for j in range(len(self.completed)):
                if self.completed[j].all_available():
                    # add the first found all-available schedule and its priority duplicates to completedPriorityD
                    self.completedPriorityDuplicate = [self.completed[j+k] for k in range(0, len(self.completed)-j-1)
                                                       if (self.completed[j].get_total_priority()
                                                       == self.completed[j+k].get_total_priority()
                                                           and self.completed[j+k].all_available())]
                    break
            if len(self.completedPriorityDuplicate) != 0:
                self.completedPriorityDuplicate.sort(key=attrgetter('schedule.daysTaken'))
                self.alternatives.append(self.completedPriorityDuplicate[0].schedule)
            perfect.data.available = True
