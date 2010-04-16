"""
/corp/CorporationSheet.xml

http://wiki.eve-id.net/APIv2_Corp_CorporationSheet_XML
"""
from xml.etree import ElementTree
from eve_proxy.models import CachedDocument
from eve_db.models import StaStation
from eve_api.api_puller.util import get_api_model_class

def __transfer_common_values(tree, corp):
    """
    This function transfers a bunch of simple fields that don't require
    FK lookups.
    """
    # Tuples of pairings of tag names and the attribute on the Corporation
    # object to set the data to. First member of the tuple is the API's
    # name, second member is the attribute name on the model to transfer into.
    tag_mappings = (
        ('corporationName', 'name'),
        ('ticker', 'ticker'),
        ('url', 'url'),
        ('description', 'description'),
        ('memberCount', 'member_count'),
        ('memberLimit', 'member_limit'),
        ('taxRate', 'tax_rate'),
        ('shares', 'shares'),
        ('logo/graphicID', 'logo_graphic_id'),
        ('logo/shape1', 'logo_shape1'),
        ('logo/shape2', 'logo_shape2'),
        ('logo/shape3', 'logo_shape3'),
        ('logo/color1', 'logo_color1'),
        ('logo/color2', 'logo_color2'),
        ('logo/color3', 'logo_color3'),
    )
    
    # Iterate through the tag mappings, setting the values of the tag names
    # (first member of the tuple) to the attribute named in the second member
    # of the tuple on the ApiPlayerCorporation object.
    for tag_map in tag_mappings:
        try:
            setattr(corp, tag_map[1], tree.find('result/%s' % tag_map[0]).text)
        except AttributeError:
            # This is a restricted field that we don't have
            # access to. Ignore.
            continue

def __transfer_ceo(tree, corp):
    """
    Transfers the CEO data.
    """
    ApiPlayerCharacter = get_api_model_class("apiplayercharacter")
    ceo_id = int(tree.find('result/ceoID').text)
    ceo, created = ApiPlayerCharacter.objects.get_or_create(id=ceo_id)
    corp.ceo_character = ceo
    
    if not ceo.name:
        # Fill in the CEO's name if it's missing from their ApiPlayer object.
        ceo.name = ceo_id = tree.find('result/ceoName').text
        ceo.save()

def __transfer_alliance(tree, corp):
    """
    Transfers alliance data (if applicable).
    """
    alliance_id = int(tree.find('result/allianceID').text)
    if alliance_id != 0:
        ApiPlayerAlliance = get_api_model_class("apiplayeralliance")
        alliance, created = ApiPlayerAlliance.objects.get_or_create(id=alliance_id)
        corp.alliance = alliance
        if not alliance.name:
            # Alliance name is missing from the ApiPlayerAlliance object.
            # Set it and save it.
            alliance.name = ceo_id = tree.find('result/allianceName').text
            alliance.save()
            
def __transfer_station(tree, corp):
    """
    Transfers home station data.
    """
    station_id = int(tree.find('result/stationID').text)
    station, created = StaStation.objects.get_or_create(id=station_id)
    station_name = tree.find('result/stationName').text
    if station.name != station_name:
        # This shouldn't happen, but if it does, use the most up-to-date
        # data (which is probably what is coming from the API).
        station.name = station_name
        station.save()
    corp.hq_station = station
    
def __transfer_divisions(tree, corp):
    """
    Transfer corporate divisions and wallet divisions.
    """
    ApiPlayerCorporationDivision = get_api_model_class("apiplayercorporationdivision")
    ApiPlayerCorporationWalletDivision = get_api_model_class("apiplayercorporationwalletdivision")
    rowsets = tree.findall('result/rowset')
    for rowset in rowsets:
        rowset_name = rowset.get('name')
        for row in rowset.getchildren():
            account_key = row.get('accountKey')
            if rowset_name == 'divisions':
                division, created = ApiPlayerCorporationDivision.objects.get_or_create(
                                                        account_key=account_key,
                                                        corporation=corp)
            elif rowset_name =='walletDivisions':
                division, created = ApiPlayerCorporationWalletDivision.objects.get_or_create(
                                                        account_key=account_key,
                                                        corporation=corp)
            else:
                # This shouldn't happen unless CCP adds a new rowset type
                # and we don't support it yet.
                continue                    
            division.name = row.get('description')
            division.save()

def query_corporation_sheet(corp_or_id, query_character=None, **kwargs):
    """
    Returns a corp's data sheet from the EVE API in the form of an 
    ElementTree Element.
    
    corp_or_id: (ApiPlayerCorporation or int) A player corporation object to
                update, or an int matching a corporation's ID number.
    query_character: (ApiPlayerCharacter) To get detailed data about a corp,
                     provide a character that is a member of said corp.
    """
    try:
        # If the user has provided an int, this will fail.
        id = corp_or_id.id
        # User has provided a corp object, use that instead of looking one up.
        corp = corp_or_id
    except AttributeError:
        # User provided an int, no corp object provided.
        id = corp_or_id
        corp = None
    
    query_params = {}
    if query_character:
        # Character provided, provide their credentials.
        account = query_character.apiaccount_set.all()[0]
        query_params['userID'] = account.api_user_id
        query_params['apiKey'] = account.api_key
        query_params['characterID'] = query_character.id
    else:
        # Outsider is looking for details on a corp.
        query_params['corporationID'] = id

    corp_doc = CachedDocument.objects.api_query('/corp/CorporationSheet.xml.aspx',
                                                params=query_params, **kwargs)
    #corp_dat = corp_doc.body.decode("utf-8", "replace")
    #u_attr = unicode(corp_doc.body, 'ascii')
    #corp_dat = u_attr.encode("utf-8", "replace")
    
    # Convert incoming data to UTF-8.
    #print "RAW", corp_doc.body
    tree = ElementTree.fromstring(corp_doc.body)
    
    error_node = tree.find('result/error')
    # If there's an error, see if it's because the corp doesn't exist.
    if error_node:
        error_code = error_node.get('code')
        if error_code == '523':
            raise APIInvalidCorpIDException(id)
    
    if not corp:
        # User did not provide a corporation object, find or create one
        # to update and return.
        ApiPlayerCorporation = get_api_model_class("apiplayercorporation")
        corp, created = ApiPlayerCorporation.objects.get_or_create(id=int(id))
    
    __transfer_common_values(tree, corp)
    __transfer_ceo(tree, corp)
    __transfer_alliance(tree, corp)
    __transfer_station(tree, corp)
    corp.save()
    __transfer_divisions(tree, corp)
    corp.set_api_last_updated()

    # This is more useful in the case where a user provides an int.
    return corp