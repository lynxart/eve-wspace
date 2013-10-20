# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AppComment'
        db.create_table('Recruitment_appcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ro_comments', to=orm['Recruitment.Application'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ro_comments', to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('Recruitment', ['AppComment'])


        # Changing field 'Interview.timestamp'
        db.alter_column('Recruitment_interview', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'AppAction.timestamp'
        db.alter_column('Recruitment_appaction', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))
        # Adding field 'Application.app_type'
        db.add_column('Recruitment_application', 'app_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='applications', to=orm['Recruitment.AppType']),
                      keep_default=False)

        # Adding field 'Application.created'
        db.add_column('Recruitment_application', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 10, 14, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Application.submitted'
        db.add_column('Recruitment_application', 'submitted',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Application.closed_by'
        db.add_column('Recruitment_application', 'closed_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='applications_closed', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Application.status_text'
        db.add_column('Recruitment_application', 'status_text',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)


        # Changing field 'Application.timestamp'
        db.alter_column('Recruitment_application', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Application.applicant'
        db.alter_column('Recruitment_application', 'applicant_id', self.gf('django.db.models.fields.related.ForeignKey')(primary_key=True, to=orm['auth.User']))

        # Changing field 'AppVote.timestamp'
        db.alter_column('Recruitment_appvote', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))
        # Deleting field 'AppType.description'
        db.delete_column('Recruitment_apptype', 'description')

        # Adding field 'AppType.instructions'
        db.add_column('Recruitment_apptype', 'instructions',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'AppType.deleted'
        db.add_column('Recruitment_apptype', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AppType.accept_group'
        db.add_column('Recruitment_apptype', 'accept_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='applications', null=True, to=orm['auth.Group']),
                      keep_default=False)

        # Adding field 'AppType.require_account'
        db.add_column('Recruitment_apptype', 'require_account',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AppType.disable_user_on_failure'
        db.add_column('Recruitment_apptype', 'disable_user_on_failure',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AppType.purge_api_on_failure'
        db.add_column('Recruitment_apptype', 'purge_api_on_failure',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AppType.accept_mail'
        db.add_column('Recruitment_apptype', 'accept_mail',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'AppType.accept_subject'
        db.add_column('Recruitment_apptype', 'accept_subject',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'AppType.reject_mail'
        db.add_column('Recruitment_apptype', 'reject_mail',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'AppType.reject_subject'
        db.add_column('Recruitment_apptype', 'reject_subject',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'AppType.defer_mail'
        db.add_column('Recruitment_apptype', 'defer_mail',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'AppType.defer_subject'
        db.add_column('Recruitment_apptype', 'defer_subject',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'AppComment'
        db.delete_table('Recruitment_appcomment')


        # Changing field 'Interview.timestamp'
        db.alter_column('Recruitment_interview', 'timestamp', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'AppAction.timestamp'
        db.alter_column('Recruitment_appaction', 'timestamp', self.gf('django.db.models.fields.DateTimeField')())
        # Deleting field 'Application.app_type'
        db.delete_column('Recruitment_application', 'app_type_id')

        # Deleting field 'Application.created'
        db.delete_column('Recruitment_application', 'created')

        # Deleting field 'Application.submitted'
        db.delete_column('Recruitment_application', 'submitted')

        # Deleting field 'Application.closed_by'
        db.delete_column('Recruitment_application', 'closed_by_id')

        # Deleting field 'Application.status_text'
        db.delete_column('Recruitment_application', 'status_text')


        # Changing field 'Application.timestamp'
        db.alter_column('Recruitment_application', 'timestamp', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Application.applicant'
        db.alter_column('Recruitment_application', 'applicant_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['auth.User']))

        # Changing field 'AppVote.timestamp'
        db.alter_column('Recruitment_appvote', 'timestamp', self.gf('django.db.models.fields.DateTimeField')())
        # Adding field 'AppType.description'
        db.add_column('Recruitment_apptype', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'AppType.instructions'
        db.delete_column('Recruitment_apptype', 'instructions')

        # Deleting field 'AppType.deleted'
        db.delete_column('Recruitment_apptype', 'deleted')

        # Deleting field 'AppType.accept_group'
        db.delete_column('Recruitment_apptype', 'accept_group_id')

        # Deleting field 'AppType.require_account'
        db.delete_column('Recruitment_apptype', 'require_account')

        # Deleting field 'AppType.disable_user_on_failure'
        db.delete_column('Recruitment_apptype', 'disable_user_on_failure')

        # Deleting field 'AppType.purge_api_on_failure'
        db.delete_column('Recruitment_apptype', 'purge_api_on_failure')

        # Deleting field 'AppType.accept_mail'
        db.delete_column('Recruitment_apptype', 'accept_mail')

        # Deleting field 'AppType.accept_subject'
        db.delete_column('Recruitment_apptype', 'accept_subject')

        # Deleting field 'AppType.reject_mail'
        db.delete_column('Recruitment_apptype', 'reject_mail')

        # Deleting field 'AppType.reject_subject'
        db.delete_column('Recruitment_apptype', 'reject_subject')

        # Deleting field 'AppType.defer_mail'
        db.delete_column('Recruitment_apptype', 'defer_mail')

        # Deleting field 'AppType.defer_subject'
        db.delete_column('Recruitment_apptype', 'defer_subject')


    models = {
        'Recruitment.action': {
            'Meta': {'object_name': 'Action'},
            'descripiton': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Recruitment.appaction': {
            'Meta': {'object_name': 'AppAction'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['Recruitment.Action']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': "orm['Recruitment.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'Recruitment.appcomment': {
            'Meta': {'object_name': 'AppComment'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ro_comments'", 'to': "orm['Recruitment.Application']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ro_comments'", 'to': "orm['auth.User']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'Recruitment.application': {
            'Meta': {'object_name': 'Application'},
            'app_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'to': "orm['Recruitment.AppType']"}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'primary_key': 'True', 'to': "orm['auth.User']"}),
            'closed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications_closed'", 'null': 'True', 'to': "orm['auth.User']"}),
            'closetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disposition': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'status_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'Recruitment.appquestion': {
            'Meta': {'ordering': "['order']", 'object_name': 'AppQuestion'},
            'app_stage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['Recruitment.AppStage']"}),
            'app_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['Recruitment.AppType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question_type': ('django.db.models.fields.IntegerField', [], {}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'Recruitment.appquestionchoice': {
            'Meta': {'object_name': 'AppQuestionChoice'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': "orm['Recruitment.AppQuestion']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'Recruitment.appresponse': {
            'Meta': {'object_name': 'AppResponse'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': "orm['Recruitment.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': "orm['Recruitment.AppQuestion']"}),
            'response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'Recruitment.appstage': {
            'Meta': {'ordering': "['order']", 'object_name': 'AppStage'},
            'app_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stages'", 'to': "orm['Recruitment.AppType']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        'Recruitment.apptype': {
            'Meta': {'object_name': 'AppType'},
            'accept_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'null': 'True', 'to': "orm['auth.Group']"}),
            'accept_mail': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'accept_subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'defer_mail': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'defer_subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disable_user_on_failure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'purge_api_on_failure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reject_mail': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'reject_subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'require_account': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_standings': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'null': 'True', 'to': "orm['core.Corporation']"})
        },
        'Recruitment.appvote': {
            'Meta': {'object_name': 'AppVote'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['Recruitment.Application']"}),
            'disposition': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appvotes'", 'to': "orm['auth.User']"})
        },
        'Recruitment.interview': {
            'Meta': {'object_name': 'Interview'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interviews'", 'to': "orm['Recruitment.Application']"}),
            'chatlog': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interviewer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interviews'", 'to': "orm['auth.User']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'Recruitment.standigsrequirement': {
            'Meta': {'object_name': 'StandigsRequirement'},
            'entity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'entitytype': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standing': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.alliance': {
            'Meta': {'object_name': 'Alliance'},
            'executor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['core.Corporation']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.corporation': {
            'Meta': {'object_name': 'Corporation'},
            'alliance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_corps'", 'null': 'True', 'to': "orm['core.Alliance']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Recruitment']