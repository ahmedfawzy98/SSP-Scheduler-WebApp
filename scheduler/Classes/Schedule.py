from scheduler.Classes.Period import Period


class Schedule:
    def __init__(self):
        self.schedule = [[None for x in range(12)] for y in range(6)]
        self.days = [False, False, False, False, False, False]
        self.daysTaken = 0
        self.priorityValue = 0

    def check_clash(self, period):
        for i in range(period.length):
            if self.schedule[period.time.day][period.time.fr + i] is not None:
                return True
        return False

    def add_period(self, period):
        for i in range(period.length):
            self.schedule[period.time.day][period.time.fr + i] = period
        if not self.days[period.time.day]:
            self.daysTaken += 1
            self.days[period.time.day] = True

    def add_to_priority(self, value):
        self.priorityValue += value

    def clone(self, sch):
        for i in range(6):
            for j in range(12):
                self.schedule[i][j] = sch.schedule[i][j]

        self.priorityValue = sch.priorityValue
        self.daysTaken = sch.daysTaken
        for i in range(6):
            self.days[i] = sch.days[i]

    def printSchedule(self):
        for i in range(6):
            print(str(i), end=' ')
            for j in range(12):
                if self.schedule[i][j] is None:
                    print('                  ' + str(j) + '                   ', end='')
                else:
                    self.schedule[i][j].printMe()
            print()
