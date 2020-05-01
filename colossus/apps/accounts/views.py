import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView
from colossus.apps.accounts.forms import UserForm
from .models import User
from django.utils.decorators import method_decorator
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseServerError)
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from django.contrib.auth import get_user_model, login, logout
from django.middleware.csrf import get_token
from . import constants
logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
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


@csrf_exempt
def initialize_saml(request):
    """
    A function to initialize the OneLogin Auth using the Http request.
    """
    logger.info("Inside Initialize SAML")
    auth = OneLogin_Saml2_Auth(request, custom_base_path=settings.SAML_FOLDER)
    return auth


@csrf_exempt
def ssoLogin(request):
    """
    A function to actually authenticate the user using SAML.
    """
    logger.info("Inside SSO Login Function")
    req = prepare_django_request(request)
    auth = initialize_saml(req)
    errors = []
    error_reason = None
    success_slo = False
    attributes = False
    paint_logout = False
    not_auth_warn = False

    logger.info("Original request : {}".format(request))
    logger.info("Django request : {}".format(req))

    if "sso" in req["get_data"]:
        logger.info("Inside SSO")
        if 'next' in request.POST:
            target_url = req['post_data']['next']
        else:
            target_url = '/'
        return HttpResponseRedirect(auth.login(return_to=target_url))

    elif "slo" in req["get_data"]:
        logger.info("Inside SLO")
        name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
        logger.info("Request Session : {}".format(request.session))
        if 'samlNameId' in request.session:
            name_id = request.session['samlNameId']
        if 'samlSessionIndex' in request.session:
            session_index = request.session['samlSessionIndex']
        if 'samlNameIdFormat' in request.session:
            name_id_format = request.session['samlNameIdFormat']
        if 'samlNameIdNameQualifier' in request.session:
            name_id_nq = request.session['samlNameIdNameQualifier']
        if 'samlNameIdSPNameQualifier' in request.session:
            name_id_spnq = request.session['samlNameIdSPNameQualifier']

        logout(request)
        logger.info("Logged out!")
        return HttpResponseRedirect(
            auth.logout(name_id=name_id, session_index=session_index, nq=name_id_nq, name_id_format=name_id_format,
                        spnq=name_id_spnq))

    elif "acs" in req["get_data"]:
        logger.info("Inside ACS")
        request_id = None
        if 'AuthNRequestID' in request.session:
            logger.info("Inside AuthRequestID")
            request_id = request.session['AuthNRequestID']

        auth.process_response(request_id=request_id)
        errors = auth.get_errors()
        not_auth_warn = not auth.is_authenticated()

        if not errors:
            if 'AuthNRequestID' in request.session:
                del request.session['AuthNRequestID']
            request.session['samlUserdata'] = auth.get_attributes()
            request.session['samlNameId'] = auth.get_nameid()
            request.session['samlNameIdFormat'] = auth.get_nameid_format()
            request.session['samlNameIdNameQualifier'] = auth.get_nameid_nq()
            request.session['samlNameIdSPNameQualifier'] = auth.get_nameid_spnq()
            request.session['samlSessionIndex'] = auth.get_session_index()
            logger.info("Printing Session data {} ".format(request.session.items()))
            logger.info("Relay state : {}".format(req['post_data']['RelayState']))
            logger.info("Self URL : {}".format(OneLogin_Saml2_Utils.get_self_url(req)))
            allUsers = get_user_model()
            logger.info("djm746 allUsers {}".format(allUsers))
            oldUser = False
            currentUser = None
            sessionAttributes = request.session
            currentUserGUID = sessionAttributes["samlUserdata"]["GUID"][0]
            currentUserEmail = sessionAttributes["samlUserdata"]["mail"][0]
            currentUserName = sessionAttributes["samlUserdata"]["givenName"][0]

            if currentUserEmail not in constants.permittedUserAccounts:
                return HttpResponseRedirect(reverse('accounts:sso_login'))

            if allUsers is not None:
                logger.info("djm746 inside allUsers is not None")
                for u in allUsers.objects.all():
                    logger.info("djm746 inside allUsers")
                    logger.info("USER DETAILS {}".format(u.get_username()))
                    if(u.get_username() == currentUserEmail):
                        logger.info("User {} found".format(currentUserGUID))
                        login(request, u)
                        oldUser = True
                        currentUser = u
                        break
            if(oldUser is False):
                logger.info("djm746 new user")
                logger.info("New user email : {}".format(currentUserEmail))
                logger.info('Creating new user directly')
                currentUser = User.objects.create_user(
                    email=currentUserEmail,
                    password=str(currentUserGUID)[::-1],
                    username=currentUserEmail,
                    first_name=currentUserName,
                    last_name=currentUserName
                )
                logger.info('Created new user')
                logger.info('Logging in new user : {}'.format(currentUser))
                login(request, currentUser)
                logger.info('Logged in')
            logger.info("Current USER DETAILS {}".format(currentUser))

            if 'RelayState' in req['post_data']:
                logger.info("Inside Relay State")
                return HttpResponseRedirect(auth.redirect_to(req['post_data']['RelayState']))
        elif auth.get_settings().is_debug_active():
            logger.info("Is Debug Active")
            error_reason = auth.get_last_error_reason()

    elif "sls" in req["get_data"]:
        logger.info("Inside SLS")
        request_id = None
        if "LogoutRequestID" in request.session:
            logger.info("Inside LogoutRequestID")
            request_id = request.session["LogoutRequestID"]
        dscb = request.session.flush()
        url = auth.process_slo(request_id=request_id, delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                return HttpResponseRedirect(url)
            else:
                success_slo = True
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()

    if "samlUserdata" in request.session:
        print("Inside SAML USER DATA")
        paint_logout = True
        if len(request.session["samlUserdata"]) > 0:
            attributes = request.session["samlUserdata"].items()
            logger.info("Attributes : {}".format(attributes))

    logger.info("Errors : {}".format(errors))
    logger.info("Error Reason : {}".format(error_reason))
    logger.info("Not Auth Warn : {}".format(not_auth_warn))
    logger.info("Success Slo : {}".format(success_slo))
    logger.info("Attributes : {}".format(attributes))
    logger.info("Paint Loout : {}".format(paint_logout))

    csrftoken = get_token(request)
    logger.info("ANOTHER CSRF TOKEN VALUE {}".format(csrftoken))
    response = render(request, "registration/login.html",
                      {"errors": errors, "error_reason": error_reason, "not_auth_warn": not_auth_warn,
                       "success_slo": success_slo, "attributes": attributes, "paint_logout": paint_logout})
    response.set_cookie(key='csrftoken', value=csrftoken)
    return response


def metadata(request):
    """
    A function to return the metadata of the Service Provider.
    """
    saml_settings = OneLogin_Saml2_Settings(settings=None, custom_base_path=settings.SAML_FOLDER,
                                            sp_validation_only=True)
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = HttpResponse(content=metadata, content_type="text/xml")
    else:
        resp = HttpResponseServerError(content=", ".join(errors))
    return resp


@login_required()
def attributes(request):
    """
    A function to return the user's session attributes
    """
    paint_logout = False
    attributes = False

    if 'samlUserdata' in request.session:
        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()
    return render(request, 'accounts/attributes.html',
                  {'paint_logout': paint_logout,
                   'attributes': attributes})
