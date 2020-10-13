class LinxClientException(Exception):
    """
    Base exception for the python linx client.
    """
    pass


class ConfigException(LinxClientException):
    """
    Signals a problem with the configuration.
    """
    pass
