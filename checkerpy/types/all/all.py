import logging as log
from typing import Union, Tuple, Iterable
from .docstring import DOC_HEADER, DOC_BODY
from ..one import _ITERABLES, Just
from ...validators.one import NonEmpty, JustLen
from ...functional import CompositionOf
from ...functional.mixins import CompositionMixin
from ...exceptions import IterError

Types = Union[type, Iterable[type]]


class All(CompositionMixin):
    """Class for easily defining type-checkers for all elements of an iterable.

    Parameters
    ----------
    types : *type
        One or more type(s) to check for.
    identifier : str, optional
        A valid python identifier as name of the type checker object.
        Defaults to 'All'.

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

    See Also
    --------
    Just

    """

    def __init__(self, *types: Types, identifier: str = 'All') -> None:
        self.__just = Just(*types)
        self.__types = self.__just.types
        self.__doc__ = self.__doc_string()
        self.__name__ = self.__identified(identifier)
        for iterable in _ITERABLES:
            setattr(self, iterable.__name__, CompositionOf(self, iterable))
        setattr(self, 'NonEmpty', CompositionOf(self, NonEmpty))
        setattr(self, 'JustLen', CompositionOf(self, JustLen))

    @property
    def types(self) -> Tuple[type, ...]:
        return self.__types

    def __call__(self, iterable: Iterable, name=None, **kwargs) -> Iterable:
        self._name = str(name) if name is not None else ''
        self.__string = self._name or str(iterable)
        self.__iter_type = type(iterable).__name__
        if not hasattr(iterable, '__iter__'):
            message = self.__not_an_iterable_message()
            log.error(message)
            raise IterError(message)
        for index, value in enumerate(iterable):
            _ = self.__just(value, name=self.__name_from(index))
        return iterable

    def __not_an_iterable_message(self) -> str:
        return (f'Variable {self.__string} with type {self.__iter_type} does'
                ' not seem to be an iterable with elements to inspect!')

    def __name_from(self, index: int) -> str:
        if self.__iter_type == 'dict':
            return f'key in dict {self.__string}'
        elif self.__iter_type == 'dict_keys':
            string = f'dict {self.__string}' if self._name else self.__string
            return f'key in ' + string
        elif self.__iter_type == 'dict_values':
            string = f'dict {self.__string}' if self._name else self.__string
            return f'value in ' + string
        elif self.__iter_type == 'frozenset':
            s = f'frozenset {self.__string}' if self._name else self.__string
            return f'element in ' + s
        elif self.__iter_type in 'set':
            return f'element in set {self.__string}'
        return f'element {index} in {self.__iter_type} {self.__string}'

    @staticmethod
    def __identified(identifier: str) -> str:
        identifier = str(identifier)
        if not identifier.isidentifier():
            raise ValueError(f'Type-checker name {identifier}'
                             f' is not a valid identifier!')
        return identifier

    def __doc_string(self) -> str:
        types = tuple(type_.__name__ for type_ in self.__types)
        types_string = types[0] if len(types) == 1 else f'one of {types}'
        doc_string = DOC_HEADER.format(types_string)
        doc_string += DOC_BODY
        return doc_string
