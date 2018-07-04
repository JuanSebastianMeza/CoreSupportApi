# Django imports
from django.contrib.auth.models import User

# Rest Framework imports
from rest_framework import serializers

# JWT rest framework imports
from rest_framework_jwt.compat import *

# Own model imports
from authentication.models import Profile


# Profiles
class ProfileSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Profile
		fields = "__all__"


# User
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    # Get full name
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    # Get all permissions
    permissions = serializers.ListField(source='get_all_permissions', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'first_name', 'last_name', 'email', 'last_login', 'profile', 'permissions', 'is_staff', 'is_superuser')
