from django.db import models
from django.contrib.auth.models import User

short_text = 100

# Profiles
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	position = models.ForeignKey('Position', on_delete=models.DO_NOTHING)
	department = models.ForeignKey('Department', on_delete=models.DO_NOTHING)
	failed_attempts = models.IntegerField(default=0)


# Department Position
class Position(models.Model):
	name = models.CharField(max_length=short_text)


# Telefónica Department
class Department(models.Model):
	name = models.CharField(max_length=short_text)