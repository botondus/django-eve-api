"""
Retrieves a list of characters associated with an account. Includes names,
character IDs, their corporation, etc.

/account/Characters.xml.aspx
http://wiki.eve-id.net/APIv2_Account_Characters_XML
"""
from xml.etree import ElementTree
from datetime import datetime
from django.conf import settings
from eve_api.api_puller.util import get_api_model_class
from eve_proxy.models import CachedDocument
from eve_proxy.proxy_exceptions import APIAuthException, APINoUserIDException
from eve_api.app_defines import API_STATUS_OK

def _populate_characters(account, characters_node_children):
    """
    Iterate through an account's character list and create/update the
    appropriate ApiPlayerCharacter objects.
    """
    ApiPlayerCorporation = get_api_model_class("apiplayercorporation")
    ApiPlayerCharacter = get_api_model_class("apiplayercharacter")

    for node in characters_node_children:
        try:
            # Get this first, as it's safe.
            corporation_id = node.get('corporationID')
            corp, created = ApiPlayerCorporation.objects.get_or_create(id=corporation_id)
            # Do this last, since the things we retrieved above are used
            # on the ApiPlayerCharacter object's fields.
            character_id = node.get('characterID')
            pchar, created = ApiPlayerCharacter.objects.get_or_create(id=character_id)
            name = node.get('name')
            # Save these for last to keep the save count low.
            pchar.name = name
            pchar.corporation = corp
            # This also saves the model.
            pchar.set_api_last_updated()
            account.characters.add(pchar)
        except AttributeError:
            # This must be a Text node, ignore it.
            continue

def query_character_list(api_key, user_id, account_obj=None, **kwargs):
    """
    Imports an account from the API into the ApiAccount model.
    
    Optional kwargs
    account_obj: (ApiAccount) Update the following account object instead
                 of querying for one. This is used to update ApiAccount
                 objects in place.
    """
    if not user_id:
        raise APINoUserIDException()
    if not api_key:
        raise APIAuthException()

    auth_params = {'userID': user_id, 'apiKey': api_key}
    account_doc = CachedDocument.objects.api_query('/account/Characters.xml.aspx',
                                                   params=auth_params,
                                                   **kwargs)

    tree = ElementTree.fromstring(account_doc.body)
    characters_node_children = tree.find('result/rowset').getchildren()

    if account_obj == None:
        # User did not specify an ApiAccount object to use. Query and get or
        # create one with a matching user_id.
        ApiAccount = get_api_model_class("apiaccount")
        # Create or retrieve the account last to make sure everything
        # before here is good to go.
        try:
            account = ApiAccount.objects.get(id=user_id)
        except ApiAccount.DoesNotExist:
            account = ApiAccount(id=user_id)
    else:
        # User specified an ApiAccount object to use.
        account = account_obj

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