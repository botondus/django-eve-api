# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ApiAccount'
        db.create_table('eve_api_apiaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('api_key', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('api_user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('api_status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('eve_api', ['ApiAccount'])

        # Adding M2M table for field characters on 'ApiAccount'
        db.create_table('eve_api_apiaccount_characters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('apiaccount', models.ForeignKey(orm['eve_api.apiaccount'], null=False)),
            ('apiplayercharacter', models.ForeignKey(orm['eve_api.apiplayercharacter'], null=False))
        ))
        db.create_unique('eve_api_apiaccount_characters', ['apiaccount_id', 'apiplayercharacter_id'])

        # Adding model 'ApiPlayerCharacter'
        db.create_table('eve_api_apiplayercharacter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('corporation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_api.ApiPlayerCorporation'], null=True, blank=True)),
            ('race', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('balance', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('attrib_intelligence', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('attrib_memory', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('attrib_charisma', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('attrib_perception', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('attrib_willpower', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('eve_api', ['ApiPlayerCharacter'])

        # Adding model 'ApiJournalTransaction'
        db.create_table('eve_api_apijournaltransaction', (
            ('api_last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('transaction_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ref_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_api.ApiJournalRefType'], null=True, blank=True)),
            ('owner_name1', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('owner_id1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('owner_type1', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='journal_transact_owner1_set', null=True, to=orm['contenttypes.ContentType'])),
            ('owner_name2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('owner_id2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('owner_type2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='journal_transact_owner2_set', null=True, to=orm['contenttypes.ContentType'])),
            ('arg_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('arg_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('balance', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('reason', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tax_receiver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_api.ApiPlayerCorporation'], null=True, blank=True)),
            ('tax_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('eve_api', ['ApiJournalTransaction'])

        # Adding model 'ApiPlayerCorporation'
        db.create_table('eve_api_apiplayercorporation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('ticker', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('ceo_character', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_api.ApiPlayerCharacter'], null=True, blank=True)),
            ('hq_station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_db.StaStation'], blank=True)),
            ('alliance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_api.ApiPlayerAlliance'], null=True, blank=True)),
            ('alliance_join_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('tax_rate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('member_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('member_limit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('shares', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('logo_graphic_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('logo_shape1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('logo_shape2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('logo_shape3', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('logo_color1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('logo_color2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('logo_color3', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('eve_api', ['ApiPlayerCorporation'])

        # Adding model 'ApiPlayerCorporationDivision'
        db.create_table('eve_api_apiplayercorporationdivision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('account_key', self.gf('django.db.models.fields.IntegerField')()),
            ('corporation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_api.ApiPlayerCorporation'])),
        ))
        db.send_create_signal('eve_api', ['ApiPlayerCorporationDivision'])

        # Adding unique constraint on 'ApiPlayerCorporationDivision', fields ['corporation', 'account_key']
        db.create_unique('eve_api_apiplayercorporationdivision', ['corporation_id', 'account_key'])

        # Adding model 'ApiPlayerCorporationWalletDivision'
        db.create_table('eve_api_apiplayercorporationwalletdivision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('account_key', self.gf('django.db.models.fields.IntegerField')()),
            ('corporation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_api.ApiPlayerCorporation'])),
        ))
        db.send_create_signal('eve_api', ['ApiPlayerCorporationWalletDivision'])

        # Adding unique constraint on 'ApiPlayerCorporationWalletDivision', fields ['corporation', 'account_key']
        db.create_unique('eve_api_apiplayercorporationwalletdivision', ['corporation_id', 'account_key'])

        # Adding model 'ApiPlayerAlliance'
        db.create_table('eve_api_apiplayeralliance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('ticker', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('member_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date_founded', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('eve_api', ['ApiPlayerAlliance'])

        # Adding model 'ApiJournalRefType'
        db.create_table('eve_api_apijournalreftype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('eve_api', ['ApiJournalRefType'])

        # Adding model 'ApiServer'
        db.create_table('eve_api_apiserver', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('server_open', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('online_players', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('eve_api', ['ApiServer'])


    def backwards(self, orm):
        
        # Deleting model 'ApiAccount'
        db.delete_table('eve_api_apiaccount')

        # Removing M2M table for field characters on 'ApiAccount'
        db.delete_table('eve_api_apiaccount_characters')

        # Deleting model 'ApiPlayerCharacter'
        db.delete_table('eve_api_apiplayercharacter')

        # Deleting model 'ApiJournalTransaction'
        db.delete_table('eve_api_apijournaltransaction')

        # Deleting model 'ApiPlayerCorporation'
        db.delete_table('eve_api_apiplayercorporation')

        # Deleting model 'ApiPlayerCorporationDivision'
        db.delete_table('eve_api_apiplayercorporationdivision')

        # Removing unique constraint on 'ApiPlayerCorporationDivision', fields ['corporation', 'account_key']
        db.delete_unique('eve_api_apiplayercorporationdivision', ['corporation_id', 'account_key'])

        # Deleting model 'ApiPlayerCorporationWalletDivision'
        db.delete_table('eve_api_apiplayercorporationwalletdivision')

        # Removing unique constraint on 'ApiPlayerCorporationWalletDivision', fields ['corporation', 'account_key']
        db.delete_unique('eve_api_apiplayercorporationwalletdivision', ['corporation_id', 'account_key'])

        # Deleting model 'ApiPlayerAlliance'
        db.delete_table('eve_api_apiplayeralliance')

        # Deleting model 'ApiJournalRefType'
        db.delete_table('eve_api_apijournalreftype')

        # Deleting model 'ApiServer'
        db.delete_table('eve_api_apiserver')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'eve_api.apiaccount': {
            'Meta': {'object_name': 'ApiAccount'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'api_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'api_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'api_user_id': ('django.db.models.fields.IntegerField', [], {}),
            'characters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['eve_api.ApiPlayerCharacter']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'eve_api.apijournalreftype': {
            'Meta': {'object_name': 'ApiJournalRefType'},
            'api_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'eve_api.apijournaltransaction': {
            'Meta': {'object_name': 'ApiJournalTransaction'},
            'amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'api_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'arg_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'arg_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'balance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'owner_id1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'owner_id2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'owner_name1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'owner_name2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'owner_type1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'journal_transact_owner1_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'owner_type2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'journal_transact_owner2_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'reason': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ref_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_api.ApiJournalRefType']", 'null': 'True', 'blank': 'True'}),
            'tax_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tax_receiver': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_api.ApiPlayerCorporation']", 'null': 'True', 'blank': 'True'}),
            'transaction_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_api.apiplayeralliance': {
            'Meta': {'object_name': 'ApiPlayerAlliance'},
            'api_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_founded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        'eve_api.apiplayercharacter': {
            'Meta': {'object_name': 'ApiPlayerCharacter'},
            'api_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'attrib_charisma': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'attrib_intelligence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'attrib_memory': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'attrib_perception': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'attrib_willpower': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'balance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_api.ApiPlayerCorporation']", 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'race': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_api.apiplayercorporation': {
            'Meta': {'object_name': 'ApiPlayerCorporation'},
            'alliance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_api.ApiPlayerAlliance']", 'null': 'True', 'blank': 'True'}),
            'alliance_join_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'api_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ceo_character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_api.ApiPlayerCharacter']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hq_station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.StaStation']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_color1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'logo_color2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'logo_color3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'logo_graphic_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'logo_shape1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'logo_shape2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'logo_shape3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'member_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tax_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'eve_api.apiplayercorporationdivision': {
            'Meta': {'unique_together': "(('corporation', 'account_key'),)", 'object_name': 'ApiPlayerCorporationDivision'},
            'account_key': ('django.db.models.fields.IntegerField', [], {}),
            'api_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_api.ApiPlayerCorporation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'eve_api.apiplayercorporationwalletdivision': {
            'Meta': {'unique_together': "(('corporation', 'account_key'),)", 'object_name': 'ApiPlayerCorporationWalletDivision'},
            'account_key': ('django.db.models.fields.IntegerField', [], {}),
            'api_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_api.ApiPlayerCorporation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'eve_api.apiserver': {
            'Meta': {'object_name': 'ApiServer'},
            'api_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'online_players': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'server_open': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'eve_db.chrfaction': {
            'Meta': {'object_name': 'ChrFaction'},
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'faction_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'size_factor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'solar_system': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'faction_set'", 'null': 'True', 'to': "orm['eve_db.MapSolarSystem']"}),
            'station_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'station_system_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'eve_db.chrrace': {
            'Meta': {'object_name': 'ChrRace'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'graphic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EVEGraphic']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'short_description': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'eve_db.crpnpccorporation': {
            'Meta': {'object_name': 'CrpNPCCorporation'},
            'border_systems': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'corridor_systems': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enemy_corp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enemy_of_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'extent': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.ChrFaction']", 'null': 'True', 'blank': 'True'}),
            'friendly_corp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'friendly_with_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'fringe_systems': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hub_systems': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'initial_share_price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'investor1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invested1_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'investor1_shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'investor2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invested2_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'investor2_shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'investor3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invested3_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'investor3_shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'investor4': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invested4_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'investor4_shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_security': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'public_share_percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'size_factor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'solar_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapSolarSystem']", 'null': 'True', 'blank': 'True'}),
            'station_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'station_system_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stations_are_scattered': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'eve_db.evegraphic': {
            'Meta': {'object_name': 'EVEGraphic'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'icon_filename': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_obsolete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'eve_db.invcategory': {
            'Meta': {'object_name': 'InvCategory'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'graphic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EVEGraphic']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'eve_db.invgroup': {
            'Meta': {'object_name': 'InvGroup'},
            'allow_anchoring': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'allow_manufacture': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'allow_recycle': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvCategory']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'graphic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EVEGraphic']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_anchored': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_fittable_non_singleton': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'use_base_price': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'eve_db.invmarketgroup': {
            'Meta': {'object_name': 'InvMarketGroup'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'graphic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EVEGraphic']", 'null': 'True', 'blank': 'True'}),
            'has_items': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvMarketGroup']", 'null': 'True', 'blank': 'True'})
        },
        'eve_db.invtype': {
            'Meta': {'object_name': 'InvType'},
            'base_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'chance_of_duplicating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'graphic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EVEGraphic']", 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'market_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvMarketGroup']", 'null': 'True', 'blank': 'True'}),
            'mass': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'portion_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.ChrRace']", 'null': 'True', 'blank': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.mapconstellation': {
            'Meta': {'object_name': 'MapConstellation'},
            'alliance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_api.ApiPlayerAlliance']", 'null': 'True', 'blank': 'True'}),
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.ChrFaction']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapRegion']", 'null': 'True', 'blank': 'True'}),
            'sovereignty_grace_start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sovereignty_start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.mapregion': {
            'Meta': {'object_name': 'MapRegion'},
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.ChrFaction']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.mapsolarsystem': {
            'Meta': {'object_name': 'MapSolarSystem'},
            'alliance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_api.ApiPlayerAlliance']", 'null': 'True', 'blank': 'True'}),
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapConstellation']", 'null': 'True', 'blank': 'True'}),
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'solarsystem_set'", 'null': 'True', 'to': "orm['eve_db.ChrFaction']"}),
            'has_interconstellational_link': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_interregional_link': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_border_system': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_corridor_system': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_fringe_system': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_hub_system': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_international': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'luminosity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapRegion']", 'null': 'True', 'blank': 'True'}),
            'security_class': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'security_level': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sovereignty_level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sovereignty_start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvType']", 'null': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.staoperation': {
            'Meta': {'object_name': 'StaOperation'},
            'activity_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'amarr_station_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'amarr_station_operation_set'", 'null': 'True', 'to': "orm['eve_db.StaStationType']"}),
            'border': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'caldari_station_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'caldari_station_operation_set'", 'null': 'True', 'to': "orm['eve_db.StaStationType']"}),
            'corridor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fringe': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gallente_station_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gallente_station_operation_set'", 'null': 'True', 'to': "orm['eve_db.StaStationType']"}),
            'hub': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'jove_station_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'jove_station_operation_set'", 'null': 'True', 'to': "orm['eve_db.StaStationType']"}),
            'minmatar_station_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'minmatar_station_operation_set'", 'null': 'True', 'to': "orm['eve_db.StaStationType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ratio': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.stastation': {
            'Meta': {'object_name': 'StaStation'},
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapConstellation']", 'null': 'True', 'blank': 'True'}),
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.CrpNPCCorporation']", 'null': 'True', 'blank': 'True'}),
            'docking_cost_per_volume': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'max_ship_volume_dockable': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'office_rental_cost': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.StaOperation']", 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapRegion']", 'null': 'True', 'blank': 'True'}),
            'reprocessing_efficiency': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reprocessing_hangar_flag': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reprocessing_stations_take': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'security': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'solar_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapSolarSystem']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.StaStationType']", 'null': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.stastationtype': {
            'Meta': {'object_name': 'StaStationType'},
            'dock_entry_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dock_entry_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dock_entry_z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dock_orientation_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dock_orientation_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dock_orientation_z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'docking_bay_graphic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'docking_bay_graphic'", 'null': 'True', 'to': "orm['eve_db.EVEGraphic']"}),
            'hangar_graphic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'hangar_graphic'", 'null': 'True', 'to': "orm['eve_db.EVEGraphic']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_conquerable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'office_slots': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.StaOperation']", 'null': 'True', 'blank': 'True'}),
            'reprocessing_efficiency': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['eve_api']
