from json import dumps
from abc import abstractclassmethod
from types import FunctionType, MethodType

from mainapp.models import Category


class BaseSerializer:
    def __init__(self, items):
        self.items = items
        self.data = {"items": []}

    def save(self):
        self.prepare_data()
        return dumps(self.data)

    @abstractclassmethod
    def prepare_data(self):
        pass


class CourseSerializer(BaseSerializer):
    def prepare_data(self):
        for item in self.items:
            chunk = {}
            for attr, value in item.__dict__.items():
                if attr.startswith("_") or isinstance(attr, (FunctionType, MethodType)):
                    continue
                if isinstance(value, Category):
                    value = value.id
                if isinstance(value, list):
                    value = [user.id for user in value]
                chunk[attr] = value
            self.data["items"].append(chunk)
