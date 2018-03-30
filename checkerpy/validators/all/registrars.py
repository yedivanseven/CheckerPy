import logging as log
from typing import Tuple, Any
from ...types.one import _ITERABLES
from ...types.all import _ALL_ITERABLES, _ALL_COMPARABLES
from ...functional import CompositionOf
from ...exceptions import IterError
from ..one import NonEmpty, JustLen

Types = Tuple[type, ...]
Enumerated = Tuple[Tuple[int, Any], ...]


class IterableRegistrar(type):
    """Sets compositions of class and iterable type checkers as attributes."""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, (), attributes)
        for iterable in _ITERABLES:
            setattr(cls, iterable.__name__, CompositionOf(cls, iterable))
        setattr(cls, 'NonEmpty', CompositionOf(cls, NonEmpty))
        setattr(cls, 'JustLen', CompositionOf(cls, JustLen))

    def _not_an_iterable_message(cls) -> str:
        return (f'Variable {cls._string} with type {cls._itertype} does'
                ' not seem to be an iterable with elements to inspect!')

    def _enumerate(cls, iterable: Any) -> Enumerated:
        try:
            if hasattr(iterable, 'index') and hasattr(iterable, 'count'):
                enumerated = tuple(enumerate(iterable))
            else:
                indices = (-1 for _ in range(len(iterable)))
                enumerated = tuple(zip(indices, iterable))
        except TypeError as error:
            message = cls._not_an_iterable_message()
            log.error(message)
            raise IterError(message) from error
        return enumerated


class AllIterableRegistrar(IterableRegistrar):
    """Sets compositions of class and all-iterable type checkers as attr's."""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, bases, attributes)
        for iterable in _ALL_ITERABLES:
            setattr(cls, iterable.__name__, CompositionOf(cls, iterable))


class AllComparableRegistrar(IterableRegistrar):
    """Set compositions of class and all-comparable type checkers as attr's."""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, (), attributes)
        for comparable in _ALL_COMPARABLES:
            setattr(cls, comparable.__name__, CompositionOf(cls, comparable))


class CustomRegistrar(type):
    """Set compositions of class and all-comparable type checkers as attr's."""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, bases, attributes)
        for comparable in _ALL_COMPARABLES:
            setattr(cls, comparable.__name__, CompositionOf(cls, comparable))
        delattr(cls, 'TypedDict')
