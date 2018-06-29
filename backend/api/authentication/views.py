from django.shortcuts import render
from django.contrib.auth.models import User

# Rest Framework imports
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.viewsets import ModelViewSet

# Own imports
from authentication.serializers import UserSerializer


class UserViewSet(ModelViewSet):
	# Get all users
	queryset = User.objects.all()
	# User serializer
	serializer_class = UserSerializer

	@action(methods=['post'], detail=True, url_path='change-password', url_name='change_password')
	def set_password(self, request, pk=None):
		# Get password info
		old_password = request.data["oldPassword"]
		new_password = request.data["newPassword"]
		repeat_new_password = request.data["repeatNewPassword"]
		# Get User Data
		user = User.objects.get(pk=pk)
		# If password is ok
		if (user.check_password(old_password)) and (new_password == repeat_new_password):
			# Change password
			user.set_password(new_password)
			user.save()
			return Response({'status': True})
		else:
			return Response({'status': False})
