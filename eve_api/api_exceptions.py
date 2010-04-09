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