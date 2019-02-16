from scheduler.Classes import Period
class Tutorial(Period):
    def __init__(self):
        Period.__init__(self)
        super().periodType = 'Tut'