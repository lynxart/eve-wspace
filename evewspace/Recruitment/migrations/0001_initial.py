# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Action'
        db.create_table(u'Recruitment_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('descripiton', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Recruitment', ['Action'])

        # Adding model 'AppComment'
        db.create_table(u'Recruitment_appcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ro_comments', to=orm['Recruitment.Application'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ro_comments', to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'Recruitment', ['AppComment'])

        # Adding model 'Application'
        db.create_table(u'Recruitment_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='applications', to=orm['auth.User'])),
            ('app_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='applications', to=orm['Recruitment.AppType'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('closetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 7, 0, 0))),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('closed_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='applications_closed', null=True, to=orm['auth.User'])),
            ('disposition', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('status_text', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'Recruitment', ['Application'])

        # Adding model 'AppVote'
        db.create_table(u'Recruitment_appvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['Recruitment.Application'])),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(related_name='appvotes', to=orm['auth.User'])),
            ('disposition', self.gf('django.db.models.fields.IntegerField')()),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'Recruitment', ['AppVote'])

        # Adding model 'AppAction'
        db.create_table(u'Recruitment_appaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['Recruitment.Application'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['Recruitment.Action'])),
            ('note', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'Recruitment', ['AppAction'])

        # Adding model 'Interview'
        db.create_table(u'Recruitment_interview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interviews', to=orm['Recruitment.Application'])),
            ('interviewer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interviews', to=orm['auth.User'])),
            ('chatlog', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'Recruitment', ['Interview'])

        # Adding model 'AppQuestion'
        db.create_table(u'Recruitment_appquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('question_type', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('app_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['Recruitment.AppType'])),
            ('app_stage', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['Recruitment.AppStage'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Recruitment', ['AppQuestion'])

        # Adding model 'AppResponse'
        db.create_table(u'Recruitment_appresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='responses', to=orm['Recruitment.Application'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='responses', to=orm['Recruitment.AppQuestion'])),
            ('response', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'Recruitment', ['AppResponse'])

        # Adding model 'AppQuestionChoice'
        db.create_table(u'Recruitment_appquestionchoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choices', to=orm['Recruitment.AppQuestion'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'Recruitment', ['AppQuestionChoice'])

        # Adding model 'AppType'
        db.create_table(u'Recruitment_apptype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('instructions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_standings', self.gf('django.db.models.fields.related.ForeignKey')(related_name='applications', null=True, to=orm['core.Corporation'])),
            ('accept_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='applications', null=True, to=orm['auth.Group'])),
            ('require_account', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('disable_user_on_failure', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('purge_api_on_failure', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accept_mail', self.gf('django.db.models.fields.TextField')(null=True)),
            ('accept_subject', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('reject_mail', self.gf('django.db.models.fields.TextField')(null=True)),
            ('reject_subject', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('defer_mail', self.gf('django.db.models.fields.TextField')(null=True)),
            ('defer_subject', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal(u'Recruitment', ['AppType'])

        # Adding model 'AppStage'
        db.create_table(u'Recruitment_appstage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('app_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stages', to=orm['Recruitment.AppType'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Recruitment', ['AppStage'])

        # Adding model 'StandigsRequirement'
        db.create_table(u'Recruitment_standigsrequirement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entity', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('standing', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('entitytype', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Recruitment', ['StandigsRequirement'])


    def backwards(self, orm):
        # Deleting model 'Action'
        db.delete_table(u'Recruitment_action')

        # Deleting model 'AppComment'
        db.delete_table(u'Recruitment_appcomment')

        # Deleting model 'Application'
        db.delete_table(u'Recruitment_application')

        # Deleting model 'AppVote'
        db.delete_table(u'Recruitment_appvote')

        # Deleting model 'AppAction'
        db.delete_table(u'Recruitment_appaction')

        # Deleting model 'Interview'
        db.delete_table(u'Recruitment_interview')

        # Deleting model 'AppQuestion'
        db.delete_table(u'Recruitment_appquestion')

        # Deleting model 'AppResponse'
        db.delete_table(u'Recruitment_appresponse')

        # Deleting model 'AppQuestionChoice'
        db.delete_table(u'Recruitment_appquestionchoice')

        # Deleting model 'AppType'
        db.delete_table(u'Recruitment_apptype')

        # Deleting model 'AppStage'
        db.delete_table(u'Recruitment_appstage')

        # Deleting model 'StandigsRequirement'
        db.delete_table(u'Recruitment_standigsrequirement')


    models = {
        u'Recruitment.action': {
            'Meta': {'object_name': 'Action'},
            'descripiton': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'Recruitment.appaction': {
            'Meta': {'object_name': 'AppAction'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': u"orm['Recruitment.Action']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['Recruitment.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'Recruitment.appcomment': {
            'Meta': {'object_name': 'AppComment'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ro_comments'", 'to': u"orm['Recruitment.Application']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ro_comments'", 'to': u"orm['auth.User']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'Recruitment.application': {
            'Meta': {'object_name': 'Application'},
            'app_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'to': u"orm['Recruitment.AppType']"}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'to': u"orm['auth.User']"}),
            'closed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications_closed'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'closetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)'}),
            'disposition': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'Recruitment.appquestion': {
            'Meta': {'ordering': "['order']", 'object_name': 'AppQuestion'},
            'app_stage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['Recruitment.AppStage']"}),
            'app_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['Recruitment.AppType']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question_type': ('django.db.models.fields.IntegerField', [], {}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'Recruitment.appquestionchoice': {
            'Meta': {'object_name': 'AppQuestionChoice'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': u"orm['Recruitment.AppQuestion']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'Recruitment.appresponse': {
            'Meta': {'object_name': 'AppResponse'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': u"orm['Recruitment.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': u"orm['Recruitment.AppQuestion']"}),
            'response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'Recruitment.appstage': {
            'Meta': {'ordering': "['order']", 'object_name': 'AppStage'},
            'app_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stages'", 'to': u"orm['Recruitment.AppType']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        u'Recruitment.apptype': {
            'Meta': {'object_name': 'AppType'},
            'accept_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'null': 'True', 'to': u"orm['auth.Group']"}),
            'accept_mail': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'accept_subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'defer_mail': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'defer_subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disable_user_on_failure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'purge_api_on_failure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reject_mail': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'reject_subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'require_account': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_standings': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'null': 'True', 'to': u"orm['core.Corporation']"})
        },
        u'Recruitment.appvote': {
            'Meta': {'object_name': 'AppVote'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['Recruitment.Application']"}),
            'disposition': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appvotes'", 'to': u"orm['auth.User']"})
        },
        u'Recruitment.interview': {
            'Meta': {'object_name': 'Interview'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interviews'", 'to': u"orm['Recruitment.Application']"}),
            'chatlog': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interviewer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interviews'", 'to': u"orm['auth.User']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'Recruitment.standigsrequirement': {
            'Meta': {'object_name': 'StandigsRequirement'},
            'entity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'entitytype': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standing': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.alliance': {
            'Meta': {'object_name': 'Alliance'},
            'executor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['core.Corporation']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.corporation': {
            'Meta': {'object_name': 'Corporation'},
            'alliance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_corps'", 'null': 'True', 'to': u"orm['core.Alliance']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Recruitment']