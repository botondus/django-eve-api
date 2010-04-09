from xml.dom import minidom
from django.contrib.contenttypes.models import ContentType
from eve_proxy.models import CachedDocument

def query_corporation_sheet(id, query_character=None, **kwargs):
    """
    Returns a corp's data sheet from the EVE API in the form of an XML 
    minidom doc.
    
    query_character: (ApiPlayerCharacter) To get detailed data about a corp,
                     provide a character that is a member of said corp.
    """
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
    corp_dat = corp_doc.body.decode("utf-8", "replace")
    
    # Convert incoming data to UTF-8.
    dom = minidom.parseString(corp_dat)
    
    error_node = dom.getElementsByTagName('error')
    
    # If there's an error, see if it's because the corp doesn't exist.
    if error_node:
        error_code = error_node[0].getAttribute('code')
        if error_code == '523':
            raise APIInvalidCorpIDException(id)
    
    ApiPlayerCorporation = ContentType.objects.get(app_label="eve_api", 
                                                   model="apiplayercorporation").model_class()
    corp, created = ApiPlayerCorporation.objects.get_or_create(id=int(id))
    
    # Tuples of pairings of tag names and the attribute on the Corporation
    # object to set the data to.
    tag_mappings = (
        ('corporationName', 'name'),
        ('ticker', 'ticker'),
        ('url', 'url'),
        ('description', 'description'),
        ('memberCount', 'member_count'),
        ('graphicID', 'logo_graphic_id'),
        ('shape1', 'logo_shape1'),
        ('shape2', 'logo_shape2'),
        ('shape3', 'logo_shape3'),
        ('color1', 'logo_color1'),
        ('color2', 'logo_color2'),
        ('color3', 'logo_color3'),
    )
    
    # Iterate through the tag mappings, setting the values of the tag names
    # (first member of the tuple) to the attribute named in the second member
    # of the tuple on the ApiPlayerCorporation object.
    for tag_map in tag_mappings:
        try:
            setattr(corp, tag_map[1], 
                    dom.getElementsByTagName(tag_map[0])[0].firstChild.nodeValue)
        except AttributeError:
            # This tag has no value, skip it.
            continue
        except IndexError:
            # Something weird has happened
            print " * Index Error:", tag_map[0]
            continue

    corp.save()
    return corp