import uuid
from calendar import timegm
from datetime import datetime

# Rest Framework imports
from rest_framework_jwt.compat import get_username, get_username_field
from rest_framework_jwt.settings import api_settings

# Own models imports
# from authentication.models import Profile
from authentication.serializers import UserSerializer


# Include aditional data inside token payload
def jwt_payload_handler(user):

	# Set payload data
    payload = {
        'user_id': user.pk,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'user': UserSerializer(user).data,
    }
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


# Return username from payload
def jwt_get_username_from_payload_handler(payload):
    return payload['user'].get('username')