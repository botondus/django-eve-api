from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from eve_api.api_puller.eve import character_id
from eve_api.api_puller.corporation import corporation_sheet
from eve_api.managers import ApiPlayerCorporationManager
from eve_api.models.base import ApiModel

class ApiPlayerCorporationManager(models.Manager):
    def get_via_id(self, corp_id, query_character=None, **kwargs):
        """
        Queries for a corporation. If the corp can't be founded, check the
        EVE API service for information on it. If a match still can't be
        found, return ApiPlayerCorporation.DoesNotExist.
        
        corp_id: (int) Corp's ID.
        """
        return corporation_sheet.query_corporation_sheet(corp_id, 
                                            query_character=query_character,
                                            **kwargs)
    
    def get_via_name(self, name):
        """
        Returns the matching model, given a name. Note that there is no
        way to type check this from the API, so be careful with this.
        """
        return character_id.query_get_model_from_name(ApiPlayerCorporation, name)

class ApiPlayerCorporation(ApiModel):
    """
    Represents a player-controlled corporation. Updated from a mixture of
    the alliance and corporation API pullers.
    """
    name = models.CharField(max_length=255, blank=True, null=True)
    ticker = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(verify_exists=False, blank=True, null=True)
    ceo_character = models.ForeignKey('ApiPlayerCharacter', blank=True, null=True)
    #home_station = models.ForeignKey(StaStation, blank=True, null=False)
    alliance = models.ForeignKey('ApiPlayerAlliance', blank=True, null=True)
    alliance_join_date = models.DateField(blank=True, null=True)
    tax_rate = models.FloatField(blank=True, null=True)
    member_count = models.IntegerField(blank=True, null=True)
    shares = models.IntegerField(blank=True, null=True)
    
    # Logo generation stuff
    logo_graphic_id = models.IntegerField(blank=True, null=True)
    logo_shape1 = models.IntegerField(blank=True, null=True)
    logo_shape2 = models.IntegerField(blank=True, null=True)
    logo_shape3 = models.IntegerField(blank=True, null=True)
    logo_color1 = models.IntegerField(blank=True, null=True)
    logo_color2 = models.IntegerField(blank=True, null=True)
    logo_color3 = models.IntegerField(blank=True, null=True)
    
    objects = models.Manager()
    api = ApiPlayerCorporationManager()
    
    class Meta:
        app_label = 'eve_api'
        verbose_name = 'Player Corporation'
        verbose_name_plural = 'Player Corporations'

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Corp #%d" % self.id
        