import pytest
from datetime import date
from unittest import mock

from clients.customers import DentaLinkClient
from clients.lib.constants import ClientConstants
from clients.lib.exceptions import ClientError


class TestDentaLinkClient:
    def test_without_token(self):
        with pytest.raises(ClientError) as error:
            DentaLinkClient()
        assert str(error.value) == "Keyword token is required"

    @mock.patch("clients.base.Session")
    def test_get(self, mocked_session_class, dentalink_token):
        mocked_session = mock.Mock()
        mocked_session_class.return_value = mocked_session
        api_response = {"data": [{"id": 0}], "links": []}
        mocked_response = mock.Mock()
        mocked_response.json.return_value = api_response
        mocked_session.get.return_value = mocked_response

        client = DentaLinkClient(token=dentalink_token)
        response = client.get(
            from_date="2023-08-01",
            to_date=date(2023, 8, 30),
        )
        assert response == api_response["data"]
        returned_data = client.get()
        assert returned_data == api_response["data"]

    @mock.patch("clients.base.Session")
    def test_confirm(self, mocked_session_class, dentalink_token):
        mocked_session = mock.Mock()
        mocked_session_class.return_value = mocked_session
        appointment_id = 1
        status_id = ClientConstants.DENTALINK_CONFIRM_STATUS_ID
        api_response = {"data": {"id": appointment_id, "id_estado": status_id}}
        mocked_response = mock.Mock()
        mocked_response.json.return_value = api_response
        mocked_session.put.return_value = mocked_response

        client = DentaLinkClient(token=dentalink_token)
        assert client.confirm(appointment_id=appointment_id) is True

    @mock.patch("clients.base.Session")
    def test_cancel(self, mocked_session_class, dentalink_token):
        mocked_session = mock.Mock()
        mocked_session_class.return_value = mocked_session
        appointment_id = 1
        status_id = ClientConstants.DENTALINK_CANCEL_STATUS_ID
        api_response = {"data": {"id": appointment_id, "id_estado": status_id}}
        mocked_response = mock.Mock()
        mocked_response.json.return_value = api_response
        mocked_session.put.return_value = mocked_response

        client = DentaLinkClient(token=dentalink_token)
        assert client.cancel(appointment_id=appointment_id) is True
