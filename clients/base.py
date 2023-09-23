from datetime import date, datetime
from typing import Dict, List, Optional, Union

from requests import Response, RequestException, Session

from .lib.exceptions import ClientError


class AppointmentClientBase:
    date_formats = ["%Y-%m-%d"]
    base_url = None

    def __init__(self, **kwargs):
        headers = self.get_headers(**kwargs)
        self.session = self.get_session(headers=headers)

    def get_headers(self, **kwargs) -> Dict:
        return kwargs

    def get_session(self, headers: Optional[Dict] = None) -> Session:
        session = Session()
        if headers:
            session.headers.update(headers)
        return session

    def get(
        self,
        from_date: Optional[Union[str, date]] = None,
        to_date: Optional[Union[str, date]] = None,
        **kwargs,
    ):
        from_date = self._serialize_date(_date=from_date)
        to_date = self._serialize_date(_date=to_date)
        response = self.get_api_response(from_date=from_date, to_date=to_date, **kwargs)
        return self.serialize_response(response=response)

    def get_api_response(
        self, from_date: Optional[date] = None, to_date: Optional[date] = None, **kwargs
    ) -> Union[List, Dict]:
        url = self.get_url(from_date=from_date, to_date=to_date, **kwargs)
        try:
            response = self.session.get(url)
        except RequestException as error:
            raise ClientError(str(error))
        return response

    def get_url(self, **kwargs) -> str:
        return self.base_url

    def serialize_response(self, response: Response) -> Dict:
        return response.json()

    def _serialize_date(self, _date: Optional[Union[str, date]]) -> Optional[date]:
        if isinstance(_date, date) or _date is None:
            return _date
        serialized_datetime = None
        for _format in self.date_formats:
            try:
                serialized_datetime = datetime.strptime(_date, _format)
            except ValueError:
                continue
        if serialized_datetime:
            return serialized_datetime.date()

    def confirm(self, appointment_id: int) -> Dict:
        raise NotImplementedError

    def cancel(self, appointment_id: int) -> Dict:
        raise NotImplementedError

    def _put(self, url: str, data: Dict) -> Response:
        try:
            response = self.session.put(url, data=data)
        except RequestException as error:
            raise ClientError(str(error))
        return response
