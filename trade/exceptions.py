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

class InsufficientFundsError(Error):
    """
    Error when account does not have enough funds
    """
    pass

class InvalidOrderError(Error):
    """
    Error when trader cannot fulfill order because it is invalid
    """
    pass
