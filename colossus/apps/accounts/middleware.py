from django.utils import timezone

import pytz
from pytz import UnknownTimeZoneError


class UserTimezoneMiddleware:
    """
    This is a middleware class for user timezones.
    """
    def __init__(self, get_response):
        """
        An init function to define self.get_response
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        A function to set the timezone of user and get response from the server.

        Keyword arguments:
        request -- The http request object

        Returns:
        response -- The http response object
        """
        if request.user.is_authenticated:
            try:
                timezone.activate(pytz.timezone(request.user.timezone))
            except UnknownTimeZoneError:
                timezone.deactivate()

        response = self.get_response(request)
        return response
