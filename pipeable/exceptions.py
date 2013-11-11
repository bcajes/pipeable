class SkipPipeItem(Exception):
    """ Raised when pipe in pipeline should be skipped, based on group
    """
    pass

class InvalidPipeInput(ValueError):
    """ Raised when unexpected pipe input is found
    """
    pass
