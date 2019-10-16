from scheduler.Classes.Schedule import Schedule
from bitarray import bitarray
import copy


def make_bit_array(size):
    ar = bitarray(size)
    ar.setall(0)
    return ar


class Node:
    def __init__(self, data, sch=None, iTut=-1,iLab=-1, priority_value=None, days_taken=None, days=None):
        self.children = []
        self.parent = None
        self.data = data
        self.days = [False, False, False, False, False, False]
        self.daysTaken = 0
        self.priorityValue = 0
        self.bit_schedule = [make_bit_array(12) for i in range(6)]
        self.schedule = None
        if sch is not None:
            self.bit_schedule = copy.deepcopy(sch)
            self.daysTaken = days_taken
            self.priorityValue = priority_value
            self.days = copy.deepcopy(days)
        self.tutNum = iTut
        self.labNum = iLab
        self.add_to_schedule()

    def add_child(self, data, iTut, iLab):
        child = Node(data, self.bit_schedule, iTut, iLab, self.priorityValue, self.daysTaken, self.days)
        child.parent = self
        self.children.append(child)

    def check_clash(self, group, iTut, iLab):
        if self.daysTaken == 0:
            return False

        if self.period_check_clash(group.lecture):
            return True

        if group.exLecture is not None:
            if self.period_check_clash(group.exLecture):
                return True

        if iTut != -1:
            if self.period_check_clash(group.tutorials[iTut]):
                return True
        if iLab != -1:
            if self.period_check_clash(group.labs[iLab]):
                return True
        return False

    def add_to_schedule(self):
        if self.data is not None:
            self.add_period(self.data.lecture)
            if self.data.exLecture is not None:
                self.add_period(self.data.exLecture)
            if self.tutNum != -1:
                self.add_period(self.data.tutorials[self.tutNum])
            if self.labNum != -1:
                self.add_period(self.data.labs[self.labNum])

    def all_available(self):
        current = self
        while current.data is not None:
            if not current.data.available:
                return False
            else:
                current = current.parent
        return True

    def get_total_priority(self):
        return self.priorityValue

    def add_to_priority(self, value):
        self.priorityValue += value

    def add_period(self, period):
        for i in range(period.length()):
            self.bit_schedule[period.time.time_day][period.time.time_from + i] = True
        if not self.days[period.time.time_day]:
            self.daysTaken += 1
            self.days[period.time.time_day] = True

    def period_check_clash(self, period):
        for i in range(period.length()):
            if self.bit_schedule[period.time.time_day][period.time.time_from + i] is True:
                return True
        return False

    def build_schedule(self):
        self.schedule = Schedule()
        self.schedule.days = self.days
        self.schedule.priorityValue = self.priorityValue
        self.schedule.daysTaken = self.daysTaken
        node = self
        while node.parent is not None:
            if node.data is not None:
                self.schedule.add_period(node.data.lecture)
                if node.data.exLecture is not None:
                    self.schedule.add_period(node.data.exLecture)
                if node.tutNum != -1:
                    self.schedule.add_period(node.data.tutorials[node.tutNum])
                if node.labNum != -1:
                    self.schedule.add_period(node.data.labs[node.labNum])
            node = node.parent

    def has_pref_days(self, days):
        for day in days:
            if self.days[day]:
                return False
        return True
