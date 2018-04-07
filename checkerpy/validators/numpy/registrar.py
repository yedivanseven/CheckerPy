from typing import Tuple
from collections import defaultdict, deque, OrderedDict
from ...functional import CompositionOf
from ...types.numpy import _NUMPY_TYPES

dict_keys = type({}.keys())
odict_keys = type(OrderedDict({}).keys())
dict_values = type({}.values())
odict_values = type(OrderedDict({}).values())
dict_items = type({}.items())
odict_items = type(OrderedDict({}).items())
named_types = (frozenset, deque, defaultdict, OrderedDict,
               dict_keys, dict_values, dict_items,
               odict_keys, odict_values, odict_items)

Types = Tuple[type, ...]


class Registrar(type):
    """Sets composition of class and ndarray type checker as attribute."""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, bases, attributes)
        for np_type in _NUMPY_TYPES:
            setattr(cls, np_type.__name__, CompositionOf(cls, np_type))
