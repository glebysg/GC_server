import warnings
from django.conf import settings
from django.contrib.auth import (
    get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url, redirect
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
from django.contrib.auth import get_user_model
from rolepermissions.checkers import has_role
from vacs.models import Participant, Assignment, Vac
from django.contrib.auth import logout
User = get_user_model()

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
            user = User.objects.get(pk=form.get_user_id())
            if has_role(user,'researcher'):
                print "%%%%%%%%%%%%%%% R %%%%%%%%%%%%%%%%"
                return HttpResponseRedirect('/vacs/experiments')
            elif has_role(user,['student','expert'] ):
                print "%%%%%%%%%%%%%%% P %%%%%%%%%%%%%%%%"
		# if the current vac is null, add the first one on the list
		participant = Participant.objects.get(user=user)
		# Get the assignments that are not done
		assignments = Assignment.objects.filter(
			user = user,
			done = False
		)
		if assignments:
		    # if not empty grab the first assignment
		    assignment = assignments[0]
		    # if the current vac is null, add the first one on the list
		    if not assignment.current_vac:
			vacs = Vac.objects.filter(experiment__id=participant.experiment.pk)
			vac = vacs[:1].get()
			assignment.current_vac = vac
			assignment.save()
                    print "ABOUT TO REDIRECT"
		    return redirect('evaluation_edit',
			assignment.pk, assignment.current_vac.pk)
		else:
		    # if empty redirect to validation
		    # experiment.
		    return redirect('validation_index')
            else:
                print "%%%%%%%%%%%%%%% N %%%%%%%%%%%%%%%%"
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


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
