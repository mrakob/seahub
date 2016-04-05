from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from seahub.api2.authentication import TokenAuthentication
from seahub.api2.throttling import UserRateThrottle
from seahub.api2.utils import api_error

from seahub.base.templatetags.seahub_tags import email2nickname
from seahub.utils.timeutils import datetime_to_isoformat_timestr
from seahub.utils import EVENTS_ENABLED, get_perm_audit_events

class PermAudit(APIView):

    authentication_classes = (TokenAuthentication, SessionAuthentication )
    permission_classes = (IsAdminUser,)
    throttle_classes = (UserRateThrottle,)

    def get(self, request):

        if not EVENTS_ENABLED:
            error_msg = 'Permission denied.'
            return api_error(status.HTTP_403_FORBIDDEN, error_msg)

        # Make sure page request is an int. If not, deliver first page.
        try:
            current_page = int(request.GET.get('page', '1'))
            per_page = int(request.GET.get('per_page', '100'))
        except ValueError:
            current_page = 1
            per_page = 100

        user_selected = request.GET.get('email', None)
        repo_selected = request.GET.get('repo_id', None)

        start = per_page * (current_page - 1)
        limit = per_page

        events = get_perm_audit_events(user_selected, 0, repo_selected, start, limit)

        result = []
        if events:
            for ev in events:
                result.append({
                    'etype': ev.etype,
                    'repo_id': ev.repo_id,
                    'permission': ev.permission,
                    'time': datetime_to_isoformat_timestr(ev.timestamp),
                    'file_path': ev.file_path,
                    'from_name': email2nickname(ev.from_user),
                    'from_email': ev.from_user,
                    'to': ev.to
                })

        return Response(result)
