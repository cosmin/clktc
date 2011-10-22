# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Link'
        db.create_table('links_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('destination_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('short_url', self.gf('django.db.models.fields.TextField')(max_length=64)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('links', ['Link'])

        # Adding unique constraint on 'Link', fields ['short_url', 'site']
        db.create_unique('links_link', ['short_url', 'site_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Link', fields ['short_url', 'site']
        db.delete_unique('links_link', ['short_url', 'site_id'])

        # Deleting model 'Link'
        db.delete_table('links_link')


    models = {
        'links.link': {
            'Meta': {'unique_together': "(['short_url', 'site'],)", 'object_name': 'Link'},
            'destination_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
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
