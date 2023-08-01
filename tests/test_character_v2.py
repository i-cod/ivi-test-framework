import http

from api.character_v2 import CharacterV2
from utils.data_generator import get_random_str


class TestCharacterV2:

    def test_create_new_character(self, basic_auth):
        """
        Описание:
            Создание и удаление нового персонажа

        Сценарий:
            1) Выполнить метод POST /v2/character с валидными данными
            2) Проверить методом GET /v2/character что запись появилась
            3) Выполнить метод DELETE /v2/character для созданного персонажа
            4) Проверить методом GET /v2/character что запись удалена

        Ожидаемый результат:
            На каждом шаге возвращается ожидаемый статус-код и тело ответа
        """
        request = {
            "education": "High school (unfinished)",
            "height": 1.9,
            "identity": "Publicly known",
            "name": get_random_str(15),
            "universe": "Marvel Universe",
            "weight": 104
        }
        character = CharacterV2()
        create_response = character.create(json=request, auth=basic_auth, status_code=http.HTTPStatus.OK).json()
        assert create_response["result"]["name"] == request["name"]

        get_response = character.get_by_name(params={"name": request["name"]}, auth=basic_auth,
                                             status_code=http.HTTPStatus.OK).json()
        assert get_response["result"]["name"] == request["name"]

        delete_response = character.delete(params={"name": request["name"]}, auth=basic_auth,
                                           status_code=http.HTTPStatus.OK).json()
        assert delete_response["result"].lower() == f"Hero {request['name']} is deleted".lower()

        character.get_by_name(params={"name": request["name"]}, auth=basic_auth,
                              status_code=http.HTTPStatus.BAD_REQUEST)

    def test_update_character(self, basic_auth):
        """
        Описание:
            Изменение информации о персонаже

        Сценарий:
            1) Выполнить метод создания POST /v2/character с валидными данными
            2) Изменить ключевые поля в запросе и выполнить PUT /v2/character

        Ожидаемый результат:
            Вернулся статус-код 200, ответ содержит обновленную структуру запроса
        """
        request = {
            "education": "High school (unfinished)",
            "height": 1.9,
            "identity": "Publicly known",
            "name": get_random_str(15),
            "universe": "Marvel Universe",
            "weight": 104
        }
        character = CharacterV2()
        character.create(json=request, auth=basic_auth, status_code=http.HTTPStatus.OK)

        request["weight"] = 99
        response = character.update(json=request, auth=basic_auth, status_code=http.HTTPStatus.OK).json()
        assert response["result"]["weight"] == request["weight"]

        character.delete(params={"name": request["name"]}, auth=basic_auth, status_code=http.HTTPStatus.OK)

    def test_create_character_twice(self, basic_auth):
        """
        Описание:
            Создание одного персонажа несколько раз

        Сценарий:
            Дважды выполнить метод POST /v2/character с одинаковыми валидными данными

        Ожидаемый результат:
            Повторное выполнение метода приводит к статус-коду 400, ответ содержит сообщение о том,
            что персонаж уже существует
        """
        request = {
            "education": "High school (unfinished)",
            "height": 1.9,
            "identity": "Publicly known",
            "name": get_random_str(15),
            "universe": "Marvel Universe",
            "weight": 104
        }
        character = CharacterV2()
        create_response = character.create(json=request, auth=basic_auth, status_code=http.HTTPStatus.OK).json()
        assert create_response["result"]["name"] == request["name"]

        response = character.create(json=request, auth=basic_auth, status_code=http.HTTPStatus.BAD_REQUEST).json()
        assert response["error"].lower() == f"{request['name']} is already exists".lower()

        character.delete(params={"name": request["name"]}, auth=basic_auth, status_code=http.HTTPStatus.OK)

    def test_try_to_get_nonexistent_character(self, basic_auth):
        """
        Описание:
            Запрос информации о несуществующем персонаже

        Сценарий:
            Выполнить метод GET /v2/character передав в качестве параметра случайно сгенерированную строку

        Ожидаемый результат:
            Вернулся статус-код 400, ответ содержит информацию о том, что имя не существует
        """
        response = CharacterV2().get_by_name(params={"name": get_random_str(20)}, auth=basic_auth,
                                             status_code=http.HTTPStatus.BAD_REQUEST).json()
        assert response["error"].lower() == "no such name"

    def test_try_to_delete_nonexistent_character(self, basic_auth):
        """
        Описание:
            Удаление несуществующего персонажа

        Сценарий:
            Выполнить метод DELETE /v2/character передав в качестве параметра случайно сгенерированную строку

        Ожидаемый результат:
            Вернулся статус-код 400, ответ содержит информацию о том, что имя не существует
        """
        response = CharacterV2().delete(params={"name": get_random_str(20)}, auth=basic_auth,
                                        status_code=http.HTTPStatus.BAD_REQUEST).json()
        assert response["error"].lower() == "no such name"

    def test_create_character_with_empty_name(self, basic_auth):
        """
        Описание:
            Создание персонажа c пустым именем

        Сценарий:
            Выполнить метод POST /v2/character с пустым полем name

        Ожидаемый результат:
            Вернулся статус-код 400, ответ содержит информацию о том, что имя не должно быть пустым
        """
        request = {
            "education": "High school (unfinished)",
            "height": 1.9,
            "identity": "Publicly known",
            "name": "",
            "universe": "Marvel Universe",
            "weight": 104
        }
        response = CharacterV2().create(json=request, auth=basic_auth, status_code=http.HTTPStatus.BAD_REQUEST).json()
        assert response['error'].lower() == "name: ['length must be between 1 and 350.']"

    def test_create_without_required_fields(self, basic_auth):
        """
        Описание:
            Создание персонажа без обязательных полей

        Сценарий:
            Выполнить метод POST /v2/character без поля name в запросе

        Ожидаемый результат:
            Вернулся статус-код 400, ответ содержит информацию о том, что пропущены обязательные данные
        """
        request = {
            "education": "High school (unfinished)",
            "height": 1.9,
            "identity": "Publicly known",
            "universe": "Marvel Universe",
            "weight": 104
        }
        response = CharacterV2().create(json=request, auth=basic_auth, status_code=http.HTTPStatus.BAD_REQUEST).json()
        assert response['error'].lower() == "name: ['missing data for required field.']"
