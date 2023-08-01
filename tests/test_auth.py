import http

import pytest
from requests.auth import HTTPBasicAuth

from api.character_v2 import CharacterV2
from settings import Config


class TestAuth:

    def test_basic_auth(self):
        """
        Описание:
            Проверка авторизации с валидными данными

        Сценарий:
            Выполнить метод GET /v2/characters c валидным логином и паролем

        Ожидаемый результат:
            Вернулся статус-код 200, ответ содержит список значений
        """
        config = Config()

        auth = HTTPBasicAuth(config.username, config.password)
        response = CharacterV2().get_list(auth=auth, status_code=http.HTTPStatus.OK)
        assert response.json()["result"], "Ответ на запрос не соответствует ожидаемому результату"

    @pytest.mark.parametrize("username, password", [
        (Config().username, "qwerty"),
        (Config().username, ""),
        ("qwerty", "qwerty"),
        ("qwerty", Config().password),
        ("", Config().password)
    ])
    def test_basic_auth_invalid(self, username, password):
        """
        Описание:
            Проверка авторизации с невалидными данными

        Сценарий:
            Выполнить метод GET /v2/characters для следующих комбинаций:
            - валидный логин, невалидный пароль
            - валидный логин, пустой пароль
            - невалидный логин, невалидный пароль
            - невалидный логин, валидный пароль
            - пустой логин, валидный пароль

        Ожидаемый результат:
            Вернулся статус-код 401, ответ содержит описание ошибки
        """
        auth = HTTPBasicAuth(username, password)
        response = CharacterV2().get_list(auth=auth, status_code=http.HTTPStatus.UNAUTHORIZED)
        assert response.json()["error"].lower() == "you have to login with proper credentials", \
            "Ответ на запрос не соответствует ожидаемому результату"

    def test_basic_auth_without_auth_data(self):
        """
        Описание:
            Проверка авторизации без авторизационных данных в запросе

        Сценарий:
            Выполнить метод GET /v2/characters без авторизационных данных

        Ожидаемый результат:
            Вернулся статус-код 401, ответ содержит описание ошибки
        """
        response = CharacterV2().get_list(auth=None, status_code=http.HTTPStatus.UNAUTHORIZED)
        assert response.json()["error"].lower() == "you have to login with proper credentials", \
            "Ответ на запрос не соответствует ожидаемому результату"
