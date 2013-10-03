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
from django.contrib.auth.models import User

from core.models import Corporation, Alliance
# Create your models here.

class Action(models.Model):
    """Represents an action that can be taken on an application e.g Intel Ran"""
    name = models.CharField(max_length=100, unique=True)
    descripiton = models.TextField(blank=True)
    required = models.BooleanField(default=False)


class Application(models.Model):
    """Represents a recruitment application."""
    applicant = models.OneToOneField(User, related_name="application", primary_key=True)
    timestamp = models.DateTimeField()
    #closetime = None indicates that the application is still open
    closetime = models.DateTimeField(null=True)
    disposition = models.IntegerField(null=True, choices=((0,'Duplicate'), (1,'Accepted'),
        (2,'Rejected'), (3, 'Deferred')))

    class Meta:
        permissions = (('can_recruit', 'Can view applications'),
                ('recruitment_admin', "Can administer the RO tool."))

    def __unicode__(self):
        return 'Applicant: %s Status: %s' % (self.applicant.name, self.disposition)


class AppVote(models.Model):
    """Represents a vote on an application"""
    application = models.ForeignKey(Application, related_name='votes')
    vote = models.ForeignKey(User, related_name='appvotes')
    disposition = models.IntegerField(choices=((1,'Accept',), (2,'Reject'), (3, 'Defer')))
    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()


class AppAction(models.Model):
    """Represents an action taken on an application."""
    application = models.ForeignKey(Application, related_name='actions')
    action = models.ForeignKey(Action, related_name='instances')
    note = models.TextField()
    timestamp = models.DateTimeField()


class Interview(models.Model):
    """Represents an interview for an application."""
    application = models.ForeignKey(Application, related_name='interviews')
    interviewer = models.ForeignKey(User, related_name='interviews')
    chatlog = models.TextField()
    timestamp = models.DateTimeField()


class AppQuestion(models.Model):
    """Represents a question to be asked on the application."""
    question = models.CharField(max_length=255)
    question_type = models.IntegerField(choices=((1,'Text Field'),
        (2, 'Text Box'), (3, 'Dropdown'), (3, 'Select'), (4, 'Multi-Select')))
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
    description = models.TextField(null=True, blank=True)
    use_standings = models.ForeignKey(Corporation,
            related_name="applications", null=True)


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
