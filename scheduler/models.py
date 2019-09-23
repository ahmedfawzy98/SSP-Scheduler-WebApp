from django.db import models

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=256, default=None, blank=True, null=True)
    priority = models.PositiveIntegerField(default=None, blank=True, null=True)
    term = models.PositiveIntegerField(default=None, blank=True, null=True)
    creditHours = models.PositiveIntegerField(default=None, blank=True, null=True)
    department = models.CharField(max_length=256, default=None, blank=True, null=True)
    instructors = None

    def keep_first(self):
        first = self.instructors[0]
        for inst in self.instructors:
            if inst.id != first.id:
                self.instructor_set.remove(inst)

    def build(self):
        self.instructors = list(self.instructor_set.all())
        for inst in self.instructors:
            inst.build()


class Instructor(models.Model):
    name = models.CharField(max_length=256, default=None, blank=True, null=True)
    priority = models.PositiveIntegerField(default=None, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None, blank=True, null=True)
    groups = None

    def build(self):
        self.groups = list(self.group_set.all())
        for group in self.groups:
            group.build()


class Group(models.Model):
    groupNum = models.PositiveIntegerField(default=None, blank=True, null=True)
    inst = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=None, blank=True, null=True)
    available = models.BooleanField(default=True)
    lecture = None
    exLecture = None
    tutorials = None
    labs = None

    def build(self):
        self.lecture = list(self.lecture_set.all())[0]
        self.tutorials = list(self.tutorial_set.all())
        self.labs = list(self.lab_set.all())
        self.exLecture = list(self.lecture.exlecture_set.all())[0] if list(self.lecture.exlecture_set.all()) else None
        self.lecture.build()
        if self.exLecture is not None:
            self.exLecture.build()
        for tut in self.tutorials:
            tut.build()
        for lab in self.labs:
            lab.build()


class Lecture(models.Model):
    place = models.CharField(max_length=256, default=None, blank=True, null=True)
    type = models.PositiveIntegerField(default=None, blank=True, null=True)
    periodType = models.CharField(max_length=256, default=None, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None, blank=True, null=True)
    time = None

    def length(self):
        return self.time.time_to - self.time.time_from + 1

    def instName(self):
        return self.group.inst.name

    def courseName(self):
        return self.group.inst.course.name

    def build(self):
        self.time = list(self.time_set.all())[0]


class ExLecture(models.Model):
    Place = models.CharField(max_length=256, default=None, blank=True, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, default=None, blank=True, null=True)
    time = None

    def length(self):
        return self.time.time_to - self.time.time_from + 1

    def instName(self):
        return self.lecture.group.inst.name

    def courseName(self):
        return self.lecture.group.inst.course.name

    def build(self):
        self.time = list(self.time_set.all())[0]


class Tutorial(models.Model):
    place = models.CharField(max_length=256, default=None, blank=True, null=True)
    type = models.PositiveIntegerField(default=None, blank=True, null=True)
    periodType = models.CharField(max_length=256, default=None, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None, blank=True, null=True)
    time = None
    length = None

    def length(self):
        return self.time.time_to - self.time.time_from + 1

    def instName(self):
        return self.group.inst.name

    def courseName(self):
        return self.group.inst.course.name

    def build(self):
        self.time = list(self.time_set.all())[0]


class Lab(models.Model):
    place = models.CharField(max_length=256, default=None, blank=True, null=True)
    type = models.PositiveIntegerField(default=None, blank=True, null=True)
    periodType = models.CharField(max_length=256, default=None, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None, blank=True, null=True)
    time = None

    def length(self):
        return self.time.time_to - self.time.time_from + 1

    def instName(self):
        return self.group.inst.name

    def courseName(self):
        return self.group.inst.course.name

    def build(self):
        self.time = list(self.time_set.all())[0]


class Time(models.Model):
    time_day = models.PositiveIntegerField(default=None, blank=True, null=True)
    time_from = models.PositiveIntegerField(default=None, blank=True, null=True)
    time_to = models.PositiveIntegerField(default=None, blank=True, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, default=None, blank=True, null=True)
    exlecture = models.ForeignKey(ExLecture, on_delete=models.CASCADE, default=None, blank=True, null=True)
    tut = models.ForeignKey(Tutorial, on_delete=models.CASCADE, default=None, blank=True, null=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, default=None, blank=True, null=True)

