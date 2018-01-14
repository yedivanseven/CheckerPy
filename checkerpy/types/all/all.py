import logging as log
from typing import Union, Tuple, Iterable
from .docstring import DOC_HEADER, DOC_BODY
from ..one import _ITERABLES, Just
from ...validators.one import NonEmpty
from ...functional import CompositionOf
from ...functional.mixins import CompositionMixin
from ...exceptions import WrongTypeError, IterError

TYPES = Union[type, Iterable[type]]


class All(CompositionMixin):
    """Class for easily defining type-checkers for all elements of an iterable.

    Examples
    --------
    A new type checker for all elements of an iterable can be defined like so:

    >>> AllNum = All(int, float)

    Custom types are also possible:

    >>> class MyType:
    ...     pass
    ...
    >>> AllMyType = All(MyType)

    It is highly recommended to also pass the optional keyword `identifier`,
    which should be a valid python identifier for the name of the type checker.

    >>> AllInt = All(int, identifier='AllInt')

    Raises
    ------
    AttributeError
        If no types to check for are found when instantiating the
        type-checker object.
    TypeError
        If the types to check for specified when instantiating the
        type-checker object contain one or more entries that are not of
        type ``type`` themselves.

    See Also
    --------
    Just

    """

    def __init__(self, *types: TYPES, identifier: str = 'All') -> None:
        self.__just = Just(*types)
        self.__types = self.__just.types
        self.__doc__ = self.__doc_string()
        self.__name__ = self.__identified(identifier)
        for iterable in _ITERABLES:
            setattr(self, iterable.__name__, CompositionOf(self, iterable))
        setattr(self, 'NonEmpty', CompositionOf(self, NonEmpty))

    @property
    def types(self) -> Tuple[type, ...]:
        return self.__types

    def __call__(self, iterable: Iterable, name=None, **kwargs) -> Iterable:
        self._name = str(name) if name is not None else ''
        self.__string = ' ' + (self._name or str(iterable))
        if not hasattr(iterable, '__iter__'):
            message = self.__not_an_iterable_message_for(iterable)
            log.error(message)
            raise IterError(message)
        try:
            _ = tuple(map(self.__just, iterable))
        except WrongTypeError as error:
            message = self.__element_of_wrong_type_message_for(iterable)
            log.error(message)
            raise WrongTypeError(message) from error
        return iterable

    def __not_an_iterable_message_for(self, value) -> str:
        type_name = type(value).__name__
        return (f'Variable{self.__string} with type {type_name} does '
                'not seem to be an iterable with elements to inspect!')

    def __element_of_wrong_type_message_for(self, iterable: Iterable) -> str:
        type_name = type(iterable).__name__
        return f'An element of the {type_name}{self.__string} has wrong type!'

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
