import logging as log
from typing import Tuple, Union, Sequence, Iterable, Any
from collections import defaultdict, deque, OrderedDict
from ...functional.mixins import CompositionMixin
from ...exceptions import WrongTypeError
from .docstring import DOC_HEADER, DOC_BODY

dict_keys = type({}.keys())
odict_keys = type(OrderedDict({}).keys())
dict_values = type({}.values())
odict_values = type(OrderedDict({}).values())
dict_items = type({}.items())
odict_items = type(OrderedDict({}).items())
NAMED_TYPES = (frozenset, slice, range,
               deque, defaultdict, OrderedDict,
               dict_keys, dict_values, dict_items,
               odict_keys, odict_values, odict_items)

TypesT = Union[type, Iterable[type]]


class Just(CompositionMixin):
    """Class for easily and concisely defining type-checker objects.

    Parameters
    ----------
    types : *type
        One or more type(s) to check for.
    identifier : str, optional
        A valid python identifier as name of the type-checker object.
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

    def __init__(self, *types: TypesT, identifier: str = 'Just') -> None:
        self.__name = None
        self.__types = self.__registered(types)
        self.__name__ = self.__identified(identifier)
        self.__doc__ = self.__doc_string()

    @property
    def types(self) -> Tuple[type, ...]:
        return self.__types

    def __call__(self, value: Any, name: str = None, **kwargs):
        self.__name = str(name) if name is not None else ''
        if type(value) not in self.__types:
            message = self.__error_message_for(value)
            log.error(message)
            raise WrongTypeError(message)
        return value

    def __error_message_for(self, value: Any) -> str:
        if isinstance(value, NAMED_TYPES):
            value_type = type(value).__name__
        else:
            value_type = type(value).__name__ + f' like {value}'
        name = ' of '+self.__name if self.__name else ''
        types = tuple(type_.__name__ for type_ in self.__types)
        of_type = types[0] if len(types) == 1 else f'one of {types}'
        return f'Type{name} must be {of_type}, not {value_type}!'

    @staticmethod
    def __identified(identifier: str) -> str:
        identifier = str(identifier)
        if not identifier.isidentifier():
            raise ValueError(f'Type-checker name {identifier}'
                             f' is not a valid identifier!')
        return identifier

    def __registered(self, types: Sequence[TypesT]) -> Tuple[type, ...]:
        if not types:
            raise AttributeError('Found no types to check for!')
        try:
            types = tuple(map(self.__validate, types[0]))
        except TypeError:
            types = tuple(map(self.__validate, types))
        return types

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
