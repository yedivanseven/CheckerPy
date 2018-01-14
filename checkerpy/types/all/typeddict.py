import logging as log
from ..one import JustDict, Just
from ...functional import CompositionOf
from ...functional.mixins import CompositionClassMixin
from ...validators.one import JustLen
from ...exceptions import WrongTypeError


class Registrar(type):
    """Sets composition of class and JustLen validator as attribute."""
    def __init__(cls, class_name: str, bases, attributes: dict) -> None:
        super().__init__(class_name, (), attributes)
        setattr(cls, 'JustLen', CompositionOf(cls, JustLen))


class TypedDict(CompositionClassMixin, metaclass=Registrar):
    def __new__(cls, mapping: dict, name=None, keys=(), values=(), **kwargs):
        cls._name = str(name) if name is not None else ''
        mapping = JustDict(mapping, name=name)
        if keys and keys is not ...:
            for key in mapping.keys():
                try:
                    _ = Just(keys)(key, name=f'dictionary key')
                except WrongTypeError as error:
                    message = cls.__element_of_wrong_type_message()
                    log.error(message)
                    raise WrongTypeError(message) from error
        if values and values is not ...:
            for key, value in mapping.items():
                try:
                    _ = Just(values)(value, name=f'dictionary entry {key}')
                except WrongTypeError as error:
                    message = cls.__element_of_wrong_type_message()
                    log.error(message)
                    raise WrongTypeError(message) from error
        return mapping

    @classmethod
    def __element_of_wrong_type_message(cls) -> str:
        name = ' '+cls._name if cls._name else ''
        return f'An element of the dictionary{name} has a wrong type!'
