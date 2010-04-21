from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from eve_api.api_puller.eve.character_id import query_get_object_from_name
from eve_api.api_puller.character import wallet_journal
from eve_api.models import ApiModel

class ApiPlayerCharacterManager(models.Manager):
    def get_via_name(self, name, **kwargs):
        """
        Returns the matching model, given a name. Note that there is no
        way to type check this from the API, so be careful with this.
        """
        return query_get_object_from_name(ApiPlayerCharacter, name, **kwargs)[0]

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
        
    class Meta:
        app_label = 'eve_api'
        verbose_name = 'Player Character'
        verbose_name_plural = 'Player Characters'
        
    def __unicode__(self):
        if self.name:
            return "%s (%d)" % (self.name, self.id)
        else:
            return "(%d)" % self.id

    def __str__(self):
        return self.__unicode__()
    
    def get_account(self):
        """
        Returns the ApiAccount object that owns this character, or raise a
        DoesNotExist exception if none exists.
        """
        account = self.apiaccount_set.all()
        if account:
            return account[0]
        else:
            raise ApiPlayerCharacter.DoesNotExist('No account associated with ApiPlayerCharacter ID#: %d' % self.id)
        
    def update_journal_from_api(self, **kwargs):
        """
        Updates this character's wallet from the API.
        """
        wallet_journal.query_character_journal(self, **kwargs)
        
class ApiJournalTransaction(ApiModel):
    """
    An individual journal transaction between players and/or corporations.
    """
    id = models.BigIntegerField(primary_key=True)
    transaction_time = models.DateTimeField(blank=True, null=True)
    ref_type = models.ForeignKey('ApiJournalRefType', blank=True, null=True)
    
    owner_name1 = models.CharField(max_length=255, blank=True)
    owner_id1 = models.IntegerField(blank=True, null=True)
    owner_type1 = models.ForeignKey(ContentType, blank=True, null=True,
                                    related_name='journal_transact_owner1_set')
    owner1 = generic.GenericForeignKey('owner_type1', 'owner_id1')
    
    owner_name2 = models.CharField(max_length=255, blank=True)
    owner_id2 = models.IntegerField(blank=True, null=True)
    owner_type2 = models.ForeignKey(ContentType, blank=True, null=True,
                                    related_name='journal_transact_owner2_set')
    owner2 = generic.GenericForeignKey('owner_type2', 'owner_id2')

    arg_name = models.CharField(max_length=255, blank=True)
    arg_id = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    reason = models.TextField(blank=True)
    tax_receiver = models.ForeignKey('ApiPlayerCorporation', blank=True, 
                                     null=True)
    tax_amount = models.FloatField(blank=True, null=True)

    objects = models.Manager()
    #api = ApiPlayerCharacterManager()
        
    class Meta:
        app_label = 'eve_api'
        verbose_name = 'Journal Transaction'
        verbose_name_plural = 'Journal Transactions'
        
    def __unicode__(self):
        return "%s (%d)" % ("Transaction", self.id)

    def __str__(self):
        return self.__unicode__()