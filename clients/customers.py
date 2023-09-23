import json
from datetime import date
from typing import Dict, List, Optional

from requests import Response

from .lib.constants import ClientConstants
from .lib.exceptions import ClientError

from .base import AppointmentClientBase


class DentaLinkClient(AppointmentClientBase):
    base_url = ClientConstants.BASE_URL_DENTALINK

    def get_headers(self, **kwargs) -> Dict:
        token_keyword = ClientConstants.KEYWORD_DENTALINK_TOKEN
        if token_keyword not in kwargs:
            raise ClientError(
                ClientConstants.ERROR_REQUIRED_KEYWORD.format(keyword=token_keyword)
            )
        token = kwargs[token_keyword]
        return {"Authorization": f"Token {token}"}

    def get_url(
        self, from_date: Optional[date] = None, to_date: Optional[date] = None, **kwargs
    ) -> str:
        query = {}
        if from_date:
            query["fecha"] = {"gte": str(from_date)}
        if to_date:
            query["fecha"] = {**query.get("fecha", {}), "lte": str(to_date)}
        if query:
            query_string = json.dumps(query)
            return f"{self.base_url}?q={query_string}"
        return self.base_url

    def serialize_response(self, response: Response) -> List:
        json_data = response.json()
        if "links" not in json_data or "data" not in json_data:
            raise ClientError(**json_data)
        if "next" in json_data["links"]:
            # todo: continue the search by making new queries
            pass
        return json_data["data"]

    def confirm(self, appointment_id: int) -> bool:
        status_id = ClientConstants.DENTALINK_CONFIRM_STATUS_ID
        return self._set_appointment_status(
            appointment_id=appointment_id, status_id=status_id
        )

    def cancel(self, appointment_id: int) -> bool:
        status_id = ClientConstants.DENTALINK_CANCEL_STATUS_ID
        return self._set_appointment_status(
            appointment_id=appointment_id, status_id=status_id
        )

    def _set_appointment_status(self, appointment_id: int, status_id: int) -> bool:
        url = f"{self.base_url}{appointment_id}"
        data = {"id_estado": status_id}
        response = self._put(url=url, data=data)
        json_data = response.json()
        return json_data["data"]["id_estado"] == status_id
