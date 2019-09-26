from operator import attrgetter
from scheduler.Classes.Node import Node
from scheduler.Classes.Schedule import Schedule
import random


class Controller:
    def __init__(self):
        self.schedule = Schedule()
        self.alternatives = []
        self.alt_courses = []
        self.completed = []
        self.priority_duplicates = []
        self.days_duplicates = []
        self.gap_duplicates = []
        self.courses = []
        self.courses_num = None
        self.best_completed = [7, -1]
        self.last_prio_course = -1
        self.offdays = []
        self.max_days = False
        self.alt_yes = False
        self.preferred_days = []

    def build_tree(self, node, cNum):
        if cNum != self.courses_num-1:
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
                                if cNum+1 < self.last_prio_course:
                                    self.build_tree(node.children[-1], cNum + 1)
                                # If this branch has more priority value than the current best then continue
                                elif child.schedule.priorityValue > self.best_completed[1]:
                                    self.build_tree(node.children[-1], cNum + 1)
                                # If this branch has the same priority value as the best but less or equal days continue
                                elif child.schedule.priorityValue == self.best_completed[1]:
                                    if self.max_days:
                                        if child.schedule.daysTaken >= self.best_completed[0]:
                                            self.build_tree(node.children[-1], cNum + 1)
                                    else:
                                        if child.schedule.daysTaken <= self.best_completed[0]:
                                            self.build_tree(node.children[-1], cNum + 1)
                                else:
                                    return

        else:
            self.completed.append(node)
            if node.schedule.priorityValue == self.best_completed[1]:
                if self.max_days:
                    if node.schedule.daysTaken > self.best_completed[0]:
                        self.best_completed[0] = node.schedule.daysTaken
                else:
                    if node.schedule.daysTaken < self.best_completed[0]:
                        self.best_completed[0] = node.schedule.daysTaken
            elif node.schedule.priorityValue > self.best_completed[1]:
                self.best_completed = [node.schedule.daysTaken, node.schedule.priorityValue]
            return

    def create_schedules(self):
        # Sorting the courses so that it starts the tree with the most prioritized to make sure the branches will always
        #   contain them
        self.courses.sort(key=attrgetter('priority'), reverse=True)

        for course in self.courses:
            course.instructors.sort(key=attrgetter('priority'), reverse=True)
            # for inst in course.instructors:
            #     random.shuffle(inst.groups)

        self.courses_num = len(self.courses)
        for ind,course in enumerate(self.courses):
            if course.priority > 0:
                self.last_prio_course = ind

        # Shuffling the courses after the last prioritized course
        # copy = self.courses[self.lastPrioCourse:] if self.lastPrioCourse > -1 else self.courses[0:]
        # random.shuffle(copy)
        # if self.lastPrioCourse > -1:
        #     self.courses[self.lastPrioCourse:] = copy
        # else:
        #     self.courses[0:] = copy

        # if the prioritized courses are 2 or less then only for these courses keep the prioritized instructor and
        # delete the others
        if 0 <= self.last_prio_course <= 1:
            for i in range(0, self.last_prio_course + 1):
                self.courses[i].instructors = [self.courses[i].instructors[0]]
        root = Node(None)
        self.build_tree(root,-1)

        try:
            perfect = self.filtered_completed()
        except IndexError:
            self.schedule = None
            return
        self.schedule = perfect.schedule

        ###
        # Alternative schedules code
        ###
        # getting alternative schedules
        if self.alt_yes:
            for i in range(len(self.courses)):
                self.priority_duplicates = []
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
                    self.alt_courses.append(self.courses[len(self.courses) - 1 - i].name)
                else:
                    self.alternatives.append(None)
                    self.alt_courses.append(self.courses[len(self.courses) - 1 - i].name)
                perfect.data.available = True

    def filtered_completed(self):
        self.completed.sort(key=attrgetter('schedule.priorityValue'), reverse=True)
        priority_duplicates = [self.completed[i] for i in range(0, len(self.completed))
                                    if self.completed[0].get_total_priority()
                                    == self.completed[i].get_total_priority()]
        if self.max_days:
            priority_duplicates.sort(key=attrgetter('schedule.daysTaken'), reverse=True)
        else:
            priority_duplicates.sort(key=attrgetter('schedule.daysTaken'))
        days_duplicates = [priority_duplicates[i] for i in range(0, len(priority_duplicates))
                                if priority_duplicates[0].schedule.daysTaken
                                == priority_duplicates[i].schedule.daysTaken]
        preferred_days = [days_duplicates[i] for i in range(0, len(days_duplicates))
                               if days_duplicates[i].schedule.has_pref_days(self.offdays)]
        list(map(lambda x: x.schedule.calculate_gap(), preferred_days))
        list(map(lambda x: x.schedule.calc_max_density(), preferred_days))
        preferred_days.sort(key=attrgetter('schedule.gap_value'))
        gap_duplicates = [preferred_days[i] for i in range(0, len(preferred_days))
                               if preferred_days[0].schedule.gap_value
                               == preferred_days[i].schedule.gap_value]
        if self.max_days:
            gap_duplicates.sort(key=attrgetter('schedule.max_density'))
            density_duplicates = [gap_duplicates[i] for i in range(0, len(gap_duplicates))
                              if gap_duplicates[0].schedule.max_density
                              == gap_duplicates[i].schedule.max_density]
            return random.choice(density_duplicates)
        else:
            return random.choice(gap_duplicates)
