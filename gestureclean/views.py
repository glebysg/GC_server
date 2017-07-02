import warnings
from django.conf import settings
from django.contrib.auth import (
    get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from . import forms
from rolepermissions.roles import get_user_roles



@sensitive_post_parameters()
@csrf_protect
@never_cache
def user_login(request, template_name='vacs/login.html',
          current_app=None, extra_context=None):

    if request.method == "POST":
        form = forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())
            role = get_user_roles(user)
            if role is 'researcher':
                return HttpResponseRedirect('/')
            elif role is 'participant':
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')
    else:
        form = forms.LoginForm()

    current_site = get_current_site(request)

    context = {
        'form': form,
        'redirect_field_name': '/',
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)
