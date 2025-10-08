from rest_framework.exceptions import APIException
from rest_framework import status


class ThirdPartyAPIException(APIException):
   status_code = status.HTTP_503_SERVICE_UNAVAILABLE
   default_detail = 'Third party service error'
   default_code = 'third_party_error'

class BusinessLogicException(APIException):
   status_code = status.HTTP_400_BAD_REQUEST
   default_detail = 'Business logic error'
   default_code = 'business_logic_error'