from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from eve_api.app_defines import API_STATUS_CHOICES, API_STATUS_PENDING
from eve_api.api_puller.account import character_list
from eve_api.models.base import ApiModel

class ApiAccountManager(models.Manager):
    def get_via_credentials(self, api_key, user_id, **kwargs):
        """
        Retrieves an ApiAccount object based on data from the API. If the
        ApiAccount object does not already exist for this account, create
        and update it. For existing accounts, update the account data and
        return the updated ApiAccount.
        """
        return character_list.query_character_list(api_key, user_id, **kwargs)

class ApiAccount(ApiModel):
    """
    Use this class to store EVE user account information. Note that its use is
    entirely optional and up to the developer's discretion.
    """
    user = models.ForeignKey(User, blank=True, null=True,
                             help_text="User that owns this account")
    description = models.CharField(max_length=50, blank=True,
                                   help_text="User-provided description.")
    api_key = models.CharField(max_length=64, verbose_name="API Key")
    api_user_id = models.IntegerField(verbose_name="API User ID")
    characters = models.ManyToManyField("ApiPlayerCharacter", blank=True,
                                        null=True)
    api_status = models.IntegerField(choices=API_STATUS_CHOICES,
                                     default=API_STATUS_PENDING,
                                     verbose_name="API Status",
                                     help_text="End result of the last attempt at updating this object from the API.")
    
    objects = models.Manager()
    api = ApiAccountManager()

    class Meta:
        app_label = 'eve_api'
        verbose_name = 'EVE Account'
        verbose_name_plural = 'EVE Accounts'
        ordering = ['api_user_id']
        
    def __unicode__(self):
        return "%s (Account: %d)" % (self.user, self.id)

    def __str__(self):
        return self.__unicode__()
    
    def update_from_api(self, **kwargs):
        """
        Updates this account from the EVE API if an api_key and api_user_id is
        specified.
        """
        return character_list.query_character_list(self.api_key, 
                                                   self.api_user_id,
                                                   account_obj=self,
                                                   **kwargs)
    
    def get_absolute_url(self):
        return reverse('profiles-edit_eve_account', args=[self.id])