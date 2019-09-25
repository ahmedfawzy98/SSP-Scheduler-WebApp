from operator import attrgetter
from scheduler.Classes.Node import Node
from scheduler.Classes.Schedule import Schedule
import random


class Controller:
    def __init__(self):
        self.schedule = Schedule()
        self.alternatives = []
        self.altCourses = []
        self.completed = []
        self.priority_duplicates = []
        self.days_duplicates = []
        self.gap_duplicates = []
        self.courses = []
        self.coursesNum = None
        self.bestCompleted = [7,-1]
        self.lastPrioCourse = -1
        self.offdays = []
        self.preferred_days = []

    def build_tree(self, node, cNum):
        if cNum != self.coursesNum-1:
            for inst in self.courses[cNum+1].instructors:
                for group in inst.groups:
                    tutsNum = len(group.tutorials)
                    labsNum = len(group.labs)
                    tutsInd = list(range(0, tutsNum)) if tutsNum > 0 else [-1]
                    labsInd = list(range(0, labsNum)) if labsNum > 0 else [-1]
                    for iTut in range(len(tutsInd)):
                        for iLab in range(len(labsInd)):
                            # check if the current group doesn't clash with the current tree branch
                            if not node.check_clash(group,node.schedule,tutsInd[iTut],labsInd[iLab]):
                                # add the group to the current branch
                                node.add_child(group, tutsInd[iTut], labsInd[iLab])
                                # update the last added child total schedule's priority
                                node.children[-1].schedule.add_to_priority(
                                    inst.priority +
                                    node.children[-1].parent.get_total_priority())

                                child = node.children[-1]
                                # If this branch didn't reach the last prioritized course then continue
                                if cNum+1 < self.lastPrioCourse:
                                    self.build_tree(node.children[-1], cNum + 1)
                                # If this branch has more priority value than the current best then continue
                                elif child.schedule.priorityValue > self.bestCompleted[1]:
                                    self.build_tree(node.children[-1], cNum + 1)
                                # If this branch has the same priority value as the best but less or equal days continue
                                elif child.schedule.priorityValue == self.bestCompleted[1]:
                                    if child.schedule.daysTaken <= self.bestCompleted[0]:
                                        self.build_tree(node.children[-1], cNum + 1)
                                else:
                                    return

        else:
            self.completed.append(node)
            if node.schedule.priorityValue == self.bestCompleted[1]:
                if node.schedule.daysTaken < self.bestCompleted[0]:
                    self.bestCompleted[0] = node.schedule.daysTaken
            elif node.schedule.priorityValue > self.bestCompleted[1]:
                self.bestCompleted = [node.schedule.daysTaken, node.schedule.priorityValue]
            return


    def makeSchedule(self):
        # Sorting the courses so that it starts the tree with the most prioritized to make sure the branches will always
        #   contain them
        self.courses.sort(key=attrgetter('priority'), reverse=True)

        for course in self.courses:
            course.instructors.sort(key=attrgetter('priority'), reverse=True)
            # for inst in course.instructors:
            #     random.shuffle(inst.groups)

        self.coursesNum = len(self.courses)
        for ind,course in enumerate(self.courses):
            if course.priority > 0:
                self.lastPrioCourse = ind

        # Shuffling the courses after the last prioritized course
        # copy = self.courses[self.lastPrioCourse:] if self.lastPrioCourse > -1 else self.courses[0:]
        # random.shuffle(copy)
        # if self.lastPrioCourse > -1:
        #     self.courses[self.lastPrioCourse:] = copy
        # else:
        #     self.courses[0:] = copy

        # if the prioritized courses are 2 or less then only for these courses keep the prioritized instructor and
        # delete the others
        if 0 <= self.lastPrioCourse <= 1:
            for i in range(0,self.lastPrioCourse+1):
                self.courses[i].instructors = [self.courses[i].instructors[0]]
        root = Node(None)
        self.build_tree(root,-1)
        self.filter_completed()
        try:
            perfect = random.choice(self.gap_duplicates)
        except IndexError:
            self.schedule = None
            return
        self.schedule = perfect.schedule

        ###
        # Alternative schedules code
        ###
        # getting alternative schedules
        for i in range(len(self.courses)):
            self.priority_duplicates.clear()
            if i != 0:
                perfect = perfect.parent
            perfect.data.available = False
            # iterate until a schedule without an unavailable group is found
            for j in range(len(self.completed)):
                if self.completed[j].all_available():
                    # add the first found all-available schedule and its priority duplicates to completedPriorityD
                    self.priority_duplicates = [self.completed[j + k] for k in range(0, len(self.completed) - j - 1)
                                                if (self.completed[j].get_total_priority()
                                                       == self.completed[j+k].get_total_priority()
                                                           and self.completed[j+k].all_available())]
                    break
            if len(self.priority_duplicates) != 0:
                self.priority_duplicates.sort(key=attrgetter('schedule.daysTaken'))
                self.alternatives.append(self.priority_duplicates[0].schedule)
                self.altCourses.append(self.courses[len(self.courses)-1-i].name)
            else:
                self.alternatives.append(None)
                self.altCourses.append(self.courses[len(self.courses) - 1 - i].name)
            perfect.data.available = True

    def filter_completed(self):
        self.completed.sort(key=attrgetter('schedule.priorityValue'), reverse=True)
        self.priority_duplicates = [self.completed[i] for i in range(0, len(self.completed))
                                    if self.completed[0].get_total_priority()
                                    == self.completed[i].get_total_priority()]
        self.priority_duplicates.sort(key=attrgetter('schedule.daysTaken'))
        self.days_duplicates = [self.priority_duplicates[i] for i in range(0, len(self.priority_duplicates))
                                if self.priority_duplicates[0].schedule.daysTaken
                                == self.priority_duplicates[i].schedule.daysTaken]
        self.preferred_days = [self.days_duplicates[i] for i in range(0, len(self.days_duplicates))
                               if self.days_duplicates[i].schedule.has_pref_days(self.offdays)]
        list(map(lambda x: x.schedule.calculate_gap(), self.preferred_days))
        self.preferred_days.sort(key=attrgetter('schedule.gap_value'))
        self.gap_duplicates = [self.preferred_days[i] for i in range(0, len(self.preferred_days))
                               if self.preferred_days[0].schedule.gap_value
                               == self.preferred_days[i].schedule.gap_value]
        return
