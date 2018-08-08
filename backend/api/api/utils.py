"""
Override jwt auth methods
"""
import uuid
from calendar import timegm
from datetime import datetime
import jwt
# Rest Framework imports
from rest_framework_jwt.settings import api_settings
# Own models imports
from authentication.serializers import UserSerializer


def jwt_payload_handler(user):
    """
    Includes user profile into the payload handler
    """
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


def jwt_encode_handler(payload):
    """
    Overrides encode handler
    """
    key = get_private_key()

    return jwt.encode(
        payload,
        key,
        algorithm='RS256'
    ).decode('utf-8')


def jwt_decode_handler(token):
    """
    Overrides decode handler
    """
    options = {
        'verify_exp': api_settings.JWT_VERIFY_EXPIRATION,
    }

    key = get_public_key()

    return jwt.decode(
        token,
        key,
        api_settings.JWT_VERIFY,
        options=options,
        leeway=api_settings.JWT_LEEWAY,
        audience=api_settings.JWT_AUDIENCE,
        issuer=api_settings.JWT_ISSUER,
        algorithm='RS256'
    )


def jwt_get_username_from_payload_handler(payload): # pylint: disable=invalid-name
    """
    Returns the username from payload
    """
    return payload['user'].get('username')


def get_public_key():
    """
    Gets public key and convert to string
    """
    public_key = '-----BEGIN PUBLIC KEY-----\nMIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgFYQGeSzijOtbpdDQGYoP7k57hOx\ngNQeYj4CGYO/al/QdYAf38oGaRXhdkacmSxI2iBlUkQixdq35xtZsBDeScnJ0brK\nnJL1Ts4BbeaZDA7AjTmpZ3klvk4y0hErai4lM8+ydsrztHhcu1qY1+SNz4nCIaKX\na/MV4KFpWO/i3izHAgMBAAE=\n-----END PUBLIC KEY-----'
    return public_key


def get_private_key():
    """
    Gets private key and convert to string
    """
    private_key = '-----BEGIN RSA PRIVATE KEY-----\nMIICWwIBAAKBgFYQGeSzijOtbpdDQGYoP7k57hOxgNQeYj4CGYO/al/QdYAf38oG\naRXhdkacmSxI2iBlUkQixdq35xtZsBDeScnJ0brKnJL1Ts4BbeaZDA7AjTmpZ3kl\nvk4y0hErai4lM8+ydsrztHhcu1qY1+SNz4nCIaKXa/MV4KFpWO/i3izHAgMBAAEC\ngYBKhsbldVRIS/dopaQu0svb6n5wL1YQWf9ZExhlLm0/a5VUzkVM/SAjAosZuqIp\n5yx8wUDsH/CV5osK9C+za8sZIcQZY2PI+PasXPJ4Q1MlxnxjqDAUeOEMu0RLVE/6\n+5bm1e+zYR/GQBumkOAvQqYloQNGgKZfl1Y/2gqJtlFrgQJBAJYsSly8yhsy8r8h\nlV4A11nJ8gD0vY7n9k0E8S/40apiZPhsy+9KlmSDhrMSf6SXKXw1ba58HNkwDRIb\naLQ8AzsCQQCStiIWRKCqec11HRecI1qBrH/cUv3N4YFFEN3Cl1PpPDkV4vr4x4fl\nu6iuYiefbzDSnwTljw0G91lyHT/e50vlAkEAi01weZAixpI/PW8wuG99VGwREjP0\n9vBTuGRCOybLjwsQ8KUzk7iTw4+CTvB0+T/DmtWQ9c9pj0qUhVxphu84awJAOG9r\naVl43FsCV7ybKmrHE/7BKIWcMChAy8qTI5mGo7+QzgSEOlK2yf6IApyrVT82bq7Q\n+WUvw7A+bhEmUp5yqQJABA36tsYiUa6BR8GnhBaDGNl2q/xyJk8yjwBwcqPumP7T\n6lviopw6ndkLKpnXZr4yjgH3ZjZLfY5hbISovReydw==\n-----END RSA PRIVATE KEY-----'
    return private_key
