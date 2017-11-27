#coding:utf-8
from django.db import models

# Create your models here.
class Match(models.Model):
    weekday = models.CharField(max_length=20)
    number = models.IntegerField(default=101)
    time = models.CharField(max_length=5)
    host_team = models.CharField(max_length=40)
    away_team = models.CharField(max_length=40)
