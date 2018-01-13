import logging as log
from typing import Tuple, List, Union
from ..one import Just
from ...validators.one import JustLen
from ...exceptions import LenError, WrongTypeError
from ...functional.mixins import CompositionClassMixin

TYPES = Union[Tuple[type, ...], List[type]]


class TypedTuple(CompositionClassMixin):
    def __new__(cls, value: tuple, name=None, types=(), **kwargs) -> tuple:
        cls._name = str(name) if name is not None else ''
        types, length = cls.__length_of(types)
        value = JustLen.JustTuple(value, name=name, length=length)
        for index, element in enumerate(value):
            try:
                _ = Just(types[index])(element)
            except WrongTypeError as error:
                message = cls.__element_of_wrong_type_message()
                log.error(message)
                raise WrongTypeError(message) from error
        return value

    @classmethod
    def __length_of(cls, types: TYPES) -> Tuple[TYPES, int]:
        if type(types) not in (tuple, list):
            message = cls.__has_no_length_message_for(types)
            raise LenError(message)
        return types, len(types)

    @staticmethod
    def __has_no_length_message_for(types) -> str:
        type_name = type(types).__name__
        return (f'Length of types argument {types} with '
                f'type {type_name} cannot be determined!')

    @classmethod
    def __element_of_wrong_type_message(cls) -> str:
        name = ' '+cls._name if cls._name else ''
        return f'An element of the tuple{name} has a wrong type!'
