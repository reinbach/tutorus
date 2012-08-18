# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table('questions_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(
                primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(
                max_length=25)),
            ('content', self.gf('django.db.models.fields.TextField')(
                default='', null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(
                default='asked', max_length=10)),
        ))
        db.send_create_signal('questions', ['Question'])

    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table('questions_question')

    models = {
        'questions.question': {
            'Meta': {'object_name': 'Question'},
            'content': ('django.db.models.fields.TextField', [],
                            {'default': "''", 'null': 'True',
                             'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [],
                       {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [],
                           {'default': "'asked'", 'max_length': '10'}),
            'subject': ('django.db.models.fields.CharField', [],
                            {'max_length': '25'})
        }
    }

    complete_apps = ['questions']
