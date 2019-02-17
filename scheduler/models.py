from django.db import models

# Create your models here.


class Group(models.Model):

    groupNum = models.PositiveIntegerField()
    
    lecInstName = models.CharField(max_length=256)
    lecCrsName = models.CharField(max_length=256)
    lecPlace = models.CharField(max_length=256)
    lecType = models.PositiveIntegerField()
    lecDay = models.PositiveIntegerField()
    lecFrom = models.PositiveIntegerField()
    lecTo = models.PositiveIntegerField()
    lecPeriodType = models.CharField(max_length=256)
    
    tut1InstName = models.CharField(max_length=256)
    tut1CrsName = models.CharField(max_length=256)
    tut1Place = models.CharField(max_length=256)
    tut1Type = models.PositiveIntegerField()
    tut1Day = models.PositiveIntegerField()
    tut1From = models.PositiveIntegerField()
    tut1To = models.PositiveIntegerField()
    tut1PeriodType = models.CharField(max_length=256)
    
    tut2InstName = models.CharField(max_length=256)
    tut2CrsName = models.CharField(max_length=256)
    tut2Place = models.CharField(max_length=256)
    tut2Type = models.PositiveIntegerField()
    tut2Day = models.PositiveIntegerField()
    tut2From = models.PositiveIntegerField()
    tut2To = models.PositiveIntegerField()
    tut2PeriodType = models.CharField(max_length=256)
    
    lab1InstName = models.CharField(max_length=256)
    lab1CrsName = models.CharField(max_length=256)
    lab1Place = models.CharField(max_length=256)
    lab1Type = models.PositiveIntegerField()
    lab1Day = models.PositiveIntegerField()
    lab1From = models.PositiveIntegerField()
    lab1To = models.PositiveIntegerField()
    lab1PeriodType = models.CharField(max_length=256)
    
    lab2InstName = models.CharField(max_length=256)
    lab2CrsName = models.CharField(max_length=256)
    lab2Place = models.CharField(max_length=256)
    lab2Type = models.PositiveIntegerField()
    lab2Day = models.PositiveIntegerField()
    lab2From = models.PositiveIntegerField()
    lab2To = models.PositiveIntegerField()
    lab2PeriodType = models.CharField(max_length=256)
