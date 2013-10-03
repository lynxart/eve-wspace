# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Interest'
        db.delete_table('Recruitment_interest')

        # Adding model 'AppQuestionChoice'
        db.create_table('Recruitment_appquestionchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choices', to=orm['Recruitment.AppQuestion'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('Recruitment', ['AppQuestionChoice'])

        # Adding model 'AppStage'
        db.create_table('Recruitment_appstage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('app_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stages', to=orm['Recruitment.AppType'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('Recruitment', ['AppStage'])

        # Adding model 'AppType'
        db.create_table('Recruitment_apptype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('use_standings', self.gf('django.db.models.fields.related.ForeignKey')(related_name='applications', null=True, to=orm['core.Corporation'])),
        ))
        db.send_create_signal('Recruitment', ['AppType'])

        # Adding field 'Action.descripiton'
        db.add_column('Recruitment_action', 'descripiton',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Action.required'
        db.add_column('Recruitment_action', 'required',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding unique constraint on 'Action', fields ['name']
        db.create_unique('Recruitment_action', ['name'])

        # Deleting field 'Application.intelclear'
        db.delete_column('Recruitment_application', 'intelclear')

        # Deleting field 'Application.killboard'
        db.delete_column('Recruitment_application', 'killboard')

        # Deleting field 'Application.standingsclear'
        db.delete_column('Recruitment_application', 'standingsclear')

        # Removing M2M table for field interests on 'Application'
        db.delete_table('Recruitment_application_interests')


        # Changing field 'Application.disposition'
        db.alter_column('Recruitment_application', 'disposition', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'AppVote.note'
        db.alter_column('Recruitment_appvote', 'note', self.gf('django.db.models.fields.TextField')(null=True))
        # Adding field 'AppQuestion.question_type'
        db.add_column('Recruitment_appquestion', 'question_type',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'AppQuestion.required'
        db.add_column('Recruitment_appquestion', 'required',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'AppQuestion.app_type'
        db.add_column('Recruitment_appquestion', 'app_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='questions', to=orm['Recruitment.AppType']),
                      keep_default=False)

        # Adding field 'AppQuestion.app_stage'
        db.add_column('Recruitment_appquestion', 'app_stage',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='questions', to=orm['Recruitment.AppStage']),
                      keep_default=False)

        # Adding field 'AppQuestion.order'
        db.add_column('Recruitment_appquestion', 'order',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'Action', fields ['name']
        db.delete_unique('Recruitment_action', ['name'])

        # Adding model 'Interest'
        db.create_table('Recruitment_interest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('Recruitment', ['Interest'])

        # Deleting model 'AppQuestionChoice'
        db.delete_table('Recruitment_appquestionchoice')

        # Deleting model 'AppStage'
        db.delete_table('Recruitment_appstage')

        # Deleting model 'AppType'
        db.delete_table('Recruitment_apptype')

        # Deleting field 'Action.descripiton'
        db.delete_column('Recruitment_action', 'descripiton')

        # Deleting field 'Action.required'
        db.delete_column('Recruitment_action', 'required')

        # Adding field 'Application.intelclear'
        db.add_column('Recruitment_application', 'intelclear',
                      self.gf('django.db.models.fields.DateTimeField')(default=False),
                      keep_default=False)

        # Adding field 'Application.killboard'
        db.add_column('Recruitment_application', 'killboard',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Application.standingsclear'
        db.add_column('Recruitment_application', 'standingsclear',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding M2M table for field interests on 'Application'
        db.create_table('Recruitment_application_interests', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('application', models.ForeignKey(orm['Recruitment.application'], null=False)),
            ('interest', models.ForeignKey(orm['Recruitment.interest'], null=False))
        ))
        db.create_unique('Recruitment_application_interests', ['application_id', 'interest_id'])


        # Changing field 'Application.disposition'
        db.alter_column('Recruitment_application', 'disposition', self.gf('django.db.models.fields.IntegerField')(default=0))

        # Changing field 'AppVote.note'
        db.alter_column('Recruitment_appvote', 'note', self.gf('django.db.models.fields.TextField')(default=''))
        # Deleting field 'AppQuestion.question_type'
        db.delete_column('Recruitment_appquestion', 'question_type')

        # Deleting field 'AppQuestion.required'
        db.delete_column('Recruitment_appquestion', 'required')

        # Deleting field 'AppQuestion.app_type'
        db.delete_column('Recruitment_appquestion', 'app_type_id')

        # Deleting field 'AppQuestion.app_stage'
        db.delete_column('Recruitment_appquestion', 'app_stage_id')

        # Deleting field 'AppQuestion.order'
        db.delete_column('Recruitment_appquestion', 'order')


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
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'Recruitment.application': {
            'Meta': {'object_name': 'Application'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'application'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"}),
            'closetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'disposition': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
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
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'use_standings': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'null': 'True', 'to': "orm['core.Corporation']"})
        },
        'Recruitment.appvote': {
            'Meta': {'object_name': 'AppVote'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['Recruitment.Application']"}),
            'disposition': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appvotes'", 'to': "orm['auth.User']"})
        },
        'Recruitment.interview': {
            'Meta': {'object_name': 'Interview'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interviews'", 'to': "orm['Recruitment.Application']"}),
            'chatlog': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interviewer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interviews'", 'to': "orm['auth.User']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
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