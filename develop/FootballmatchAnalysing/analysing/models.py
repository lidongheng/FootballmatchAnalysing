#coding:utf-8
from django.db import models

# Create your models here.
class League(models.Model):
    league = models.CharField(max_length=20)

class Team(models.Model):
    name = models.CharField(max_length=40)
    league = models.ForeignKey(League)
    note = models.CharField(max_length=400)

class Player(models.Model):
    name = models.CharField(max_length=200)
    team = models.CharField(max_length=40)
    homeland = models.CharField(max_length=40)
    main_position = models.CharField(max_length=2)
    main_position_short = models.CharField(max_length=2)
    current_position = models.CharField(max_length=3,null=True)
    other_position = models.CharField(max_length=3,null=True)
    another_pstion = models.CharField(max_length=3,null=True)
    tall = models.SmallIntegerField(default=0)
    weight = models.SmallIntegerField(default=0)
    game = models.SmallIntegerField(default=0)
    first = models.SmallIntegerField(default=0)
    substitute = models.SmallIntegerField(default=0)
    goal = models.SmallIntegerField(default=0)
    assists = models.SmallIntegerField(default=0)
    yellowcard = models.SmallIntegerField(default=0)
    redcard = models.SmallIntegerField(default=0)
    other = models.CharField(max_length=200)
    note = models.CharField(max_length=400)

class PremierLeague(models.Model):
	  team = models.ForeignKey(Team)
    round = models.SmallIntegerField(default=0)
    win = models.SmallIntegerField(default=0)
    tie = models.SmallIntegerField(default=0)
    defeat = models.SmallIntegerField(default=0)
    goal = models.SmallIntegerField(default=0)
    lose = models.SmallIntegerField(default=0)
    diff = models.SmallIntegerField(default=0)
    point = models.SmallIntegerField(default=0)

class LaLiga(models.Model):
    team = models.ForeignKey(Team)
    round = models.SmallIntegerField(default=0)
    win = models.SmallIntegerField(default=0)
    tie = models.SmallIntegerField(default=0)
    defeat = models.SmallIntegerField(default=0)
    goal = models.SmallIntegerField(default=0)
    lose = models.SmallIntegerField(default=0)
    diff = models.SmallIntegerField(default=0)
    point = models.SmallIntegerField(default=0)

class SerieA(models.Model):
    team = models.ForeignKey(Team)
    round = models.SmallIntegerField(default=0)
    win = models.SmallIntegerField(default=0)
    tie = models.SmallIntegerField(default=0)
    defeat = models.SmallIntegerField(default=0)
    goal = models.SmallIntegerField(default=0)
    lose = models.SmallIntegerField(default=0)
    diff = models.SmallIntegerField(default=0)
    point = models.SmallIntegerField(default=0)

class Bundesliga(models.Model):
    team = models.ForeignKey(Team)
    round = models.SmallIntegerField(default=0)
    win = models.SmallIntegerField(default=0)
    tie = models.SmallIntegerField(default=0)
    defeat = models.SmallIntegerField(default=0)
    goal = models.SmallIntegerField(default=0)
    lose = models.SmallIntegerField(default=0)
    diff = models.SmallIntegerField(default=0)
    point = models.SmallIntegerField(default=0)

class Bundesliga(models.Model):
    team = models.ForeignKey(Team)
    round = models.SmallIntegerField(default=0)
    win = models.SmallIntegerField(default=0)
    tie = models.SmallIntegerField(default=0)
    defeat = models.SmallIntegerField(default=0)
    goal = models.SmallIntegerField(default=0)
    lose = models.SmallIntegerField(default=0)
    diff = models.SmallIntegerField(default=0)
    point = models.SmallIntegerField(default=0)

class Franchleaue(models.Model):
    team = models.ForeignKey(Team)
    round = models.SmallIntegerField(default=0)
    win = models.SmallIntegerField(default=0)
    tie = models.SmallIntegerField(default=0)
    defeat = models.SmallIntegerField(default=0)
    goal = models.SmallIntegerField(default=0)
    lose = models.SmallIntegerField(default=0)
    diff = models.SmallIntegerField(default=0)
    point = models.SmallIntegerField(default=0)

class JLeague(models.Model):
    team = models.ForeignKey(Team)
    round = models.SmallIntegerField(default=0)
    win = models.SmallIntegerField(default=0)
    tie = models.SmallIntegerField(default=0)
    defeat = models.SmallIntegerField(default=0)
    goal = models.SmallIntegerField(default=0)
    lose = models.SmallIntegerField(default=0)
    diff = models.SmallIntegerField(default=0)
    point = models.SmallIntegerField(default=0)

class ChinaFootballLeague(models.Model):
    team = models.ForeignKey(Team)
    round = models.SmallIntegerField(default=0)
    win = models.SmallIntegerField(default=0)
    tie = models.SmallIntegerField(default=0)
    defeat = models.SmallIntegerField(default=0)
    goal = models.SmallIntegerField(default=0)
    lose = models.SmallIntegerField(default=0)
    diff = models.SmallIntegerField(default=0)
    point = models.SmallIntegerField(default=0)