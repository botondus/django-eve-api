from xml.etree import ElementTree
from eve_proxy.models import CachedDocument

def query_get_object_from_name(child_model, names, update_missing_names=True,
                               fail_silently=False, **kwargs):
    """
    Queries the EVE API looking for the ID of the specified corporation,
    alliance, or character based on its name. This is not case sensitive.
    
    Returns a list of updated objects, or an empty list if there were
    no matches.
    
    NOTE: Type checking is not possible from the API. Be very careful where
          you use this, or you might end up with a Player object that has
          the ID of an Alliance that will never be populated.
    
    child_model: (Model) Model of the type of object we're querying for.
    names: (str or list) At least one name to search for. A list of names
                         may be used to query in bulk.
    update_missing_names: (bool) If an object instance doesn't already have a
                                 name set, set/save it if this is True.
    fail_silently: (bool) In the case where no match could be found, if this is
                          False, raise a DoesNotExist exception. If True, just
                          continue to the next name and don't return the
                          missing object in the results list.
    """
    # We have to be able to accept a single name in the form of a string, or
    # a list of strings to look up in bulk.
    if hasattr(names, 'pop'):
        # Looks like a list.
        names_str = ','.join(names)
    else:
        # Probably a string.
        names_str = names

    query_doc = CachedDocument.objects.api_query('/eve/CharacterID.xml.aspx',
                                                 params={'names': names_str},
                                                 **kwargs)
    query_dat = query_doc.body.decode("utf-8", "replace")
    tree = ElementTree.fromstring(query_dat)
    rowset_node = tree.find('result/rowset')
    row_nodes = rowset_node.getchildren()
    
    # Store the queried objects in here to return later.
    query_results = []
    for result_node in row_nodes:
        object_id = result_node.get('characterID')
        object_name = result_node.get('name')
        
        if object_id == '0' and not fail_silently:
            # Failing a match noisily.
            error_msg = 'API returned no matches for the given name: %s' % object_name
            raise child_model.DoesNotExist(error_msg)
        elif object_id == '0':
            # Failing silently, just omit this one from the results.
            continue
        else:
            # This is a good result.
            ret_obj, created = child_model.objects.get_or_create(id=int(object_id))
    
            if update_missing_names and ret_obj.name != object_name:
                # If there is no name set on the object, update it to match what the
                # user provided, since it matched the EVE API.
                ret_obj.name = object_name
                ret_obj.save()
                
            # Return reference to the object, with name set.
            query_results.append(ret_obj)
    
    return query_results