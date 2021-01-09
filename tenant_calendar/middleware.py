import pytz
from django.utils import timezone


def set_timezone(get_response):

    def middleware(request):
        if request.user.is_authenticated:
            if request.user.default_timezone:
                timezone.activate(
                    pytz.timezone(request.user.default_timezone)
                )
            else:
                timezone.activate('UTC')
        else:
            timezone.deactivate()
        return get_response(request)
    return middleware
