from datetime import datetime
from django.db import models

class ApiModel(models.Model):
    """
    A simple abstract base class to set some consistent fields on the models
    that are updated from the EVE API.
    """
    api_last_updated = models.DateTimeField(blank=True, null=True,
                                            verbose_name="Time last updated from API",
                                            help_text="When this object was last updated from the EVE API.")
    
    class Meta:
        abstract = True
        
    def set_api_last_updated(self):
        """
        Sets the object's api_last_updated value to the current time. We do
        this manually because not all object saves are API updates.
        """
        self.api_last_updated = datetime.now()
        self.save()