# ivi-test-framework

## Описание проекта
Решение тестового задания для компании IVI. В рамках решения реализован простой 
framework с автотестами. 

Файл `Test cases` содержит описание всех тест-кейсов. 
Файл `Bugs` содержит описания обнаруженных ошибок.

## Структура проекта
```
|--api - содержит классы оберток поверх api методов
    |--wrapper_one.py - класс обертка в котором описываются методы одного эндпоинта
    |--wrapper_two.py
|--test - содержит наборы тестов
    |--test_one.py - модуль с тестовыми сценариями
    |--test_two.py
|--utils - содержит вспомогательный код для тестов
|--settings.py - конфигурационные данные проекта
|--conftest.py - описание фикстур для тестов
|--.flake8 - конфигурация линтера 
|--requirements.txt - зависимости проекта

|--Test cases - список тестовых сценариев
|--Bugs - описание обнаруженных багов
```

## Локальный запуск проекта
#### Клонируем проект:
`git clone https://github.com/i-cod/ivi-test-framework.git`


#### Настраиваем виртуальное окружение:
```
cd ivi-test-framework/
pip3 install virtualenv
virtualenv venv/
source venv/bin/activate
```

#### Задаем логин и пароль
Перейти в файл `settings.py` и прописать данные вместо пустых кавычек:
```
self.username = os.environ.get("IVI_TEST_USER", "")
self.password = os.environ.get("IVI_TEST_PASSWORD", "")
```
Либо задать через переменные окружения

#### Ставим зависимости и запускаем тесты
```
pip install -r requirements.txt
pytest -v
```

## Запуск в Docker контейнере
Данный метод - альтернатива локальному запуску проекта
#### Собираем образ
```
cd ivi-test-framework/
docker build -f ./Dockerfile -t ivi_test .
```
#### Запускаем контейнер
`docker run --env IVI_TEST_USER=<username> --env IVI_TEST_PASSWORD=<password> ivi_test`
    