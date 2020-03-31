from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from colossus.apps.accounts.forms import UserForm
from .models import User
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
from onelogin.saml2.auth import OneLogin_Saml2_Auth


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    This is the class for displaying the user profile.
    """
    model = User
    form_class = UserForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        """
        This getter function gets the user object.
        """
        return self.request.user


def prepare_django_request(request):
    """
    A function to get information about the host.
    """

    http_host = None
    script_name = None
    server_port = None

    if 'HTTP_HOST' in request.META:
        http_host = request.META["HTTP_HOST"]
    if 'PATH_INFO' in request.META:
        script_name = request.META["PATH_INFO"]
    if 'SERVER_PORT' in request.META:
        server_port = request.META["SERVER_PORT"]
    result = {
        "https": "on" if request.is_secure() else "off",
        "http_host": http_host,
        "script_name": script_name,
        "server_port": server_port,
        "get_data": request.GET.copy(),
        "post_data": request.POST.copy()
    }
    return result


def initialize_saml(request):
    """
    A function to initialize the OneLogin Auth using the Http request.
    """

    auth = OneLogin_Saml2_Auth(request, custom_base_path=settings.SAML_FOLDER)
    return auth


def login(request):
    """
    A function to actually authenticate the user using SAML.
    """

    req = prepare_django_request(request)
    auth = initialize_saml(req)
    errors = []
    error_reason = None
    success_slo = False
    attributes = False

    if "sso" in req["get_data"]:
        return HttpResponseRedirect(auth.login())

    elif "slo" in req["get_data"]:
        pass

    elif "acs" in req["get_data"]:
        pass

    elif "sls" in req["get_data"]:
        pass

    return render(request, "registration/login.html", {"errors": errors, "error_reason": error_reason,
                  "success_slo": success_slo, "attributes": attributes})


def metadata(request):
    """
    A function to return the metadata of the Service Provider.
    """
    pass
