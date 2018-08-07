"""
Authentication views
"""
# Django imports
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Rest Framework imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
# JWT rest framework imports
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
# Own imports
from authentication.serializers import (UserSerializer, WebAppsSerializer,
                                        WebAppModulesSerializer, AccessAuditSerializer,
                                        AppAuditSerializer)
from authentication.models import (Profile, PasswordHistory,
                                   WebApps, WebAppModules,
                                   AccessAudit, AppAudit)
from authentication.utils import is_valid_new_password, save_last_login

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER # pylint: disable=invalid-name

# User view set
class UserViewSet(ModelViewSet): # pylint: too-many-ancestors
    """
    View to handle users data
    """
    # Get all users
    queryset = User.objects.all()
    # User serializer
    serializer_class = UserSerializer

    @action(methods=['post'], detail=True, url_path='change-password', url_name='change_password')
    def set_password(self, request, pk=None): # pylint: disable=invalid-name
        """
        View for password changing
        """
        # Get password info
        old_password = request.data["oldPassword"]
        new_password = request.data["newPassword"]
        repeat_new_password = request.data["repeatNewPassword"]
        # Get User Data
        user = User.objects.get(pk=pk)
        is_valid_password = is_valid_new_password(user, new_password)
        # If password is ok
        if (user.check_password(old_password)) and \
                                (new_password == repeat_new_password) and is_valid_password:
            # Change password
            user.set_password(new_password)
            user.save()
            # Edit first time profile
            user_profile = Profile.objects.get(user=user)
            user_profile.is_first_time = False
            user_profile.save()
            # Add new password to history
            user_history = PasswordHistory(user=user, password=make_password(new_password))
            user_history.save()
            return Response({'status': True})
        return Response({
            'status': False,
            'valid_password': is_valid_password
        })


class WebAppsViewSet(ModelViewSet):
    """
    Web apps viewset
    """
    queryset = WebApps.objects.all()
    serializer_class = WebAppsSerializer


class WebAppModulesViewSet(ModelViewSet):
    """
    Web app modules viewset
    """
    queryset = WebAppModules.objects.all()
    serializer_class = WebAppModulesSerializer


class AccessAuditViewSet(CreateAPIView):
    """
    Access Audit viewset
    """
    queryset = AccessAudit.objects.all()
    serializer_class = AccessAuditSerializer
    permission_classes = []


class AppAuditViewSet(CreateAPIView):
    """
    App Audit viewset
    """
    queryset = AppAudit.objects.all()
    serializer_class = AppAuditSerializer
    permission_classes = []


class CustomJSONWebTokenAPIView(JSONWebTokenAPIView):
    """
    Overide JWT Auth view
    """

    def check_valid_username(self, request, error):
        """
        Check if username is valid
        Validate user failed attempts
        """
        # Get username
        username = request.data['username']
        print(request.META)
        # If username exists, add one failed attempts
        try:
            # Get user
            user = User.objects.get(username=username)
            # Get user profile
            user_profile = Profile.objects.get(user=user)
            # Get login failed attempts
            failed_attempts = user_profile.failed_attempts
            # If it es less than 2 (4 because it is duplicated)
            if failed_attempts < 2 and user.is_active:
                # Add one failed atempts
                failed_attempts += 1
                user_profile.failed_attempts = failed_attempts
                # Save value
                user_profile.save()
                # Add error message
                error['failed_attempts_msg'] = \
                    'Usuario y clave no válidos. Número de intentos fallidos: '\
                        + str(int(user_profile.failed_attempts)) + ' (máximo 3)'
            # Block user
            else:
                # Add error message
                error['failed_attempts_msg'] = """Su usuario se encuentra
                                                  bloqueado. Por favor,
                                                  contactar al equipo de
                                                  Soluciones Ágiles para
                                                  su desbloqueo"""
                # Set active to false
                user.is_active = False
                user.save()
        except User.DoesNotExist:
            # If username is not valid
            error['failed_attempts_msg'] = 'El usuario indicado no posee una cuenta registrada'
        return error

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
            save_last_login(user)

            return Response(response_data)

        # Return custom response if not valid
        return Response(self.check_valid_username(request, serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# This view overrides
class CustomObtainJSONWebToken(CustomJSONWebTokenAPIView):
    """
    Set custom serializer class to get JWT token
    """
    serializer_class = JSONWebTokenSerializer


# Create custom get token api view
obtain_jwt_token = CustomObtainJSONWebToken.as_view()  # pylint: disable=invalid-name
