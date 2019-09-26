class Schedule:
    def __init__(self):
        self.schedule = [[None for x in range(12)] for y in range(6)]
        self.days = [False, False, False, False, False, False]
        self.daysTaken = 0
        self.priorityValue = 0
        self.gap_value = 0
        self.max_density = 0

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

    def calculate_gap(self):
        counting = False
        for i in range(0,6):
            day_gap = 0
            for j in range(0,12):
                # When the first non free period is encountered starts counting gaps , when another non free period
                #   add the counted gaps to the day_gap
                if counting:
                    if self.schedule[i][j] is not None:
                        if day_gap:
                            # If an even single-period lab or tutorial is found decrement the day_gap because that means
                            #   there's a counted gap that isn't actually a gap
                            if self.schedule[i][j].length() == 1 and self.schedule[i][j].periodType != "Lecture" and j % 2 == 1 \
                                    and self.schedule[i][j - 1] is None:
                                day_gap -= 1
                            self.gap_value += day_gap
                            day_gap = 0
                        else:
                            # If an odd single-period lab or tutorial is found decrement the day_gap because that means
                            #   there will be a counted gap that isn't actually a gap
                            if self.schedule[i][j].length() == 1 and self.schedule[i][j].periodType != "Lecture" and j % 2 == 0 \
                                    and self.schedule[i][j + 1] is None:
                                day_gap -= 1
                    else:
                        day_gap += 1
                elif self.schedule[i][j] is not None:
                    if self.schedule[i][j].length() == 1 and self.schedule[i][j].periodType != "Lecture" and j % 2 == 0 \
                                and self.schedule[i][j+1] is None:
                        day_gap -= 1
                    counting = True
            day_gap = 0
            counting = False

    def calc_max_density(self):
        for i in range(0, 6):
            day_density = 0
            for j in range(0, 12):
                if self.schedule[i][j]:
                    day_density += 1
            if day_density > self.max_density:
                self.max_density = day_density

    def clone(self, sch):
        for i in range(6):
            for j in range(12):
                self.schedule[i][j] = sch.schedule[i][j]

        # self.priorityValue = sch.priorityValue
        self.daysTaken = sch.daysTaken
        for i in range(6):
            self.days[i] = sch.days[i]

