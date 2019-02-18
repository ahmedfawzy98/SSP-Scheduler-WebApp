from scheduler.Classes.Time import Time


class Period:
    # def __init__(self):
    #     self.instName = ''
    #     self.courseName = ''
    #     self.place = ''
    #     self.type = 0
    #     self.time = Time()
    #     self.length = 0
    #     self.groupNum = 0
    #     self.periodType = ''
    def __init__(self, periodType='', instName='', courseName='', place='', type=0, time=Time(), length=0, groupNum=0):
        self.periodType = periodType
        self.instName = instName
        self.courseName = courseName
        self.place = place
        self.type = type
        self.time = time
        self.length = length
        self.groupNum = groupNum

    def printMe(self):
        info = '(' + str(self.groupNum) + ')' + str(self.courseName) + '-' + str(self.periodType)
        print(info, end='')
        for i in range(38-len(info)):
            print(end=' ')
