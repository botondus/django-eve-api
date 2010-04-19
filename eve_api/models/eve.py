from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from eve_api.api_puller.eve import character_id
from eve_api.api_puller.eve import alliance_list
from eve_api.api_puller.corporation import corps_from_alliances
from eve_api.api_puller.eve import ref_types
from eve_api.models.base import ApiModel

class ApiPlayerAllianceManager(models.Manager):
    def get_via_name(self, name, **kwargs):
        """
        Returns the matching model, given a name. Note that there is no
        way to type check this from the API, so be careful with this.
        """
        return character_id.query_get_object_from_name(ApiPlayerAlliance, name,
                                                      **kwargs)
    
    def update_all_alliances(self, **kwargs):
        """
        Does an AllianceList API query, updating all of the local alliance
        data from the results. Also creates stub ApiPlayerCorporation objects
        from the members list.
        
        WARNING: This is a very long running query that should only be done
                 in a background task.
        """
        alliance_list.query_alliance_list(**kwargs)
        
    def update_all_corporations(self, **kwargs):
        corps_from_alliances.update_alliance_corporations(**kwargs)
        

class ApiPlayerAlliance(ApiModel):
    """
    Represents a player-controlled alliance. Updated from the alliance
    EVE XML API puller at intervals.
    """
    name = models.CharField(max_length=255, blank=True)
    ticker = models.CharField(max_length=15, blank=True)
    #executor_character = models.ForeignKey(EVECharacter, blank=True, null=False)
    member_count = models.IntegerField(blank=True, null=True)
    date_founded = models.DateField(blank=True, null=True)
    
    objects = models.Manager()
    api = ApiPlayerAllianceManager()
    
    class Meta:
        app_label = 'eve_api'
        ordering = ['date_founded']
        verbose_name = 'Player Alliance'
        verbose_name_plural = 'Player Alliances'
    
    def __unicode__(self):
        if self.name:
            return "%s (%d)" % (self.name, self.id)
        else:
            return "(#%d)" % self.id
        
    def __str__(self):
        return self.__unicode__()
    
class ApiJournalRefTypeManager(models.Manager):    
    def update_all_types(self, **kwargs):
        """
        This API method creates/updates the ApiJournalRefType objects. This
        should only need to be once, or at any time that CCP adds new 
        transaction reference types.
        """
        ref_types.query_type_list(**kwargs)
    
class ApiJournalRefType(ApiModel):
    """
    Transaction types used for Corporate and Character journal entries.
    """
    name = models.CharField(max_length=255, blank=True)
    
    objects = models.Manager()
    api = ApiJournalRefTypeManager()
    
    class Meta:
        app_label = 'eve_api'
        ordering = ['id']
        verbose_name = 'Transaction Ref Type'
        verbose_name_plural = 'Transaction Ref Type'
    
    def __unicode__(self):
        if self.name:
            return "%s (%d)" % (self.name, self.id)
        else:
            return "(#%d)" % self.id
        
    def __str__(self):
        return self.__unicode__()