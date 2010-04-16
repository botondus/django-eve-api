from xml.etree import ElementTree
from eve_api.api_puller.util import get_api_model_class
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
    
    ApiServer = get_api_model_class('apiserver')
                                        
    server, created = ApiServer.objects.get_or_create(id=1)
    server.server_open = server_open == 'True'
    server.online_players = online_players
    server.save()
    return server
    