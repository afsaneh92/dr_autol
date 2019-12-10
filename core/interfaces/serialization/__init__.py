import json
from abc import ABCMeta, abstractmethod


class Serializable:
    __metaclass__ = ABCMeta

    def serialize(self):
        return json.dumps(self)

    @abstractmethod
    def deserialize(self):
        pass

    @staticmethod
    def convert_input_to_dict(obj):
        return json.loads(obj)
