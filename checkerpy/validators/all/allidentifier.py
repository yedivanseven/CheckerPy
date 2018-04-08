from typing import Any
from ...functional.mixins import CompositionClassMixin
from ..one import Identifier
from .registrars import IterableRegistrar, DICT_PARTS


class AllIdentifier(CompositionClassMixin, metaclass=IterableRegistrar):
    """

    """

    def __new__(cls, iterable, name: str = None, *, attrs='__new__', **kwargs):
        cls.__name = str(name) if name is not None else ''
        cls._string = cls.__name or str(iterable)
        cls._itertype = type(iterable).__name__
        for index, value in cls._enumerate(iterable):
            value_name = cls.__name_from(index, value)
            _ = Identifier(value, name=value_name)
        return iterable

    @classmethod
    def __name_from(cls, index: int, value: Any) -> str:
        named = f'{cls._itertype} {cls.__name}' if cls.__name else cls._string
        if cls._itertype == 'dict':
            return f'{value} in keys to dict {cls._string}'
        elif cls._itertype in DICT_PARTS:
            return f'{value} in {named}'
        elif cls._itertype in ('OrderedDict', 'defaultdict'):
            return f'{value} in keys to {named}'
        elif cls._itertype == 'frozenset':
            value = set(value) if type(value) is frozenset else value
            return f'{value} in {named}'
        elif cls._itertype == 'deque':
            return f'{value}{cls.__string_for(index)} in {named}'
        return (f'{value}{cls.__string_for(index)} '
                f'in {cls._itertype} {cls._string}')

    @staticmethod
    def __string_for(index: int) -> str:
        return f' with index {index}' if index >= 0 else ''
