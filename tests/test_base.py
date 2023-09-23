from datetime import date
from unittest import mock

import pytest
from requests import Session, RequestException

from clients.base import AppointmentClientBase
from clients.lib.exceptions import ClientError


class TestAppointmentClientBase:
    def test_init(self):
        client = AppointmentClientBase()
        assert isinstance(client.session, Session)

    def test_init_with_headers(self):
        header_key = "fake_token"
        kwargs = {header_key: "FAKE"}
        client = AppointmentClientBase(**kwargs)
        assert client.session.headers[header_key] == kwargs[header_key]

    @mock.patch("clients.base.Session")
    def test_get(self, mocked_session_class):
        mocked_session = mock.Mock()
        mocked_session_class.return_value = mocked_session
        expected_response = {"data": [], "links": []}
        mocked_response = mock.Mock()
        mocked_response.json.return_value = expected_response
        mocked_session.get.return_value = mocked_response

        client = AppointmentClientBase()
        returned_data = client.get(from_date="2000-01-01", to_date=date(2000, 1, 1))
        assert returned_data == expected_response
        assert client.get() == expected_response

    def test_confirm(self):
        client = AppointmentClientBase()
        with pytest.raises(NotImplementedError):
            client.confirm(appointment_id=None)

    def test_cancel(self):
        client = AppointmentClientBase()
        with pytest.raises(NotImplementedError):
            client.cancel(appointment_id=None)

    @mock.patch("clients.base.Session")
    def test_get_api_response_error(self, mocked_session_class):
        mocked_session = mock.Mock()
        mocked_session.get.side_effect = RequestException
        mocked_session_class.return_value = mocked_session
        client = AppointmentClientBase()
        with pytest.raises(ClientError):
            client.get_api_response()

    @mock.patch("clients.base.Session")
    def test__put(self, mocked_session_class):
        mocked_session = mock.Mock()
        mocked_session.put.side_effect = RequestException
        mocked_session_class.return_value = mocked_session
        client = AppointmentClientBase()
        with pytest.raises(ClientError):
            client._put(url="", data={})
