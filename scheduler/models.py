from django.db import models

# Create your models here.


class Group(models.Model):
    department = models.CharField(max_length=256, default=None, blank=True, null=True)
    termNum = models.PositiveIntegerField(default=None, blank=True, null=True)
    creditHours = models.PositiveIntegerField(default=None, blank=True, null=True)
    groupNum = models.PositiveIntegerField(default=None, blank=True, null=True)
    #
    lecInstName = models.CharField(max_length=256, default=None, blank=True, null=True)
    lecCrsName = models.CharField(max_length=256, default=None, blank=True, null=True)
    lecPlace = models.CharField(max_length=256, default=None, blank=True, null=True)
    lecType = models.PositiveIntegerField(default=None, blank=True, null=True)
    lecDay = models.PositiveIntegerField(default=None, blank=True, null=True)
    lecFrom = models.PositiveIntegerField(default=None, blank=True, null=True)
    lecTo = models.PositiveIntegerField(default=None, blank=True, null=True)
    #
    lecExPlace = models.CharField(max_length=256, default=None, blank=True, null=True)
    lecExDay = models.PositiveIntegerField(default=None, blank=True, null=True)
    lecExFrom = models.PositiveIntegerField(default=None, blank=True, null=True)
    lecExTo = models.PositiveIntegerField(default=None, blank=True, null=True)
    #
    lecPeriodType = models.CharField(max_length=256, default=None, blank=True, null=True)
    #
    tut1InstName = models.CharField(max_length=256, default=None, blank=True, null=True)
    tut1CrsName = models.CharField(max_length=256, default=None, blank=True, null=True)
    tut1Place = models.CharField(max_length=256, default=None, blank=True, null=True)
    tut1Type = models.PositiveIntegerField(default=None, blank=True, null=True)
    tut1Day = models.PositiveIntegerField(default=None, blank=True, null=True)
    tut1From = models.PositiveIntegerField(default=None, blank=True, null=True)
    tut1To = models.PositiveIntegerField(default=None, blank=True, null=True)
    tut1PeriodType = models.CharField(max_length=256, default=None, blank=True, null=True)
    #
    tut2InstName = models.CharField(max_length=256, default=None, blank=True, null=True)
    tut2CrsName = models.CharField(max_length=256, default=None, blank=True, null=True)
    tut2Place = models.CharField(max_length=256, default=None, blank=True, null=True)
    tut2Type = models.PositiveIntegerField(default=None, blank=True, null=True)
    tut2Day = models.PositiveIntegerField(default=None, blank=True, null=True)
    tut2From = models.PositiveIntegerField(default=None, blank=True, null=True)
    tut2To = models.PositiveIntegerField(default=None, blank=True, null=True)
    tut2PeriodType = models.CharField(max_length=256, default=None, blank=True, null=True)
    #
    lab1InstName = models.CharField(max_length=256, default=None, blank=True, null=True)
    lab1CrsName = models.CharField(max_length=256, default=None, blank=True, null=True)
    lab1Place = models.CharField(max_length=256, default=None, blank=True, null=True)
    lab1Type = models.PositiveIntegerField(default=None, blank=True, null=True)
    lab1Day = models.PositiveIntegerField(default=None, blank=True, null=True)
    lab1From = models.PositiveIntegerField(default=None, blank=True, null=True)
    lab1To = models.PositiveIntegerField(default=None, blank=True, null=True)
    lab1PeriodType = models.CharField(max_length=256, default=None, blank=True, null=True)
    #
    lab2InstName = models.CharField(max_length=256, default=None, blank=True, null=True)
    lab2CrsName = models.CharField(max_length=256, default=None, blank=True, null=True)
    lab2Place = models.CharField(max_length=256, default=None, blank=True, null=True)
    lab2Type = models.PositiveIntegerField(default=None, blank=True, null=True)
    lab2Day = models.PositiveIntegerField(default=None, blank=True, null=True)
    lab2From = models.PositiveIntegerField(default=None, blank=True, null=True)
    lab2To = models.PositiveIntegerField(default=None, blank=True, null=True)
    lab2PeriodType = models.CharField(max_length=256, default=None, blank=True, null=True)
    #


class Instructor(models.Model):
    name = models.CharField(max_length=256, default=None, blank=True, null=True)
    courseName = models.CharField(max_length=256, default=None, blank=True, null=True)
    priority = models.PositiveIntegerField(default=None, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=256, default=None, blank=True, null=True)
    priority = models.PositiveIntegerField(default=None, blank=True, null=True)
    inst = models.ForeignKey(Instructor, on_delete=models.CASCADE)
