from typing import Tuple
from ...types.one import _ITERABLES
from ...types.all import _ALL_ITERABLES
from ..one import NonEmpty
from ...functional import CompositionOf

TYPES = Tuple[type, ...]


class IterableRegistrar(type):
    """Sets compositions of class and iterable type checkers as attributes."""
    def __init__(cls, class_name: str, bases: TYPES, attributes: dict) -> None:
        super().__init__(class_name, (), attributes)
        for iterable in _ITERABLES:
            setattr(cls, iterable.__name__, CompositionOf(cls, iterable))
        setattr(cls, 'NonEmpty', CompositionOf(cls, NonEmpty))


class AllIterableRegistrar(IterableRegistrar):
    """Sets compositions of class and all-iterable type checkers as attr's."""
    def __init__(cls, class_name: str, bases: TYPES, attributes: dict) -> None:
        super().__init__(class_name, bases, attributes)
        for iterable in _ALL_ITERABLES:
            setattr(cls, iterable.__name__, CompositionOf(cls, iterable))
