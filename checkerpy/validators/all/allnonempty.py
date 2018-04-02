from ...functional.mixins import CompositionClassMixin
from ..one import NonEmpty
from .registrars import AllIterableRegistrar


class AllNonEmpty(CompositionClassMixin, metaclass=AllIterableRegistrar):
    """Checks if any of the elements of an iterable is an empty iterable.

    Parameters
    ----------
    iterable
        The iterable to check empty elements of.
    name : str, optional
        The name of the variable to check empty elements of. Defaults to None.

    Returns
    -------
    iterable
        The `iterable` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the emptiness checker to another `callable`, returning
        the functional composition of both.

    Notes
    -----
    For convenience, type checkers for built-in iterables and an emptiness
    checker for `iterable` are attached as methods as well.


    Raises
    ------
    IterError
        If the variable passed to the emptiness checker is not an iterable.
    EmptyError
        If the emptiness of any of the elements of `iterable` cannot be
        determined or if any of the elements of `iterable` are empty.

    See Also
    --------
    NonEmpty, CompositionOf

    """

    def __new__(cls, iterable, name: str = None, **kwargs):
        cls.__name = str(name) if name is not None else ''
        cls._string = cls.__name or str(iterable)
        cls._itertype = type(iterable).__name__
        for index, value in cls._enumerate(iterable):
            _ = NonEmpty(value, name=cls.__name_from(index))
        return iterable

    @classmethod
    def __name_from(cls, index: int) -> str:
        dicts = f'dict {cls._string}' if cls.__name else cls._string
        named = f'{cls._itertype} {cls.__name}' if cls.__name else cls._string
        if cls._itertype == 'dict':
            return f'key in dict {cls._string}'
        if cls._itertype in ('dict_keys', 'odict_keys'):
            return f'key in {dicts}'
        elif cls._itertype in ('dict_values', 'odict_values'):
            return f'value in {dicts}'
        elif cls._itertype in ('OrderedDict', 'defaultdict'):
            return f'key in {named}'
        elif cls._itertype == 'frozenset':
            return f'{cls.__string_for(index)}in {named}'
        elif cls._itertype == 'deque':
            return f'{cls.__string_for(index)}in {named}'
        return f'{cls.__string_for(index)}in {cls._itertype} {cls._string}'

    @staticmethod
    def __string_for(index: int) -> str:
        return f'with index {index} ' if index >= 0 else ''
