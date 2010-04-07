"""
Admin interface models. Automatically detected by admin.autodiscover().
"""
from django.contrib import admin
from eve_api.models import *

class ApiAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ['id']
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
