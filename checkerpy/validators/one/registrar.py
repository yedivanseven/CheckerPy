from typing import Tuple
from ...types.one import _ITERABLES
from ...functional import CompositionOf

Types = Tuple[type, ...]


class IterableRegistrar(type):
    """Sets compositions of class and iterable type checkers as attributes."""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, (), attributes)
        for iterable in _ITERABLES:
            setattr(cls, iterable.__name__, CompositionOf(cls, iterable))
