#!/usr/bin/env python
"""
This module abstracts the pulling of account data from the EVE API.
"""
from xml.dom import minidom
from datetime import datetime
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from eve_proxy.models import CachedDocument
from eve_proxy.proxy_exceptions import APIAuthException, APINoUserIDException
from eve_api.app_defines import API_STATUS_OK

def _populate_characters(account, characters_node_children):
    """
    Iterate through an account's character list and create/update the
    appropriate ApiPlayerCharacter objects.
    """
    ApiPlayerCorporation = ContentType.objects.get(app_label="eve_api", 
                                                   model="apiplayercorporation").model_class()
    ApiPlayerCharacter = ContentType.objects.get(app_label="eve_api", 
                                                model="apiplayercharacter").model_class()
    for node in characters_node_children:
        try:
            # Get this first, as it's safe.
            corporation_id = node.getAttribute('corporationID')
            corp, created = ApiPlayerCorporation.objects.get_or_create(id=corporation_id)
            # Do this last, since the things we retrieved above are used
            # on the ApiPlayerCharacter object's fields.
            character_id = node.getAttribute('characterID')
            pchar, created = ApiPlayerCharacter.objects.get_or_create(id=character_id)
            name = node.getAttribute('name')
            # Save these for last to keep the save count low.
            pchar.name = name
            pchar.corporation = corp
            account.characters.add(pchar)
            pchar.save()
        except AttributeError:
            # This must be a Text node, ignore it.
            continue

def query_character_list(api_key, user_id, **kwargs):
    """
    Imports an account from the API into the ApiAccount model.
    
    Optional kwargs
    no_cache: (bool) When True, skip the cache and query the API.
    """
    if not user_id:
        raise APINoUserIDException()
    if not api_key:
        raise APIAuthException()

    auth_params = {'userID': user_id, 'apiKey': api_key}
    account_doc = CachedDocument.objects.api_query('/account/Characters.xml.aspx',
                                                   params=auth_params,
                                                   **kwargs)
    #print account_doc.body

    dom = minidom.parseString(account_doc.body)
    characters_node_children = dom.getElementsByTagName('rowset')[0].childNodes

    ApiAccount = ContentType.objects.get(app_label="eve_api", 
                                         model="apiaccount").model_class()

    # Create or retrieve the account last to make sure everything
    # before here is good to go.
    try:
        account = ApiAccount.objects.get(id=user_id)
    except ApiAccount.DoesNotExist:
        account = ApiAccount(id=user_id)

    account.api_key = api_key
    account.api_user_id = user_id
    account.api_last_updated = datetime.now()
    account.api_status = API_STATUS_OK
    account.save()

    # Iterate through the characters on this account and create/update the
    # appropriate ApiPlayerCharacter models.
    _populate_characters(account, characters_node_children)
    
    # Finally, return the latest version of the ApiAccount.
    return account