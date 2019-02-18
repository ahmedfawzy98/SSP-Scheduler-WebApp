from scheduler.Classes.Period import Period


class Lecture(Period):
    def __init__(self):
        super().__init__(periodType='Lec')

