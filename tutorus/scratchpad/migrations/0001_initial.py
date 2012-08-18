# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Scratchpad'
        db.create_table('scratchpad_scratchpad', (
            ('id', self.gf('django.db.models.fields.AutoField')(
                primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(
                default='', null=True, blank=True)),
        ))
        db.send_create_signal('scratchpad', ['Scratchpad'])

    def backwards(self, orm):
        # Deleting model 'Scratchpad'
        db.delete_table('scratchpad_scratchpad')

    models = {
        'scratchpad.scratchpad': {
            'Meta': {'object_name': 'Scratchpad'},
            'content': ('django.db.models.fields.TextField', [],
                            {'default': "''", 'null': 'True',
                             'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [],
                       {'primary_key': 'True'})
        }
    }

    complete_apps = ['scratchpad']
