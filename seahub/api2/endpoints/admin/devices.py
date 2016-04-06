import logging

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from seahub.utils.devices import get_devices

from seahub.api2.authentication import TokenAuthentication
from seahub.api2.throttling import UserRateThrottle

logger = logging.getLogger(__name__)

class AdminDevices(APIView):
    """
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    throttle_classes = (UserRateThrottle, )
    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):

        try:
            current_page = int(request.GET.get('page', '0'))
            per_page = int(request.GET.get('per_page', '100'))
        except ValueError:
            current_page = 0
            per_page = 100

        start = current_page * per_page
        limit = (current_page + 1) * per_page
        devices = get_devices(start, limit)

        return Response(devices)
