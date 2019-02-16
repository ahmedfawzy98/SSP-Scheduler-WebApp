from scheduler.Classes import Period
class Lecture(Period):
    def __init__(self):
        Period.__init__(self)
        super().periodType = 'Lec'