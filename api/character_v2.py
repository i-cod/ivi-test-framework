import http
from typing import Optional

import requests as requests
from requests.auth import HTTPBasicAuth

from settings import Config


class CharacterV2:

    def __init__(self):
        self.config: Config = Config()

    def get_by_name(self, params: Optional[dict], auth: Optional[HTTPBasicAuth],
                    status_code: http.HTTPStatus) -> requests.Response:
        url = f"{self.config.host}/v2/character"
        if auth is None:
            response = requests.get(url, params=params)
        else:
            response = requests.get(url, params=params, auth=auth)
            print("\n request: ", response.request.url)
        assert response.status_code == status_code, f"Невалидный статус-код для запроса GET {url}. " \
                                                    f"Полученный: {response.status_code}, ожидаемый: {status_code}"

        return response

    def get_list(self, auth: Optional[HTTPBasicAuth], status_code: http.HTTPStatus) -> requests.Response:
        url = f"{self.config.host}/v2/characters"
        if auth is None:
            response = requests.get(url)
        else:
            response = requests.get(url, auth=auth)
        assert response.status_code == status_code, f"Невалидный статус-код для запроса GET {url}. " \
                                                    f"Полученный: {response.status_code}, ожидаемый: {status_code}"

        return response

    def create(self, json: Optional[dict], auth: Optional[HTTPBasicAuth],
               status_code: http.HTTPStatus) -> requests.Response:
        url = f"{self.config.host}/v2/character"
        if auth is None:
            response = requests.post(url, json=json)
        else:
            response = requests.post(url, json=json, auth=auth)
        assert response.status_code == status_code, f"Невалидный статус-код для запроса POST {url}. " \
                                                    f"Полученный: {response.status_code}, ожидаемый: {status_code}"

        return response

    def update(self, json: Optional[dict], auth: Optional[HTTPBasicAuth],
               status_code: http.HTTPStatus) -> requests.Response:
        url = f"{self.config.host}/v2/character"
        if auth is None:
            response = requests.put(url, json=json)
        else:
            response = requests.put(url, json=json, auth=auth)
        assert response.status_code == status_code, f"Невалидный статус-код для запроса POST {url}. " \
                                                    f"Полученный: {response.status_code}, ожидаемый: {status_code}"

        return response

    def delete(self, params: Optional[dict], auth: Optional[HTTPBasicAuth],
               status_code: http.HTTPStatus) -> requests.Response:
        url = f"{self.config.host}/v2/character"
        if auth is None:
            response = requests.delete(url, params=params)
        else:
            response = requests.delete(url, params=params, auth=auth)
        assert response.status_code == status_code, f"Невалидный статус-код для запроса DELETE {url}. " \
                                                    f"Полученный: {response.status_code}, ожидаемый: {status_code}"

        return response
