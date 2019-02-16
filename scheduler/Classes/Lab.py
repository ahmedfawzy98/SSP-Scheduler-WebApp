from scheduler.Classes import Period
class Lab(Period):
    def __init__(self):
        Period.__init__(self)
        super().periodType = 'Lab'