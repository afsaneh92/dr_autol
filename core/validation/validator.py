from abc import ABCMeta, abstractmethod
import re

from core.messages import fail_keys
from core.messages import json_keys


class Validator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate_schema(self, obj, format_type):
        pass

    @abstractmethod
    def validate_pattern(self, field):
        pass
