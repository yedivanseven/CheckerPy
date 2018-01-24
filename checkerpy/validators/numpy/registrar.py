from typing import Tuple
from ...functional import CompositionOf
from ...types.numpy import _NUMPY_TYPES

Types = Tuple[type, ...]


class Registrar(type):
    """Sets composition of class and ndarray type checker as attribute."""
    def __init__(cls, class_name: str, bases: Types, attributes: dict) -> None:
        super().__init__(class_name, (), attributes)
        for np_type in _NUMPY_TYPES:
            setattr(cls, np_type.__name__, CompositionOf(cls, np_type))
