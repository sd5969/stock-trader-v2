"""
Base Exceptions Classes
"""

class Error(Exception):
    """
    Base class for all exceptions
    """
    pass

class InsufficientArgumentsError(Error):
    """
    Error when arguments sent are inadequate
    """
    pass
