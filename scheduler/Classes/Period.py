from scheduler.Classes.Time import Time


class Period:
    def __init__(self):
        self.instName = ''
        self.courseName = ''
        self.place = ''
        self.type = 0
        self.time = Time()
        self.length = 0
        self.groupNum = 0
        self.periodType = ''

    def printMe(self):
        info = '(' + str(self.groupNum) + ')' + str(self.courseName) + '-' + str(self.periodType)
        print(info, end='')
        for i in range(38-len(info)):
            print(end=' ')
