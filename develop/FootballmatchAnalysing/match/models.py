#coding:utf-8
from django.db import models

# Create your models here.
class Recentmatch(models.Model):
    weekday = models.CharField(max_length=20)
    number = models.IntegerField(default=101)
    time = models.CharField(max_length=30)
    host_team = models.CharField(max_length=40)
    away_team = models.CharField(max_length=40)

class Historymatch(models.Model):
    date = models.CharField(max_length=30)
    league = models.CharField(max_length=20)
    host_team = models.CharField(max_length=40)
    host_goal = models.SmallIntegerField(default=0)
    away_team = models.CharField(max_length=40)
    away_goal = models.SmallIntegerField(default=0)
    handicap = models.CharField(max_length=16,null=True)
    handicap_result = models.CharField(max_length=4,null=True)

class Futurematch(models.Model):
    date = models.CharField(max_length=30)
    league = models.CharField(max_length=20)
    host_team = models.CharField(max_length=40)
    host_goal = models.SmallIntegerField(default=0)
    away_team = models.CharField(max_length=40)
    away_goal = models.SmallIntegerField(default=0)
    handicap = models.CharField(max_length=16,null=True)
    handicap_result = models.CharField(max_length=4,null=True)

class Odd(models.Model):
    match = models.ForeignKey(Historymatch)
    text = models.TextField()

class Log(models.Model):
    accident = models.CharField(max_length=40)
    datetime = models.DateTimeField(auto_now_add=True)
    next_time_period = models.SmallIntegerField(default=10)
    note = models.CharField(max_length=400)

