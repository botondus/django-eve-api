"""
Various useful functions for the API pullers.
"""
from datetime import datetime
from django.contrib.contenttypes.models import ContentType

def get_api_model_class(model_name):
    """
    Convenience function to return an API model class. Used to prevent
    circular imports.
    """
    model_name = model_name.lower()
    return ContentType.objects.get(app_label="eve_api", 
                                   model=model_name).model_class()
                                   
def parse_api_datetime(datetime_str):
    """
    Parses a datetime value from EVE's API.
    """
    dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return dt