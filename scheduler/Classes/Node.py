from scheduler.Classes.Schedule import Schedule


class Node:
    def __init__(self, data, sch=None, iTut=-1,iLab=-1):
        self.children = []
        self.parent = None
        self.data = data
        self.schedule = Schedule()
        if sch is not None:
            self.schedule.clone(sch)
        self.tutNum = iTut
        self.labNum = iLab
        self.add_to_schedule()


    def add_child(self, data, iTut, iLab):
        child = Node(data, self.schedule, iTut, iLab)
        child.parent = self
        self.children.append(child)

    @staticmethod
    def check_clash(group, sch , iTut, iLab):
        if sch.daysTaken == 0:
            return False

        if sch.check_clash(group.lecture):
            return True

        if group.exLecture is not None:
            if sch.check_clash(group.exLecture):
                return True

        if iTut != -1:
            if sch.check_clash(group.tutorials[iTut]):
                return True
        if iLab != -1:
            if sch.check_clash(group.labs[iLab]):
                return True
        return False

    def add_to_schedule(self):
        if self.data is not None:
            self.schedule.add_period(self.data.lecture)
            if self.data.exLecture is not None:
                self.schedule.add_period(self.data.exLecture)
            if self.tutNum != -1:
                self.schedule.add_period(self.data.tutorials[self.tutNum])
            if self.labNum != -1:
                self.schedule.add_period(self.data.labs[self.labNum])

    def all_available(self):
        current = self
        while current is not None:
            if not current.data.available:
                return False
            else:
                current = current.parent
        return True

    def get_total_priority(self):
        return self.schedule.priorityValue
