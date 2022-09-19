from django.db import models
from django.utils.html import mark_safe

# Create your models here.

long_char = 300
short_char = 50
json_char = 1000

class Participant(models.Model):

	name    = models.CharField(max_length=long_char,  blank=True)
	school  = models.CharField(max_length=long_char,  blank=True)
	grade   = models.CharField(max_length=short_char, blank=True)
	phone   = models.CharField(max_length=short_char, blank=True)
	birthday   = models.DateField(blank=True)
	docs    = models.FileField(upload_to='files/', null=True)

	def __str__(self):
		return self.name

class Team(models.Model):

	teamname   = models.CharField(max_length=long_char,  blank=True)
	school  = models.CharField(max_length=long_char,  blank=True)
	leader  = models.CharField(max_length=long_char,  blank=True)
	phone   = models.CharField(max_length=short_char, blank=True)
	docs    = models.FileField(upload_to='files/', null=True)

	def __str__(self):
		return self.teamname

class Member(models.Model):

	team    = models.ForeignKey(Team, on_delete=models.CASCADE)
	name    = models.CharField(max_length=long_char,  blank=True)
	grade   = models.CharField(max_length=short_char, blank=True)
	birthday   = models.DateField(blank=True)

	def __str__(self):
		return self.name
