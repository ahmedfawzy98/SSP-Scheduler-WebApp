from operator import attrgetter
from scheduler.Classes.Node import Node
from scheduler.Classes.Schedule import Schedule
import random
import sys

cache = {}

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
        for ind, course in enumerate(self.courses):
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
        # if 0 <= self.last_prio_course <= 1:
        #     for i in range(0, self.last_prio_course + 1):
        #         self.courses[i].instructors = [self.courses[i].instructors[0]]
        combination_key = ""
        for course in self.courses:
            combination_key += course.name
            if course.priority > 0:
                combination_key += course.instructors[0].name
                combination_key += str(course.instructors[0].priority)
        combination_key += str(self.max_days)
        combination_key += str(self.offdays)
        combination_key += str(self.alt_yes)
        
        

        if combination_key in cache:
            # print(sys.getsizeof(cache[combination_key]))
            self.schedule = random.choice(cache[combination_key][0])
            alt_index = cache[combination_key][0].index(self.schedule)
            self.alternatives = cache[combination_key][1][alt_index]
            self.alt_courses = cache[combination_key][2]
            return
        root = Node(None)
        self.build_tree(root, -1)
        if len(self.completed) > 0:
            perfect_list = self.filtered_completed(combination_key)
        else:
            self.schedule = None
            return
        perfect_schedules_list = [perfect.schedule for perfect in perfect_list]
        cache[combination_key] = [perfect_schedules_list, [], []]

        if len(cache) > 200:
            cache.clear()

        ###
        # Alternative schedules code
        ###
        # getting alternative schedules
        for index, perfect in enumerate(perfect_list):
            cache[combination_key][1].append([])
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
                    # self.alternatives.append(self.priority_duplicates[0].schedule)
                    cache[combination_key][1][index].append(self.priority_duplicates[0].schedule)
                    if index == 0:
                        # self.alt_courses.append(self.courses[len(self.courses) - 1 - i].name)
                        cache[combination_key][2].append(self.courses[len(self.courses) - 1 - i].name)
                else:
                    # self.alternatives.append(None)
                    cache[combination_key][1][index].append(None)
                    if index == 0:
                        # self.alt_courses.append(self.courses[len(self.courses) - 1 - i].name)
                        cache[combination_key][2].append(self.courses[len(self.courses) - 1 - i].name)
                perfect.data.available = True

        try:
            self.schedule = random.choice(cache[combination_key][0])
            alt_index = cache[combination_key][0].index(self.schedule)
            self.alternatives = cache[combination_key][1][alt_index]
            self.alt_courses = cache[combination_key][2]
            return
        except IndexError:
            self.schedule = None
            return


    def filtered_completed(self, combination_key):
        self.completed.sort(key=attrgetter('schedule.priorityValue'), reverse=True)
        best_priority = self.completed[0].get_total_priority()
        priority_duplicates = list(filter(lambda cm: cm.get_total_priority() == best_priority, self.completed))
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
            # cache[combination_key] = [density_duplicates, [], []]
            return density_duplicates
        else:
            # cache[combination_key] = [gap_duplicates, [], []]
            return gap_duplicates