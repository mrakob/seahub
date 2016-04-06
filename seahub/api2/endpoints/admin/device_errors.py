import logging

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from seaserv import seafile_api
from pysearpc import SearpcError

from seahub.api2.authentication import TokenAuthentication
from seahub.api2.throttling import UserRateThrottle
from seahub.api2.utils import api_error

from seahub.utils.timeutils import timestamp_to_isoformat_timestr

logger = logging.getLogger(__name__)

class AdminDeviceErrors(APIView):
    """
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    throttle_classes = (UserRateThrottle, )
    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):
        return_results = []
        try:
            devices_errors = seafile_api.list_repo_sync_errors()
        except SearpcError as e:
            logger.error(e)
            error_msg = 'Internal Server Error'
            return api_error(status.HTTP_500_INTERNAL_SERVER_ERROR, error_msg)

        for error in devices_errors:
            result = {}
            result['email'] = error.email if error.email else ''
            result['peer_ip'] = error.peer_ip if error.peer_ip else ''
            result['peer_name'] = error.peer_name if error.peer_name else ''
            result['repo_name'] = error.repo_name if error.repo_name else ''
            result['repo_id'] = error.repo_id if error.repo_id else ''
            result['error_con'] = error.error_con if error.error_con else ''

            if error.error_time:
                result['error_time'] = timestamp_to_isoformat_timestr(error.error_time)
            else:
                result['error_time'] = ''

            return_results.append(result)

        return Response(return_results)
