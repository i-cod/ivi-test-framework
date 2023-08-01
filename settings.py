import os
from dataclasses import dataclass


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
@dataclass
class Config:
    username: str
    password: str

    def __init__(self):
        self.username = os.environ.get("IVI_TEST_LOGIN")
        self.password = os.environ.get("IVI_TEST_PASSWORD")
