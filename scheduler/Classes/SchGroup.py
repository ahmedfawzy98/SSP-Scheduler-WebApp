class SchGroup:
    def __init__(self):
        self.lecture = None
        self.tutorials = []
        self.labs = []
        self.number = None
        self.daysTaken = set()
        self.available = True

    def add_lab(self, lab):
        self.labs.append(lab)
        self.daysTaken.add(lab.time.day)

    def add_tut(self, tut):
        self.tutorials.append(tut)
        self.daysTaken.add(tut.time.day)
