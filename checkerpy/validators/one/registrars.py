from typing import Tuple
from ...types.one import JustStr, _ITERABLES
from ...types.weak import LikeSized, _LIKE_ITERABLES, _LIKE_CONTAINERS
from ...functional import CompositionOf

Types = Tuple[type, ...]


class IterableRegistrar(type):
    """Sets compositions of class and iterable type checkers as attributes."""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, (), attributes)
        for iterable in _ITERABLES:
            setattr(cls, iterable.__name__, CompositionOf(cls, iterable))
        for iterable in _LIKE_ITERABLES:
            setattr(cls, iterable.__name__, CompositionOf(cls, iterable))


class SizedRegistrar(IterableRegistrar):
    """Sets composition of class and LikeSized checker as attribute"""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, bases, attributes)
        setattr(cls, 'LikeSized', CompositionOf(cls, LikeSized))


class ContainerRegistrar(IterableRegistrar):
    """Sets compositions of class and container-like checkers as attributes"""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, bases, attributes)
        for container in _LIKE_CONTAINERS:
            setattr(cls, container.__name__, CompositionOf(cls, container))


class StrRegistrar(type):
    """Sets composition of class and JustStr as attribute."""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, (), attributes)
        setattr(cls, 'JustStr', CompositionOf(cls, JustStr))
