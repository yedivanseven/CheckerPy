import logging as log
from typing import Tuple, Union, Iterable, Any
from .docstring import DOC_HEADER, DOC_BODY
from ...functional.mixins import CompositionMixin
from ...exceptions import WrongTypeError

Types = Union[type, Iterable[type]]


class Just(CompositionMixin):
    """Class for easily and concisely defining type-checker objects.

    Parameters
    ----------
    types : *type
        One or more type(s) to check for.
    identifier : str, optional
        A valid python identifier as name of the type checker object.
        Defaults to 'Just'.

    Raises
    ------
    AttributeError
        If no `types` to check for are found when instantiating the
        type-checker object.
    TypeError
        If the `types` to check for specified when instantiating the
        type-checker object contain one or more entries that are not of
        type ``type`` themselves.
    ValueError
        If the (optional) `identifier` is not a valid python identifier.

    """

    def __init__(self, *types: Types, identifier: str = 'Just') -> None:
        self._name = None
        self.__types = self.__registered(types)
        self.__doc__ = self.__doc_string()
        self.__name__ = self.__identified(identifier)

    @property
    def types(self) -> Tuple[type, ...]:
        return self.__types

    def __call__(self, value: Any, name: str = None, **kwargs):
        value_type = type(value)
        self._name = str(name) if name is not None else ''
        if value_type not in self.__types:
            message = self.__error_message_for(value, value_type.__name__)
            log.error(message)
            raise WrongTypeError(message)
        return value

    def __error_message_for(self, value: Any, value_type: str) -> str:
        name = ' of '+self._name if self._name else ''
        types = tuple(type_.__name__ for type_ in self.__types)
        of_type = types[0] if len(types) == 1 else f'one of {types}'
        return f'Type{name} must be {of_type}, not {value_type} like {value}!'

    @staticmethod
    def __identified(identifier: str) -> str:
        identifier = str(identifier)
        if not identifier.isidentifier():
            raise ValueError(f'Type-checker name {identifier}'
                             f' is not a valid identifier!')
        return identifier

    def __registered(self, types: Tuple[type, ...]) -> Tuple[type, ...]:
        if not types:
            raise AttributeError('Found no types to check for!')
        type_is_iter = len(types) == 1 and type(types[0]) in (tuple, list, set)
        types = types[0] if type_is_iter else types
        return tuple(map(self.__validate, types))

    def __validate(self, type_: type) -> type:
        if not type(type_) is type:
            message = self.__invalid_type_message_for(type_)
            raise TypeError(message)
        return type_

    @staticmethod
    def __invalid_type_message_for(type_: Any) -> str:
        name = type_.__name__ if hasattr(type_, '__name__') else type_
        type_name = type(type_).__name__
        return f'Type of type specifier {name} must be type, not {type_name}!'

    def __doc_string(self) -> str:
        types = tuple(type_.__name__ for type_ in self.__types)
        types_string = types[0] if len(types) == 1 else f'one of {types}'
        doc_string = DOC_HEADER.format(types_string)
        doc_string += DOC_BODY
        return doc_string
