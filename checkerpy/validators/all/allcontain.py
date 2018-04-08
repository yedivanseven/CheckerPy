from ...functional.mixins import CompositionClassMixin
from ..one import Contains
from .registrars import AllIterableRegistrar, DICT_PARTS


class AllContain(CompositionClassMixin, metaclass=AllIterableRegistrar):
    """

    """

    def __new__(cls, iterable, name=None, *, each=(), asome=(), **kwargs):
        cls.__name = str(name) if name is not None else ''
        cls._string = cls.__name or str(iterable)
        cls._itertype = type(iterable).__name__
        for index, value in cls._enumerate(iterable):
            value_name = cls.__name_from(index)
            _ = Contains(value, name=value_name, every=each, some=asome)
        return iterable

    @classmethod
    def __name_from(cls, index: int) -> str:
        named = f'{cls._itertype} {cls.__name}' if cls.__name else cls._string
        if cls._itertype == 'dict':
            return f'in keys to dict {cls._string}'
        elif cls._itertype in DICT_PARTS+('frozenset',):
            return f'in {named}'
        elif cls._itertype in ('OrderedDict', 'defaultdict'):
            return f'in keys to {named}'
        elif cls._itertype == 'deque':
            return f'{cls.__string_for(index)} in {named}'
        return f'{cls.__string_for(index)} in {cls._itertype} {cls._string}'

    @staticmethod
    def __string_for(index: int) -> str:
        return f' with index {index}' if index >= 0 else ''
