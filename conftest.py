import pytest
from requests.auth import HTTPBasicAuth

from settings import Config


@pytest.fixture(scope='session')
def basic_auth():
    config = Config()
    return HTTPBasicAuth(config.username, config.password)
