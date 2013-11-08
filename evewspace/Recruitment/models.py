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
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django import forms
from core.models import Corporation, Alliance

from datetime import datetime
import pytz
# Create your models here.

class Action(models.Model):
    """Represents an action that can be taken on an application e.g Intel Ran"""
    name = models.CharField(max_length=100, unique=True)
    descripiton = models.TextField(blank=True)
    required = models.BooleanField(default=False)


class AppComment(models.Model):
    application = models.ForeignKey('Application', related_name="ro_comments")
    author = models.ForeignKey(User, related_name="ro_comments")
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Application(models.Model):
    """Represents a recruitment application."""
    applicant = models.ForeignKey(User, related_name="applications")
    app_type = models.ForeignKey('AppType', related_name="applications")
    timestamp = models.DateTimeField(auto_now=True)
    #closetime = None indicates that the application is still open
    closetime = models.DateTimeField(null=True)
    created = models.DateTimeField(default=datetime.now(pytz.utc))
    submitted = models.DateTimeField(null=True)
    closed_by = models.ForeignKey(User, related_name="applications_closed",
            null=True)
    disposition = models.IntegerField(null=True, choices=((0,'Duplicate'),
        (1,'Accepted'), (2,'Rejected'), (3, 'Deferred')))
    status_text = models.TextField(null=True)

    class Meta:
        permissions = (('can_recruit', 'Can view applications'),
                ('recruitment_admin', "Can administer the RO tool."),
                )

    def add_action(self, user, action, note):
        result = AppAction(application=self, user=user, action=action,
                note=note)
        result.save()
        return result

    def add_vote(self, user, disposition, note):
        result = AppVote(application=self, user=user, disposition=disposition,
                note=note)
        result.save()
        return result

    def add_interview(self, user, chatlog):
        result = Interview(application=self, interviewer=user,
                chatlog=chatlog)
        result.save()
        return result

    def add_comment(self, user, comment):
        result = AppComment(application=self, author=user, comment=comment)
        result.save()
        return result

    def send_applicant_mail(self, subject, body):
        # TODO: this
        return True

    def reject_application(self, user, note):
        self.disposition = 2
        self.closetime = datetime.now(pytz.utc)
        self.status_text = note
        self.closed_by = user
        if self.app_type.disable_user_on_failure:
            self.applicant.is_active = False
            self.applicant.set_unusable_password()
            self.applicant.groups = []
            self.applicant.save()
        if self.app_type.purge_api_on_failure:
            self.applicant.api_keys.all().delete()
        self.save()
        if self.app_type.reject_mail:
            self.send_applicant_mail(subject=self.app_type.reject_subject,
                    body=self.app_type.reject_mail)
        return self

    def close_as_duplicate(self, user, note):
        self.disposition = 0
        self.closetime = datetime.now(pytz.utc)
        self.status_text = note
        self.closed_by = user
        self.save()
        return self

    def defer_application(self, user, note):
        self.disposition = 3
        self.closetime = datetime.now(pytz.utc)
        self.status_text = note
        self.closed_by = user
        self.save()
        if self.app_type.defer_mail:
            self.send_applicant_mail(subject=self.app_type.defer_subject,
                    body=self.app_type.defer_mail)
        return self

    def accept_application(self, user, note):
        self.disposition = 1
        self.closetime = datetime.now(pytz.utc)
        self.status_text = note
        self.closed_by = user
        if self.app_type.accept_group:
            self.applicant.groups.add(self.app_type.accept_group)
        if not self.applicant.is_active:
            self.applicant.is_active = True
            self.applicant.save()
        self.save()
        if self.app_type.accept_mail:
            self.send_applicant_mail(subject=self.app_type.accept_subject,
                    body=self.app_type.accept_mail)
        return self

    def __unicode__(self):
        return 'Applicant: %s Status: %s' % (self.applicant.username,
                self.disposition)


class AppVote(models.Model):
    """Represents a vote on an application"""
    application = models.ForeignKey(Application, related_name='votes')
    vote = models.ForeignKey(User, related_name='appvotes')
    disposition = models.IntegerField(choices=((1,'Accept',), (2,'Reject'),
        (3, 'Defer')))
    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class AppAction(models.Model):
    """Represents an action taken on an application."""
    application = models.ForeignKey(Application, related_name='actions')
    action = models.ForeignKey(Action, related_name='instances')
    note = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Interview(models.Model):
    """Represents an interview for an application."""
    application = models.ForeignKey(Application, related_name='interviews')
    interviewer = models.ForeignKey(User, related_name='interviews')
    chatlog = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class AppQuestion(models.Model):
    """Represents a question to be asked on the application."""
    question = models.CharField(max_length=255)
    question_type = models.IntegerField(choices=((1,'Text Field'),
        (2, 'Text Box'), (3, 'Radio'), (3, 'Checkbox')))
    description = models.TextField(null=True, blank=True)
    required = models.BooleanField(default=True)
    app_type = models.ForeignKey('AppType', related_name='questions')
    app_stage = models.ForeignKey('AppStage', related_name='questions')
    order = models.IntegerField()

    class Meta:
        ordering = ['order',]


class AppResponse(models.Model):
    """Represents a response to a custom application question."""
    application = models.ForeignKey(Application, related_name='responses')
    question = models.ForeignKey(AppQuestion, related_name='responses')
    response = models.TextField(blank=True, null=True)


class AppQuestionChoice(models.Model):
    question = models.ForeignKey(AppQuestion, related_name='choices')
    value = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)


class AppType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    instructions = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    use_standings = models.ForeignKey(Corporation,
            related_name="applications", null=True)
    # Determines what group a user accepted via this application type will
    # have. If it is null, the user's groups will not be changed
    accept_group = models.ForeignKey(Group, related_name="applications",
            null=True)
    require_account = models.BooleanField(default=False)
    disable_user_on_failure = models.BooleanField(default=False)
    purge_api_on_failure = models.BooleanField(default=False)
    accept_mail = models.TextField(null=True)
    accept_subject = models.CharField(max_length=255, null=True)
    reject_mail = models.TextField(null=True)
    reject_subject = models.CharField(max_length=255, null=True)
    defer_mail = models.TextField(null=True)
    defer_subject = models.CharField(max_length=255, null=True)

    def start_application(self, user):
        """
        Returns a blank application for the user with this type.
        """
        app = Application(app_type=self, applicant=user)
        app.save()
        return app


class AppStage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    app_type = models.ForeignKey(AppType, related_name='stages')
    order = models.IntegerField()

    class Meta:
        ordering = ['order',]


class StandigsRequirement(models.Model):
    """Represents a standing to be checked against applications."""
    entity = models.CharField(max_length=100)
    # If standing is null and we have a requirement record, we can interpret
    # this as requiring no standing
    standing = models.FloatField(blank=True, null=True)
    entitytype = models.IntegerField(choices=((0,'Corporation'),
        (1,'Faction')))

class RecruitRegistrationForm(UserCreationForm):
    """Extends the django registration form to add fields."""
    username = forms.CharField(max_length=30, label="Username")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password:")
