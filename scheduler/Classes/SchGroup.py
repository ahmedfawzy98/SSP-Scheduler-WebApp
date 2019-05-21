class SchGroup:
    def __init__(self):
        self.lecture = None
        self.exLecture = None
        self.tutorials = []
        self.labs = []
        self.number = None
        self.daysTaken = set()
        self.available = True
        self.termNum = 0
        self.creditHours = 0

    def setLecture(self, lecture):
        self.lecture = lecture
        self.daysTaken.add(lecture.time.day)

    def setExLecture(self, exLecture):
        self.exLecture = exLecture
        self.daysTaken.add(exLecture.time.day)


    def add_lab(self, lab):
        self.labs.append(lab)
        self.daysTaken.add(lab.time.day)

    def add_tut(self, tut):
        self.tutorials.append(tut)
        self.daysTaken.add(tut.time.day)
