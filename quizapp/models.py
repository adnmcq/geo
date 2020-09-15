from django.db import models

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

Q_URL =  'q/'
T_URL =  't/'


class Team(models.Model):
    name = models.CharField(max_length=200)
    pic = models.ImageField(upload_to=T_URL, null=True, blank=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Quiz(models.Model):
    date = models.DateTimeField('date')
    games = models.ManyToManyField(Team, through='Game')

    def __str__(self):
        return '#%s - %s'%(self.id, self.date)

class Game(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    def __str__(self):
        return '#%s - %s, %s %s Pts'%(self.quiz.id, self.quiz.date, self.team.name, self.points)

ROUNDS= [
    ('ff', 'Fact or Fiction'),
    ('gk', 'General Knowledge'),
    ('pic', 'Picture Round'),
    ('aud', 'Audio Round'),
    ('sp', 'Spotlight Round'),
    ('an', 'Analysis Round'),
    ('b', 'Bonus Round'),
]

class Round(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    type = models.CharField(max_length=200, choices = ROUNDS)

    def __str__(self):
        return self.type

class Question(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to=Q_URL, null=True, blank=True)



