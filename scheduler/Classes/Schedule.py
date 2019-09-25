class Schedule:
    def __init__(self):
        self.schedule = [[None for x in range(12)] for y in range(6)]
        self.days = [False, False, False, False, False, False]
        self.daysTaken = 0
        self.priorityValue = 0
        self.gap_value = 0

    def check_clash(self, period):
        for i in range(period.length()):
            if self.schedule[period.time.time_day][period.time.time_from + i] is not None:
                return True
        return False

    def add_period(self, period):
        for i in range(period.length()):
            self.schedule[period.time.time_day][period.time.time_from + i] = period
        if not self.days[period.time.time_day]:
            self.daysTaken += 1
            self.days[period.time.time_day] = True

    def add_to_priority(self, value):
        self.priorityValue += value

    def has_pref_days(self, days):
        for day in days:
            if self.days[day]:
                return False
        return True

    def clone(self, sch):
        for i in range(6):
            for j in range(12):
                self.schedule[i][j] = sch.schedule[i][j]

        # self.priorityValue = sch.priorityValue
        self.daysTaken = sch.daysTaken
        for i in range(6):
            self.days[i] = sch.days[i]

