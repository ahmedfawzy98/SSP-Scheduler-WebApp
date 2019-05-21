from scheduler.Classes.Course import Course
from scheduler.Classes.Instructor import Instructor
from scheduler.Classes.Lab import Lab
from scheduler.Classes.Schedule import Schedule
from scheduler.Classes.Tutorial import Tutorial
from scheduler.models import Group
from scheduler.Classes.SchGroup import SchGroup
from scheduler.Classes.Time import Time
from scheduler.Classes.Lecture import Lecture


class Input:
    def __init__(self):
        self.courses = []
        self.instructors = []
        self.groups = []
        self.read()
        self.create()

    def getCoursesOnly(self):
        # using dict to avoid duplicates
        return list({row.lecCrsName: Course(row.lecCrsName, termNum=row.termNum, crHrs=row.creditHours)
                     for row in Group.objects.all()}.values())

    def read(self):
        database = Group.objects.all()
        for item in database:
            g = SchGroup()
            t = Time()
            l = Lecture()
            g.number = item.groupNum
            l.groupNum = item.groupNum
            l.instName = item.lecInstName
            l.courseName = item.lecCrsName
            l.place = item.lecPlace
            l.type = item.lecType
            t.day = item.lecDay
            t.fr = item.lecFrom
            t.to = item.lecTo
            l.setTime(t)
            l.periodType = item.lecPeriodType
            g.setLecture(l)

            ###
            t = Time()
            l = Lecture()
            l.groupNum = item.groupNum
            l.instName = item.lecInstName
            l.courseName = item.lecCrsName
            l.place = item.lecExPlace
            l.type = item.lecType
            t.day = item.lecExDay
            t.fr = item.lecExFrom
            t.to = item.lecExTo
            if l.place is not None:
                l.setTime(t)
            l.periodType = item.lecPeriodType
            if l.place is not None:
                g.setExLecture(l)
            ###

            tut = Tutorial()
            t = Time()
            tut.instName = item.tut1InstName
            tut.courseName = item.tut1CrsName
            tut.place = item.tut1Place
            tut.type = item.tut1Type
            t.day = item.tut1Day
            t.fr = item.tut1From
            t.to = item.tut1To
            tut.setTime(t)
            tut.periodType = item.tut1PeriodType
            if tut.courseName is not None:
                g.add_tut(tut)

            tut = Tutorial()
            t = Time()
            tut.instName = item.tut2InstName
            tut.courseName = item.tut2CrsName
            tut.place = item.tut2Place
            tut.type = item.tut2Type
            t.day = item.tut2Day
            t.fr = item.tut2From
            t.to = item.tut2To
            tut.setTime(t)
            tut.periodType = item.tut2PeriodType
            if tut.courseName is not None:
                g.add_tut(tut)

            lab = Lab()
            t = Time()
            lab.instName = item.lab1InstName
            lab.courseName = item.lab1CrsName
            lab.place = item.lab1Place
            lab.type = item.lab1Type
            t.day = item.lab1Day
            t.fr = item.lab1From
            t.to = item.lab1To
            lab.setTime(t)
            lab.periodType = item.lab1PeriodType
            if lab.courseName is not None:
                g.add_lab(lab)

            lab = Lab()
            t = Time()
            lab.instName = item.lab2InstName
            lab.courseName = item.lab2CrsName
            lab.place = item.lab2Place
            lab.type = item.lab2Type
            t.day = item.lab2Day
            t.fr = item.lab2From
            t.to = item.lab2To
            lab.setTime(t)
            lab.periodType = item.lab2PeriodType
            if lab.courseName is not None:
                g.add_lab(lab)

            self.groups.append(g)

    def create(self):
        for group in self.groups:
            self.instructors.append(Instructor(group.lecture.instName, group.lecture.courseName, group))
        i = 0
        while i < len(self.instructors):
            inst = self.instructors[i]
            j = i + 1
            while j < len(self.instructors):
                if inst.name == self.instructors[j].name and inst.courseName == self.instructors[j].courseName:
                    inst.add_group(self.instructors[j].groups[0])
                    del self.instructors[j]
                else:
                    j += 1
            i += 1
        self.courses.append(Course(self.instructors[0].courseName, self.instructors[0]))
        for i in range(1, len(self.instructors)):
            inst = self.instructors[i]
            check = True
            for j in range(len(self.courses)):
                if inst.courseName == self.courses[j].name:
                    self.courses[j].add_instructor(inst)
                    check = False
            if check:
                self.courses.append(Course(inst.courseName, inst))

        for course in self.courses:
            course.term = 6
