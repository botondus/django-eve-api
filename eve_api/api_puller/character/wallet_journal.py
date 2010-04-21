"""
/char/WalletJournal.xml.aspx

http://wiki.eve-id.net/APIv2_Char_JournalEntries_XML
"""
from datetime import datetime
from xml.etree import ElementTree
from eve_proxy.models import CachedDocument
from eve_db.models import StaStation, CrpNPCCorporation
from eve_api.api_puller.util import get_api_model_class, parse_api_datetime

def __resolve_generic_relation(generic_id, generic_name, ApiPlayerCharacter, 
                               ApiPlayerCorporation):
    """
    Given ownerID1 or ownerID2, determine the object that its pointing to.
    """
    if generic_id == '0':
        # This is probably something like a Market Escrow, where there is
        # no real owner2.
        return None

    try:
        # Look through existing characters first, since the bulk of
        # transactions happen between players.
        character = ApiPlayerCharacter.objects.get(id=generic_id)
        if not character.name:
            # This guy is missing a name, save it.
            character.name = generic_name
            character.save()
        return character
    except:
        # This doesn't match any current characters, but doesn't necessarily
        # rule the possibility out.
        pass
    
    try:
        # NPC Corporations are static data, so this is a quick and
        # easy thing to check and rule out.
        return CrpNPCCorporation.objects.get(id=generic_id)
    except:
        # Not an NPC corporation. We can completely rule this possiblity out.
        pass
    
    try:
        # See if there's already a player corporation on record for this
        # transaction.
        return ApiPlayerCorporation.objects.get(id=generic_id)
    except:
        # Not a currently recorded player corporation.
        pass
    try:
        return ApiPlayerCorporation.api.get_via_id(generic_id, no_cache=True)
    except ApiPlayerCorporation.DoesNotExist:
        # Definitely not a player corporation.
        pass
    
    # It must be a character at this point, we've ruled out all of the other
    # scenarios.
    character, created = ApiPlayerCharacter.objects.get_or_create(id=generic_id)
    if not character.name:
        character.name = generic_name
        character.save()
    return character

def __import_transaction(elem, ApiJournalTransaction, ApiJournalRefType,
                         ApiPlayerCorporation):
    """
    Given an ElementTree Element, parse it for Journal transaction data and
    import it to the DB.
    """
    ref_id = elem.get('refID')
    ref_type_id = elem.get('refTypeID')
    
    transaction, created = ApiJournalTransaction.objects.get_or_create(id=ref_id)
    transaction.transaction_time = parse_api_datetime(elem.get('date'))
    ref_type, created = ApiJournalRefType.objects.get_or_create(id=ref_type_id)
    transaction.ref_type = ref_type
    transaction.owner_name1 = elem.get('ownerName1')
    transaction.owner_name2 = elem.get('ownerName2')
    transaction.arg_name = elem.get('argName1')
    transaction.arg_id = elem.get('argID1')
    transaction.amount = elem.get('amount')
    transaction.balance = elem.get('balance')
    transaction.reason = elem.get('reason')
    
    # For things like bounties, taxes get paid to the player's corp.
    tax_amount = elem.get('taxAmount')
    if tax_amount:
        transaction.tax_amount = tax_amount
    tax_receiver_id = elem.get('taxReceiverID')
    if tax_receiver_id:
        tax_receiver, created = ApiPlayerCorporation.objects.get_or_create(id=tax_receiver_id)
        transaction.tax_receiver = tax_receiver
    
    # Get around circular dependencies.
    ApiPlayerCharacter = get_api_model_class('ApiPlayerCharacter')
    ApiPlayerCorporation = get_api_model_class('ApiPlayerCorporation')

    # Resolve the generic relationships by the ownerID* values.
    transaction.owner1 = __resolve_generic_relation(elem.get('ownerID1'),
                                                    transaction.owner_name1,
                                                    ApiPlayerCharacter, 
                                                    ApiPlayerCorporation)
    transaction.owner2 = __resolve_generic_relation(elem.get('ownerID2'),
                                                    transaction.owner_name2,
                                                    ApiPlayerCharacter, 
                                                    ApiPlayerCorporation)

    # This also saves changes.
    transaction.set_api_last_updated()

def query_character_journal(character_or_id, account_key=1000, 
                            before_ref_id=None, **kwargs):
    """
    This function queries a character's journal and creates/updates
    ApiJournalTransaction objects found therein.
    """
    try:
        # If the user has provided an int, this will fail.
        id = character_or_id.id
        # User has provided a corp object, use that instead of looking one up.
        character = character_or_id
    except AttributeError:
        # User provided an int, no corp object provided.
        id = character_or_id
        character = None
    
    # This raises a ApiAccount.DoesNotExist if there is no match.
    account = character.get_account()
    
    # Assemble GET keys.
    query_params = {'userID': account.api_user_id,
                    'apiKey': account.api_key,
                    'characterID': character.id,
                    'accountKey': account_key}
    
    if before_ref_id:
        # This allows for walking journal transactions backwards.
        # http://wiki.eve-id.net/APIv2_Char_JournalEntries_XML
        query_params['beforeRefID'] = before_ref_id

    # Retrieve the XML for the query from the API or the cache.
    corp_doc = CachedDocument.objects.api_query('/char/WalletJournal.xml.aspx',
                                                params=query_params, **kwargs)
    # Parse the XML response.
    tree = ElementTree.fromstring(corp_doc.body)
    
    # List of <row> elements, each being a transaction.
    transactions = tree.find('result/rowset').getchildren()
    
    # The following calls get around circular imports.
    ApiJournalTransaction = get_api_model_class('ApiJournalTransaction')
    ApiJournalRefType = get_api_model_class('ApiJournalRefType')
    ApiPlayerCorporation = get_api_model_class('ApiPlayerCorporation')

    for transaction in transactions:
        # Hand off importing logic.
        __import_transaction(transaction, ApiJournalTransaction,
                             ApiJournalRefType, ApiPlayerCorporation)
    