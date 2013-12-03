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
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required, login_required
from models import *
from API.models import MemberAPIKey

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
    next_page = reverse('Recruitment.views.get_application',
            args=(app_type.pk,))
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
    app = app_type.start_application(request.user)
    return HttpResponseRedirect(
            reverse('Recruitment.views.get_application_form', args=(app.pk,)))

@login_required
def get_application_form(request, app_id):
    app = get_object_or_404(Application, pk=app_id)
    app_type = app.app_type
    if app.applicant != request.user:
        raise PermissionDenied
    status_view = False
    if app.submitted:
        status_view = True
    return TemplateResponse(request, 'application.html', {'app': app_type,
        'application': app, 'status_view': status_view})

@login_required
def get_api_keys(request, app_id):
    app = get_object_or_404(Application, pk=app_id)
    if app.applicant != request.user or not request.is_ajax():
        raise PermissionDenied
    if request.method == "POST":
        error_list = []
        key_id = request.POST.get('key_id', 0)
        key_vcode = request.POST.get('vcode', '')
        if not key_id or not key_vcode:
            error_list.append('You must provide both Key ID and vCode!')
        else:
            try:
                key_id = int(key_id)
            except ValueError:
               error_list.append('The Key ID is invalid (not an integer)!')
            api_key = MemberAPIKey(keyid=key_id, vcode=key_vcode,
                    user=request.user)
            api_key.validate()
            if not api_key.validation_error:
                return HttpResponse()
            else:
                error_list.append(api_key.validation_error)
                api_key.delete()
        if error_list:
            error_text = ''
            for x in error_list:
                error_text += '%s<br />' % x
            return HttpResponse(error_text, status=400)
    else:

        return TemplateResponse(request, 'api_widget.html',
                {'application': app})

@login_required
def save_application(request, app_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    try:
        app.save_from_dict(request.POST.copy())
    except Exception as ex:
        raise
    return HttpResponse()

@permission_required('Recruitment.can_recruit')
def view_applications(request):
    open_apps = Application.objects.filter(submitted__isnull=False,
            disposition__isnull=True).all()
    closed_apps = Application.objects.filter(disposition__isnull=False).all()

    open_paginator = Paginator(open_apps, 4)
    open_pages = [open_paginator.page(x) for x in open_paginator.page_range]
    closed_paginator = Paginator(closed_apps, 4)
    closed_pages = [closed_paginator.page(x) for x in closed_paginator.page_range]

    return TemplateResponse(request, 'ro_panel.html',
            {'open_apps': open_pages, 'closed_apps': closed_pages})

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

def _process_stage_details_form(request, app_type, stage=None):
    if not stage:
        stage = AppStage()

    name = request.POST.get('name','')
    description = request.POST.get('description','')
    order = request.POST.get('order','')

    stage.name = name
    stage.description = description
    stage.order = int(order)
    stage.app_type = app_type

    stage.save()

    return stage

@permission_required('Recruitment.recruitment_admin')
def add_app_stage(request, app_type_id):
    if not request.is_ajax():
        raise PermissionDenied

    app_type = get_object_or_404(AppType, pk=app_type_id)
    try:
        _process_stage_details_form(request, app_type)
        return HttpResponse()
    except Exception as ex:
        return HttpResponse(repr(ex), status=400)

@permission_required('Recruitment.recruitment_admin')
def edit_app_stage(request, app_type_id, stage_id):
    if not request.is_ajax():
        raise PermissionDenied

    app_type = get_object_or_404(AppType, pk=app_type_id)
    app_stage = get_object_or_404(AppStage, pk=stage_id)
    error = ''
    if request.method == 'POST':
        try:
            _process_stage_details_form(request, app_type, app_stage)
            saved = True
        except Exception as ex:
            saved = False
            error = ex.message
    else:
        saved = False

    return TemplateResponse(request, 'stage_edit.html', {'stage': app_stage,
        'saved': saved, 'error': error})

@permission_required('Recruitment.recruitment_admin')
def delete_app_type(request, app_type_id):
    if not request.is_ajax():
        raise PermissionDenied
    app_type = get_object_or_404(AppType, pk=app_type_id)
    app_type.delete()
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def delete_app_stage(request, app_type_id, stage_id):
    if not request.is_ajax():
        raise PermissionDenied
    app_stage = get_object_or_404(AppStage, pk=stage_id)
    app_stage.delete()
    return HttpResponse()

def _process_question_form(request, app_type, stage, question=None):
    if not question:
        question = AppQuestion()
    question_text = request.POST.get('question', None)
    question_type = request.POST.get('type', None)
    order = request.POST.get('order', '1')
    question_choices = request.POST.get('choices', None)
    required = request.POST.get('required', False) != False
    description = request.POST.get('description', None)

    question.question = question_text
    question.question_type = int(question_type)
    question.app_type = app_type
    question.app_stage = stage
    question.order = int(order)
    question.required = required
    question.description = description

    question.save()
    if question.question_type > 2:
        choices = question_choices.splitlines()
        question.choices.all().delete()
        for item in choices:
           AppQuestionChoice(question=question, value=item).save()

    return question

@permission_required('Recruitment.recruitment_admin')
def new_question(request, app_type_id, stage_id):
    if not request.is_ajax():
        raise PermissionDenied
    if request.method != "POST":
        return HttpResponse()

    app_type = get_object_or_404(AppType, pk=app_type_id)
    app_stage = get_object_or_404(AppStage, pk=stage_id)

    try:
        question = _process_question_form(request, app_type, app_stage)
        return HttpResponse()
    except AttributeError as ex:
        return HttpResponse(ex.message, status=400)


@permission_required('Recruitment.recruitment_admin')
def edit_question(request, app_type_id, stage_id, question_id):
    if not request.is_ajax():
        raise PermissionDenied
    app_type = get_object_or_404(AppType, pk=app_type_id)
    app_stage = get_object_or_404(AppStage, pk=stage_id)
    question = get_object_or_404(AppQuestion, pk=question_id)
    if request.method != "POST":
        return TemplateResponse(request, 'edit_question.html',
                {'question': question})
    try:
        question = _process_question_form(request, app_type, app_stage,
                question)
        return HttpResponse()
    except Exception as ex:
        return HttpResponse(ex.message, status=400)


@permission_required('Recruitment.recruitment_admin')
def delete_question(request, app_type_id, stage_id, question_id):
    if not request.is_ajax():
        raise PermissionDenid
    if request.method != "POST":
        return HttpResponse(status=400)
    question = get_object_or_404(AppQuestion, pk=question_id)
    question.delete()
    return HttpResponse()

def _process_app_type_form(request, app_type=None):
    if not app_type:
        app_type = AppType()
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
        if name != app_type.name and AppType.objects.filter(
                name=name).exists():
            raise AttributeError('The name must be unique!')
        app_type.name = name
    else:
        raise AttributeError('Name cannot be blank.')

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

    return app_type


@permission_required('Recruitment.recruitment_admin')
def edit_app_type(request, app_type_id):
    if not request.is_ajax():
        raise PermmissionDenied
    app_type = get_object_or_404(AppType, pk=app_type_id)
    error = None
    if request.method == "POST":
        try:
            app_type = _process_app_type_form(request, app_type)
            saved = True
        except AttributeError as ex:
           saved = False
           error = ex.message
    else:
        saved = False
    return TemplateResponse(request, 'application_edit.html',
            {'application': app_type, 'app_saved': saved, 'error': error})

@permission_required('Recruitment.recruitment_admin')
def new_app_type(request):
    if not request.is_ajax():
        raise PermissionDenied
    if request.method == "POST":
        try:
            app_type = _process_app_type_form(request)
        except AttributeError as ex:
            return HttpResponse(ex.message, status=400)
        return HttpResponse()
    else:
        return HttpResponse()
