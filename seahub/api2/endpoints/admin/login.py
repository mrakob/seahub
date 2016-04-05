from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from seahub.base.templatetags.seahub_tags import email2nickname
from seahub_extra.sysadmin_extra.models import UserLoginLog
from seahub.utils.timeutils import datetime_to_isoformat_timestr
from seahub.api2.authentication import TokenAuthentication
from seahub.api2.throttling import UserRateThrottle

class Login(APIView):

    authentication_classes = (TokenAuthentication, SessionAuthentication )
    permission_classes = (IsAdminUser,)
    throttle_classes = (UserRateThrottle,)

    def get(self, request):
        try:
            current_page = int(request.GET.get('page', '1'))
            per_page = int(request.GET.get('per_page', '100'))
        except ValueError:
            current_page = 1
            per_page = 100

        offset = per_page * (current_page - 1)
        limit = per_page + 1
        logs_plus_one = list(UserLoginLog.objects.all()[offset:offset + limit])
        logs = logs_plus_one[:per_page]

        result = []
        for log in logs:
            result.append({
                'id': log.id,
                'login_time': datetime_to_isoformat_timestr(log.login_date),
                'login_ip': log.login_ip,
                'name': email2nickname(log.username),
                'email':log.username
            })

        return Response(result)
