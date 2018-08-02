"""
Imports
"""
# Django imports
from django.contrib.auth.models import User
# Rest Framework imports
from rest_framework import serializers
# Own imports
from authentication.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profiles serializer
    """
    last_password_change = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ('user', 'position', 'department', 'failed_attempts', \
                    'is_first_time', 'last_password_change')


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    profile = ProfileSerializer(read_only=True)
    # Get full name
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    # Get all permissions
    permissions = serializers.ListField(source='get_all_permissions', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'first_name', 'last_name', 'email', \
                        'last_login', 'profile', 'permissions', 'is_staff', 'is_superuser')
