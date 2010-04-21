"""
Admin interface models. Automatically detected by admin.autodiscover().
"""
from django.contrib import admin
from eve_api.models import *

class ApiAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ['id']
    readonly_fields = ('user', 'characters')
admin.site.register(ApiAccount, ApiAccountAdmin)

class ApiPlayerCharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'corporation')
    search_fields = ['id', 'name']
admin.site.register(ApiPlayerCharacter, ApiPlayerCharacterAdmin)

class ApiPlayerCorporationInline(admin.TabularInline):
    model = ApiPlayerCorporation
    fields = ('name', 'ticker')
    extra = 0

class ApiPlayerAllianceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ticker', 'member_count', 'date_founded')
    search_fields = ['name', 'ticker']
    date_hierarchy = 'date_founded'
    inlines = [ApiPlayerCorporationInline]
admin.site.register(ApiPlayerAlliance, ApiPlayerAllianceAdmin)

class ApiPlayerCorporationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ticker', 'member_count', 'alliance')
    search_fields = ['name', 'ticker']
admin.site.register(ApiPlayerCorporation, ApiPlayerCorporationAdmin)

class ApiPlayerCorporationDivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'corporation', 'name', 'account_key')
    search_fields = ['corporation__name', 'name', 'account_key']
admin.site.register(ApiPlayerCorporationDivision, 
                    ApiPlayerCorporationDivisionAdmin)

class ApiPlayerCorporationWalletDivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'corporation', 'name', 'account_key')
    search_fields = ['corporation__name', 'name', 'account_key']
admin.site.register(ApiPlayerCorporationWalletDivision, 
                    ApiPlayerCorporationWalletDivisionAdmin)

class ApiJournalTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'ref_type', 'owner_name1', 'owner_name2', 'amount', 
                    'transaction_time')
    search_fields = ['id']
    readonly_fields = ('id', 'owner_id1', 'owner_id2', 
                       'owner_type1', 'owner_type2', 'tax_receiver')
admin.site.register(ApiJournalTransaction, ApiJournalTransactionAdmin)

class ApiJournalRefTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']
admin.site.register(ApiJournalRefType, ApiJournalRefTypeAdmin)