"""
Utils imports
"""
# Python imports
import datetime as dt
# Django imports
from django.contrib.auth.hashers import check_password
# Own imports
from authentication.models import PasswordHistory


def is_valid_new_password(user, passwd):
    """
    Returns if new password don't match with previous 10 passwords
    """
    # Get user previous passwords
    last_passwd = PasswordHistory.objects.filter(user=user) \
                        .order_by('-passwd_date').values_list('password')[:10]
    # Check if password is in array
    for password in last_passwd:
        if check_password(passwd, password[0]):
            return False
    return True

# Save last login date
def save_last_login(user):
    """
    Saves user last login date
    """
    user.last_login = dt.datetime.utcnow()
    user.save(update_fields=['last_login'])
