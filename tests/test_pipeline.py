import pytest
import os

from clients.pipeline import ClientPipeline
from clients.lib.constants import ClientConstants


class TestClientPipeline:
    def test_unknown_customer_key(self):
        with pytest.raises(ValueError) as error:
            ClientPipeline(customer_key="X")
        assert str(error.value) == "Unknown customer key"

    def test_env_key(self):
        fake_token = "FAKE_TOKEN"
        os.environ[ClientConstants.ENV_KEY_DENTALINK_TOKEN] = fake_token
        client = ClientPipeline(customer_key=ClientConstants.CUSTOMER_KEY_DATALINK)

        assert fake_token in client.session.headers["Authorization"]
