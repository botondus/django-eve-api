"""
This module pulls all of the Journal transaction types from the API and
stores them in ApiJournalRefType objects. This is a fairly quick
operation that should only need to be done at initial setup, and as CCP adds
additional types.
"""
from xml.etree import ElementTree
from eve_proxy.models import CachedDocument
from eve_api.api_puller.util import get_api_model_class

def query_type_list(**kwargs):
    """
    This function is called to update the reference type list objects.
    """
    type_doc = CachedDocument.objects.api_query('/eve/RefTypes.xml.aspx ',
                                                    **kwargs)
    
    tree = ElementTree.fromstring(type_doc.body)
    type_rowset = tree.find('result/rowset').getchildren()
    
    for type_node in type_rowset:
        type_id = int(type_node.get('refTypeID'))
        
        ApiJournalRefType = get_api_model_class('ApiJournalRefType')
        reftype, created = ApiJournalRefType.objects.get_or_create(id=type_id)
        reftype.name = type_node.get('refTypeName')
        reftype.save()
