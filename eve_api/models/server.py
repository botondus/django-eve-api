from django.db import models
from eve_api.api_puller.server import server_status
from eve_api.models.base import ApiModel

class ApiServerManager(models.Manager):
    def get_status(self, **kwargs):
        """
        Returns an up-to-date ApiServer object with server status details.
        
        Retrieve the ApiServer through here, instead of going
        through ApiServer's manager.
        """
        return server_status.query_server_status(**kwargs)

class ApiServer(ApiModel):
    """
    Represents the Tranquility cluster.
    """
    server_open = models.BooleanField(default=True)
    online_players = models.IntegerField(default=0)
    
    objects = models.Manager()
    api = ApiServerManager()
    
    class Meta:
        app_label = 'eve_api'
        verbose_name = 'Server'
        verbose_name_plural = 'Server'
    
    def __unicode__(self):
        return 'Tranquility'
        
    def __str__(self):
        return self.__unicode__()