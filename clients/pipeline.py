import os

from .lib.constants import ClientConstants
from .customers import DentaLinkClient


class ClientPipeline:
    clients_map = {ClientConstants.CUSTOMER_KEY_DATALINK: DentaLinkClient}

    def __new__(cls, customer_key: str, **kwargs):
        if customer_key not in cls.clients_map:
            raise ValueError("Unknown customer key")
        for env_key, keyword in ClientConstants.ENV_KEY_TO_KEYWORD.items():
            if keyword not in kwargs and env_key in os.environ:
                kwargs[keyword] = os.environ[env_key]
        client_class = cls.clients_map[customer_key]
        return client_class(**kwargs)
