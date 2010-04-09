from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from eve_api.api_puller.eve.character_id import query_get_model_from_name
from eve_api.models.base import ApiModel

class ApiPlayerCharacterManager(models.Manager):
    def get_from_name(self, name):
        """
        Returns the matching model, given a name. Note that there is no
        way to type check this from the API, so be careful with this.
        """
        return query_get_model_from_name(ApiPlayerCharacter, name)

class ApiPlayerCharacter(ApiModel):
    """
    Represents an individual player character within the game. Not to be
    confused with an account.
    """
    name = models.CharField(max_length=255, blank=True, null=False)
    corporation = models.ForeignKey('ApiPlayerCorporation', blank=True, null=True)
    # TODO: Choices field
    race = models.IntegerField(blank=True, null=True)
    # TODO: Choices field
    gender = models.IntegerField(blank=True, null=True)
    balance = models.FloatField("Account Balance", blank=True, null=True)
    attrib_intelligence = models.IntegerField("Intelligence", blank=True, 
                                              null=True)
    attrib_memory = models.IntegerField("Memory", blank=True, null=True)
    attrib_charisma = models.IntegerField("Charisma", blank=True, null=True)
    attrib_perception = models.IntegerField("Perception", blank=True, null=True)
    attrib_willpower = models.IntegerField("Willpower", blank=True, null=True)
    
    objects = models.Manager()
    api = ApiPlayerCharacterManager()
    
    def __unicode__(self):
        if self.name:
            return "%s (%d)" % (self.name, self.id)
        else:
            return "(%d)" % self.id

    def __str__(self):
        return self.__unicode__()
    
    class Meta:
        app_label = 'eve_api'
        verbose_name = 'Player Character'
        verbose_name_plural = 'Player Characters'