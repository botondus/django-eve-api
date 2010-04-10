from xml.etree import ElementTree
from django.contrib.contenttypes.models import ContentType
from eve_proxy.models import CachedDocument

def query_server_status(**kwargs):
    """
    Populates and returns an ApiServer object.
    """
    server_doc = CachedDocument.objects.api_query('/server/ServerStatus.xml.aspx',
                                                  **kwargs)
    tree = ElementTree.fromstring(server_doc.body)
    
    server_open = tree.find('result/serverOpen').text
    online_players = tree.find('result/onlinePlayers').text
    
    ApiServer = ContentType.objects.get(app_label="eve_api", 
                                        model="apiserver").model_class()
                                        
    server, created = ApiServer.objects.get_or_create(id=1)
    server.server_open = server_open == 'True'
    server.online_players = online_players
    server.save()
    return server
    