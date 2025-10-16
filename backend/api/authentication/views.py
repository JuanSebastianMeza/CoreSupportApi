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
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# Own imports
from authentication.serializers import (UserSerializer, WebAppsSerializer, WebAppModulesSerializer, GrantedAccessAuditSerializer, DeniedAccessAuditSerializer, AppAuditSerializer)
from authentication.models import (Profile, PasswordHistory,WebApps, WebAppModules,GrantedAccessAudit, DeniedAccessAudit,AppAudit)
from authentication.utils import is_valid_new_password, save_last_login

# jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER # pylint: disable=invalid-name

def custom_jwt_response_payload_handler(token, user=None, request=None):
    print(f"token: {token} for testing, user: {user}")
    return {
        'token': token,
        'user': {
            'username': user.username,
            'email': user.email,
        }
    }

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


class GrantedAccessAuditViewSet(CreateAPIView):
    """
    Access Audit viewset
    """
    queryset = GrantedAccessAudit.objects.all()
    serializer_class = GrantedAccessAuditSerializer
    permission_classes = []


class DeniedAccessAuditViewSet(CreateAPIView):
    """
    Access Audit viewset
    """
    queryset = DeniedAccessAudit.objects.all()
    serializer_class = DeniedAccessAuditSerializer
    permission_classes = []


class AppAuditViewSet(CreateAPIView):
    """
    App Audit viewset
    """
    queryset = AppAudit.objects.all()
    serializer_class = AppAuditSerializer
    permission_classes = []


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Override JWT Auth view
    """
    serializer_class = TokenObtainPairSerializer

    def check_valid_username(self, request, error):
        """
        Check if username is valid
        Validate user failed attempts
        """
        username = request.data['username']
        print(request.META)
        try:
            user = User.objects.get(username=username)
            user_profile = Profile.objects.get(user=user)
            failed_attempts = user_profile.failed_attempts
            if failed_attempts < 2 and user.is_active:
                failed_attempts += 1
                user_profile.failed_attempts = failed_attempts
                user_profile.save()
                error['failed_attempts_msg'] = 'Usuario y clave no válidos. Número de intentos fallidos: ' + str(int(user_profile.failed_attempts)) + ' (máximo 3)'
            else:
                error['failed_attempts_msg'] = """Su usuario se encuentra bloqueado. Por favor, contactar al equipo de Herramientas Operativas (cpsa.ve@telefonica.com) para su desbloqueo"""
                user.is_active = False
                user.save()
        except User.DoesNotExist:
            error['failed_attempts_msg'] = 'El usuario indicado no posee una cuenta registrada'
        return error

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token = serializer.validated_data['access']
            response_data = custom_jwt_response_payload_handler(token, user, request)
            save_last_login(user)
            user_profile = Profile.objects.get(user=user)
            user_profile.failed_attempts = 0
            user_profile.save()
            return Response(response_data)
        return Response(self.check_valid_username(request, serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class CustomGetAuthTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agrega claims personalizados
        # token['username'] = user.username
        # token['is_staff'] = user.is_staff
        # token['is_superuser'] = user.is_superuser
        # token['groups'] = list(user.groups.values_list('name', flat=True))
        # ...otros campos
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Incluye los datos que tu frontend espera
        user = self.user
        profile = getattr(user, 'profile', None)
        groups = list(user.groups.values_list('name', flat=True))
        permissions = list(user.user_permissions.values_list('codename', flat=True))
        # Si usas permisos por grupo:
        for group in user.groups.all():
            permissions += list(group.permissions.values_list('codename', flat=True))
        permissions = list(set(permissions))  # Quita duplicados

        data['user'] = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.get_full_name(),
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'groups': groups,
            'permissions': permissions,
            # Si tienes perfil extendido:
            'profile': {
                'is_first_time': getattr(profile, 'is_first_time', False),
                'last_password_change': getattr(profile, 'last_password_change', None),
                # agrega más campos si los necesitas
            } if profile else {},
            'last_login': user.last_login,
        }
        return data

class CustomGetAuthTokenView(TokenObtainPairView):
    serializer_class = CustomGetAuthTokenSerializer