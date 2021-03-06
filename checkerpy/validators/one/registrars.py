from typing import Tuple
from collections import defaultdict, deque, OrderedDict
from ...types.one import JustStr, _ITERABLES
from ...types.weak import LikeSized, LikeContainer, _LIKE_ITERABLES
from ...functional import CompositionOf

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

Types = Tuple[type, ...]


class IterableRegistrar(type):
    """Sets compositions of class and iterable type checkers as attributes."""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, bases, attributes)
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
        setattr(cls, 'LikeContainer', CompositionOf(cls, LikeContainer))


class StrRegistrar(type):
    """Sets composition of class and JustStr as attribute."""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, bases, attributes)
        setattr(cls, 'JustStr', CompositionOf(cls, JustStr))
