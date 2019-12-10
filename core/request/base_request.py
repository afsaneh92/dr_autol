from abc import ABCMeta

from core.interfaces.serialization import Serializable
from core.validation import Validatable


class RequestBaseClass(Validatable, Serializable):
    __metaclass__ = ABCMeta
