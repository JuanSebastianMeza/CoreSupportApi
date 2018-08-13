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
    def last_password_change(self):
        """
        Gets the latest password change date
        """
        from datetime import date
        return (date.today() - PasswordHistory.objects.filter(user=self.user) \
                        .order_by('-passwd_date').values_list('passwd_date')[0][0]).days


class Position(models.Model):
    """
	Position info
    """
    name = models.CharField(max_length=SHORT_TEXT)


class Department(models.Model):
    """
	Department info
    """
    name = models.CharField(max_length=SHORT_TEXT)


class PasswordHistory(models.Model):
    """
	Password history info
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=SHORT_TEXT)
    passwd_date = models.DateField(auto_now_add=True)


class WebApps(models.Model):
    """
	List of all SA web apps
    """
    name = models.CharField(max_length=SHORT_TEXT)


class WebAppModules(models.Model):
    """
	List all Apps modules
    """
    name = models.CharField(max_length=SHORT_TEXT)
    app = models.ForeignKey('WebApps', on_delete=models.DO_NOTHING)


class GrantedAccessAudit(models.Model):
    """
	Log of all granted accesses to SA apps
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey('WebApps', on_delete=models.DO_NOTHING)
    access_date = models.DateTimeField(auto_now_add=True)
    login_or_logout = models.BooleanField(default=True)
    # system = models.CharField(max_length=SHORT_TEXT, blank=True, default='')


class DeniedAccessAudit(models.Model):
    """
	Log of all denied accesses to SA apps
    """
    user = models.CharField(max_length=SHORT_TEXT)
    app = models.ForeignKey('WebApps', on_delete=models.DO_NOTHING)
    access_date = models.DateTimeField(auto_now_add=True)
    # system = models.CharField(max_length=SHORT_TEXT, blank=True, default='')


class AppAudit(models.Model):
    """
	Apps analitics
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_module = models.ForeignKey('WebAppModules', on_delete=models.DO_NOTHING)
    access_date = models.DateTimeField(auto_now_add=True)
