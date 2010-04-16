import unittest
from django.conf import settings
from eve_api.models import *

class ApiAccountTests(unittest.TestCase):
    """
    Tests ApiAccount.
    """
    def setUp(self):
        self.api_key = settings.EVE_API_USER_KEY
        self.user_id = settings.EVE_API_USER_ID
    
    def test_manager_query(self):
        """
        Tests the standard CharacterList API call.
        """
        # Just use the values from settings.py, since they should theoretically
        # match up to a valid account.
        account = ApiAccount.api.get_account(self.api_key, self.user_id)
        self.assertTrue(account)
        
    def test_update_object(self):
        """
        Checks updating a specific ApiAccount object.
        """
        # Get an ApiAccount object to update. This is not normally how we'd
        # do this, but it ensures we have a valid object to work with.
        account = ApiAccount.api.get_account(self.api_key, self.user_id)
        # Update the ApiAccount object.
        self.assertTrue(account.update_from_api())