# Python imports
import datetime as dt

# Django imports
from django.contrib.auth.models import User

# Rest Framework imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

# JWT rest framework imports
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

# Own imports
from authentication.serializers import UserSerializer
from authentication.models import Profile

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

# User view set
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


# 
class CustomJSONWebTokenAPIView(JSONWebTokenAPIView):

	# Validate user failed attempts
	def check_valid_username(self, request, error):
		# Get username
		username = request.data['username']
		# If username exists, add one failed attempts
		try:
			# Get user
			user = User.objects.get(username=username)
			# Get user profile
			user_profile = Profile.objects.get(user=user)
			# Get login failed attempts
			failed_attempts = user_profile.failed_attempts
			# If it es less than 2 (4 because it is duplicated)
			if failed_attempts < 2:
				# Add one failed atempts
				failed_attempts += 1
				user_profile.failed_attempts = failed_attempts
				# Save value
				user_profile.save()
				# Add error message
				error['failed_attempts_msg'] = 'Usuario y clave no válidos. Número de intentos fallidos: ' + str(int(user_profile.failed_attempts)) + ' (máximo 3)'
			# Block user
			else:
				# Add error message
				error['failed_attempts_msg'] = 'Su usuario se encuentra bloqueado. Por favor, contactar al equipo de Soluciones Ágiles para su desbloqueo'
				# Set active to false
				user.is_active = False
				user.save()
		except:
			# If username is not valid
			error['failed_attempts_msg'] = 'El usuario indicado no posee una cuenta registrada'
		return error

	# Update failed attemps
	def update_failed_attempts(self, user):
		# Get user profile
		user_profile = Profile.objects.get(user=user)
		# Save previous failed attemps
		user_profile.previous_failed_attempts = user_profile.failed_attempts
		# Reset failed attemps
		user_profile.failed_attempts = 0
		user_profile.save(update_fields=['failed_attempts', 'previous_failed_attempts'])

	# Save last login date
	def save_last_login(self, user):
		user.last_login = dt.datetime.now()
		user.save(update_fields=['last_login'])

	# Override post method to include
	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(
			data=request.data
		)

		if serializer.is_valid():
			user = serializer.object.get('user') or request.user
			token = serializer.object.get('token')
			response_data = jwt_response_payload_handler(token, user, request)

			# Save last login
			self.save_last_login(user)

			# Update failed attempts
			self.update_failed_attempts(user)

			return Response(response_data)

		# Return custom response if not valid
		return Response(self.check_valid_username(request, serializer.errors), status=status.HTTP_400_BAD_REQUEST)


# This view overrides
class CustomObtainJSONWebToken(CustomJSONWebTokenAPIView):
    """
    Set custom serializer class to get JWT token
    """
    serializer_class = JSONWebTokenSerializer


# Create custom get token api view
obtain_jwt_token = CustomObtainJSONWebToken.as_view()