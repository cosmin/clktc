# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Link.destination_url'
        db.alter_column('links_link', 'destination_url', self.gf('django.db.models.fields.URLField')(max_length=255))


    def backwards(self, orm):
        
        # Changing field 'Link.destination_url'
        db.alter_column('links_link', 'destination_url', self.gf('django.db.models.fields.URLField')(max_length=200))


    models = {
        'links.link': {
            'Meta': {'unique_together': "(['short_url', 'site'],)", 'object_name': 'Link'},
            'destination_url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_url': ('django.db.models.fields.TextField', [], {'max_length': '64'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['links']
