from dataclasses import dataclass


@dataclass
class ImproperlyConfigured(Exception):
    """
    :raises Exception if the config file has problems
    """
    text_err: str