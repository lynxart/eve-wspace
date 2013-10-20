#    Eve W-Space
#    Copyright (C) 2013  Andrew Austin and other contributors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version. An additional term under section
#    7 of the GPL is included in the LICENSE file.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from datetime import datetime
import pytz

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.template.response import TemplateResponse
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import get_object_or_404
from django import forms
from core.utils import get_config
from core.models import Corporation
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required, login_required
from models import AppType, Application, RecruitRegistrationForm

def applicant_register(request, app_type=None):
    email_required = get_config('RECRUIT_REQUIRE_EMAIL', None).value == "1"
    if not app_type:
        app_type = get_object_or_404(AppType, pk=request.POST.get('app_type'))
    if request.method == "POST":
        form = RecruitRegistrationForm(request.POST)
        valid = form.is_valid()
        email = request.POST.get('email', None)
        if email_required and not email:
            form.errors['__all__'] = form.error_class(
                    ['An email address is required.'])
            valid = False
        if valid:
            newUser = form.save()
            newUser.is_active = False
            if email:
                newUser.email = email
            newUser.save()
            log_user = authenticate(username=newUser.username,
                    password=request.POST.get('password1', ''))
            login(request, log_user)
            return HttpResponseRedirect(request.POST.get('next_page'))
    else:
        form = RecruitRegistrationForm()
    # TODO: Replace with url reversal
    next_page = "/recruitment/apply/%s/" % app_type.pk
    return TemplateResponse(request, "recruit_register.html", {'form': form,
                            'email_required': email_required,
                            'next_page': next_page,
                            'app_type': app_type.pk})



def get_application(request, app_type_id):
    app_type = get_object_or_404(AppType, pk=app_type_id)
    if app_type.require_account and not request.user.is_authenticated():
        raise PermissionDenied
    if not app_type.require_account and not request.user.is_authenticated():
        return applicant_register(request, app_type)

    return TemplateResponse(request, 'application.html', {'app': app_type})

@permission_required('Recruitment.can_recruit')
def view_applications(request):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def edit_applications(request):
    return TemplateResponse(request, 'edit_applications.html',
            {'apps': AppType.objects.filter(deleted=False).all()})

@permission_required('Recruitment.recruitment_admin')
def edit_workflows(request):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def recruitment_settings(request):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def app_global_settings(request, app_type_id):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def add_app_stage(request, app_type_id):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def delete_app_type(request, app_type_id):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def delete_app_stage(request, app_type_id, stage_id):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def edit_app_stage(request, app_type_id, stage_id):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def new_question(request, app_type_id, stage_id):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def edit_question(request, app_type_id, stage_id, question_id):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def delete_question(request, app_type_id, stage_id, question_id):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def edit_app_type(request, app_type_id):
    if not request.is_ajax():
        raise PermmissionDenied
    app_type = get_object_or_404(AppType, pk=app_type_id)
    if request.method == "POST":
        name = request.POST.get('name', None)
        instructions = request.POST.get('instructions', '')
        disable_user = request.POST.get('disable_user', 'False') == 'on'
        purge_api = request.POST.get('purge_api', 'False') == 'on'
        require_user = request.POST.get('require_user', 'False') == 'on'
        standings_text = request.POST.get('standings', None)
        if standings_text:
            standings_corp = get_object_or_404(Corporation,
                    name=standings_text)
        else:
            standings_corp = None
        accept_text = request.POST.get('accept_group', None)
        if accept_text:
            accept_group = get_object_or_404(Group, name=accept_text)
        else:
            accept_group = None
        accept_subject = request.POST.get('accept_sbj', None)
        accept_body = request.POST.get('accept_mail', None)
        defer_subject = request.POST.get('defer_sbj', None)
        defer_body = request.POST.get('defer_mail', None)
        reject_subject = request.POST.get('reject_sbj', None)
        reject_body = request.POST.get('reject_mail', None)

        if name:
            app_type.name = name
        else:
            return HttpResponse('Name cannot be blank.', status=400)

        app_type.instructions = instructions
        app_type.use_standings = standings_corp
        app_type.accept_group = accept_group
        app_type.require_account = require_user
        app_type.disable_user_on_failure = disable_user
        app_type.purge_api_on_failure = purge_api
        app_type.accept_subject = accept_subject
        app_type.accept_mail = accept_body
        app_type.defer_subject = defer_subject
        app_type.defer_mail = defer_body
        app_type.reject_subject = reject_subject
        app_type.reject_mail = reject_body

        app_type.save()
        saved = True
    else:
        saved = False
    return TemplateResponse(request, 'application_edit.html',
            {'application': app_type, 'saved': saved})
