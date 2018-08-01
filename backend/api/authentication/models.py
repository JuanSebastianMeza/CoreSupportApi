"""
Django imports
"""
from django.db import models
from django.contrib.auth.models import User

SHORT_TEXT = 128


class Profile(models.Model):
    """
	Profile info
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.ForeignKey('Position', on_delete=models.DO_NOTHING)
    department = models.ForeignKey('Department', on_delete=models.DO_NOTHING)
    failed_attempts = models.IntegerField(default=0)
    is_first_time = models.BooleanField(default=True)

    @property
    def last_passwrd_change(self):
        """
        Gets the latest password change date
        """
        return PasswordHistory.objects.filter(user=self.user) \
                        .order_by('-passwd_date').values_list('passwd_date')[0][0]


# Department Position
class Position(models.Model):
    """
	Position info
    """
    name = models.CharField(max_length=SHORT_TEXT)


# Telefónica Department
class Department(models.Model):
    """
	Department info
    """
    name = models.CharField(max_length=SHORT_TEXT)


# Password history
class PasswordHistory(models.Model):
    """
	Password history info
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=SHORT_TEXT)
    passwd_date = models.DateField(auto_now_add=True)
	