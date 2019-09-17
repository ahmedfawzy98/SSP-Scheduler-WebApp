from operator import attrgetter
from scheduler.Classes.Node import Node
from scheduler.Classes.Schedule import Schedule
from scheduler.Controller.Input import Input
import time
import random


class Controller:
    def __init__(self):
        self.schedule = Schedule()
        self.alternatives = []
        self.levels = []
        self.level = []
        self.completed = []
        self.completedPriorityDuplicate = []
        self.completedDaysDuplicate = []
        self.courses = []
        self.coursesNum = None
        self.bestCompleted = [7,-1]
        self.lastPrioCourse = -1

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
                                if cNum+1 < self.lastPrioCourse:
                                    self.build_tree(node.children[-1], cNum + 1)
                                elif child.schedule.priorityValue >= self.bestCompleted[1]:
                                    self.build_tree(node.children[-1], cNum + 1)
                                elif child.schedule.priorityValue <= self.bestCompleted[1]:
                                    if child.schedule.daysTaken < self.bestCompleted[0]:
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
        self.courses.sort(key=attrgetter('priority'), reverse=True)
        for course in self.courses:
            course.instructors.sort(key=attrgetter('priority'), reverse=True)
            for inst in course.instructors:
                random.shuffle(inst.groups)

        start_time = time.time()
        self.coursesNum = len(self.courses)
        for ind,course in enumerate(self.courses):
            if course.priority > 0:
                self.lastPrioCourse = ind
        copy = self.courses[self.lastPrioCourse:] if self.lastPrioCourse > -1 else self.courses[0:]
        random.shuffle(copy)
        if self.lastPrioCourse > -1:
            self.courses[self.lastPrioCourse:] = copy
        else:
            self.courses[0:] = copy
        # if the prioritized courses are 2 or less then only for these courses keep the prioritized instructor and
        # delete the others
        if 0 <= self.lastPrioCourse <= 1:
            for i in range(0,self.lastPrioCourse+1):
                self.courses[i].instructors = [self.courses[i].instructors[0]]
        root = Node(None)
        self.build_tree(root,-1)
        print("Execution Time: --- %s seconds ---" % (time.time() - start_time))
        self.completed.sort(key=attrgetter('schedule.priorityValue'), reverse=True)
        self.completedPriorityDuplicate = [self.completed[i] for i in range(0,len(self.completed))
                                           if self.completed[0].get_total_priority()
                                           == self.completed[i].get_total_priority()]

        self.completedPriorityDuplicate.sort(key=attrgetter('schedule.daysTaken'))
        self.completedDaysDuplicate = [self.completedPriorityDuplicate[i] for i in range(0, len(self.completedPriorityDuplicate))
                                           if self.completedPriorityDuplicate[0].schedule.daysTaken
                                           == self.completedPriorityDuplicate[i].schedule.daysTaken]
        self.schedule = random.choice(self.completedDaysDuplicate).schedule
        print("HAKUNA")
        # self.schedule = self.completedPriorityDuplicate[0].schedule
        ####
        # Alternative schedules code
        ####
        # perfect = self.completedPriorityDuplicate[0]
        # getting alternative schedules
        # for i in range(len(self.courses)):
        #     self.completedPriorityDuplicate.clear()
        #     if i != 0:
        #         perfect = perfect.parent
        #     perfect.data.available = False
        #     # iterate until a schedule without an unavailable group is found
        #     for j in range(len(self.completed)):
        #         if self.completed[j].all_available():
        #             # add the first found all-available schedule and its priority duplicates to completedPriorityD
        #             self.completedPriorityDuplicate = [self.completed[j+k] for k in range(0, len(self.completed)-j-1)
        #                                                if (self.completed[j].get_total_priority()
        #                                                == self.completed[j+k].get_total_priority()
        #                                                    and self.completed[j+k].all_available())]
        #             break
        #     if len(self.completedPriorityDuplicate) != 0:
        #         self.completedPriorityDuplicate.sort(key=attrgetter('schedule.daysTaken'))
        #         self.alternatives.append(self.completedPriorityDuplicate[0].schedule)
        #     perfect.data.available = True
