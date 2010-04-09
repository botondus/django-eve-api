from xml.dom import minidom
from eve_proxy.models import CachedDocument

def query_get_model_from_name(child_model, name, **kwargs):
    """
    Queries the EVE API looking for the ID of the specified corporation,
    alliance, or character based on its name. This is not case sensitive.
    
    NOTE: Type checking is not possible from the API. Be very careful where
          you use this, or you might end up with a Player object that has
          the ID of an Alliance that will never be populated.
    
    name: (str) Name to search for.
    """
    query_doc = CachedDocument.objects.api_query('/eve/CharacterID.xml.aspx',
                                                 params={'names': name},
                                                 **kwargs)
    query_dat = query_doc.body.decode("utf-8", "replace")
    dom = minidom.parseString(query_dat)
    
    id_node = dom.getElementsByTagName('row')[0]
    object_id = id_node.getAttribute('characterID')
    
    if object_id == '0':
        raise child_model.DoesNotExist('API returned no matches for the given name.')
    else:
        ret_obj, created = child_model.objects.get_or_create(id=int(object_id))

        if ret_obj.name != name:
            # If there is no name set on the object, update it to match what the
            # user provided, since it matched the EVE API.
            ret_obj.name = name
            ret_obj.save()
            
        # Return reference to the object, with name set.
        return ret_obj 