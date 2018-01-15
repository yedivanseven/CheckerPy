from ..one import JustDict, Just
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
        cls.__string = ' '+cls._name if cls._name else ''
        mapping = JustDict(mapping, name=name)
        if keys and keys is not ...:
            for key in mapping:
                _ = Just(keys)(key, name=f'key in dictionary{cls.__string}')
        if values and values is not ...:
            for key, value in mapping.items():
                value_name = f'entry "{key}" in dictionary{cls.__string}'
                _ = Just(values)(value, name=value_name)
        return mapping
