"""
Various useful functions for the API pullers.
"""
from django.contrib.contenttypes.models import ContentType

def get_api_model_class(model_name):
    """
    Convenience function to return an API model class. Used to prevent
    circular imports.
    """
    model_name = model_name.lower()
    return ContentType.objects.get(app_label="eve_api", 
                                   model=model_name).model_class()