# Only mess with the environmental stuff if this is being ran directly.
from importer_path import fix_environment
fix_environment()
from eve_api.models import *
from eve_proxy.models import CachedDocument
"""
corp = ApiPlayerCorporation.api.get_via_name("Blackman Industries",
                                             no_cache=False)
corp.name = "YARR"
print corp.name
corp.update_from_api()
print corp.name
"""
"""
corp = ApiPlayerCorporation.api.get_via_name("Blackman Industries",
                                             no_cache=False)
print "CORP", corp
print "ID", corp.id
charact = ApiPlayerCharacter.objects.all()[0]
corp = ApiPlayerCorporation.api.get_via_id(corp.id, query_character=charact,
                                           no_cache=False)
print "BY ID", corp
"""
"""
account = ApiAccount.objects.all()[0]
account.update_from_api()
"""
#ApiJournalRefType.api.update_all_types()

#print ApiPlayerCharacter.api.get_via_name("Ilyk Halibut")
#ApiPlayerAlliance.api.update_all_alliances(no_cache=True)
#print ApiPlayerAlliance.api.get_via_name("Atlas Alliance")
#ApiPlayerAlliance.api.update_all_corporations(no_cache=True)
#print "OPEN", ApiServer.api.get_status().online_players

charact = ApiPlayerCharacter.objects.get(name='Ilyk Halibut')
print charact
charact.update_journal_from_api(no_cache=False)

#CachedDocument.objects.clean_expired_entries()