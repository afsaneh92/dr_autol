from abc import ABCMeta, abstractmethod


class Validatable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate_pattern(self):
        pass

