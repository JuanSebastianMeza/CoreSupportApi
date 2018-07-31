# Django imports
from django.contrib.auth.hashers import check_password

# Own imports
from authentication.models import PasswordHistory


# Returns if new password don't match with previous 10 passwords
def is_valid_new_password(user, passwd):
    # Get user previous passwords
    last_passwd = PasswordHistory.objects.filter(user=user) \
                        .order_by('-passwd_date').values_list('password')[:10]
    print(last_passwd)
    # Check if password is in array
    for password in last_passwd:
        print(password)
        print(password[0])
        if check_password(passwd, password[0]):
            return False
    return True
