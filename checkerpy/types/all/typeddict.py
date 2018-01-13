from .all import All
from ..one import JustDict
from ...functional import CompositionOf
from ...functional.mixins import CompositionClassMixin
from ...validators.one import JustLen


class Registrar(type):
    """Sets composition of class and JustLen validator as attribute."""
    def __init__(cls, class_name: str, bases, attributes: dict) -> None:
        super().__init__(class_name, (), attributes)
        setattr(cls, 'JustLen', CompositionOf(cls, JustLen))


class TypedDict(CompositionClassMixin, metaclass=Registrar):
    def __new__(cls, mapping: dict, name=None, keys=(), values=(), **kwargs):
        cls._name = str(name) if name is not None else ''
        mapping = JustDict(mapping)
        if keys:
            _ = All(keys)(mapping, name=name)
        if values:
            _ = All(values)(mapping.values(), name=name)
        return mapping
