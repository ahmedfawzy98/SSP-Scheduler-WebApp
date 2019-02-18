from scheduler.Classes.Period import Period


class Lab(Period):
    def __init__(self):
        super().__init__(periodType='Lab')
