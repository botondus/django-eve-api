"""
Contains exeptions used in the eve_api app.
"""
class APIInvalidCorpIDException(Exception):
    """
    Raised when an invalid corp id is given in an api query.
    """
    def __init__(self, id):
        self.value = "ID: %s does not match any corporation." % id
        
    def __str___(self):
        return repr(self.value)

class APIAuthException(Exception):
    """
    Raised when an invalid userID and/or authKey were provided.
    """
    def __str__(self):
        return "An authentication was encountered while querying the EVE API."
    
class APINoUserIDException(Exception):
    """
    Raised when a userID is required, but missing or mal-formed.
    """
    def __str__(self):
        return "This query requires a valid userID, but yours is either missing or invalid."