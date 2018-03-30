from typing import Any
from ...functional.mixins import CompositionClassMixin
from ..one import JustLen
from .registrars import AllIterableRegistrar


class AllLen(CompositionClassMixin, metaclass=AllIterableRegistrar):
    """Checks if all elements of an iterable have one of the specified lengths.

    Parameters
    ----------
    iterable
        The iterable for which to check the length of its elements.
    name : str, optional
        The name of the variable to check the length of the elements of.
        Defaults to None.
    alen : int, tuple(int)
        One or more lengths that all elements of `iterable` should have.

    Returns
    -------
    iterable
        The `iterable` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the length checker to another `callable`, returning the
        functional composition of both. If the optional argument `alen` is
        specified when calling the composition, it is passed through to the
        length checker.

    Notes
    -----
    For convenience, type checkers for built-in iterables (str, tuple, list,
    set, and dict) and an emptiness checker for `iterable` are attached as
    methods as well. If the optional argument `alen` is specified in calls
    to these methods, it is passed through to the length checker.

    Raises
    ------
    IntError
        If the specified length(s) cannot be converted to required type int.
    IterError
        If the variable passed to the length checker is not an iterable.
    LenError
        If the length of any element of `iterable` can either not be determined
        or is not among the allowed lengths.

    See Also
    --------
    JustLen, CompositionOf

    """

    def __new__(cls, iterable, name: str = None, *, alen: int, **kwargs):
        cls.__name = str(name) if name is not None else ''
        cls._string = cls.__name or str(iterable)
        cls._itertype = type(iterable).__name__
        for index, value in cls._enumerate(iterable):
            value_name = cls.__name_from(index, value)
            _ = JustLen(value, name=value_name, length=alen)
        return iterable

    @classmethod
    def __name_from(cls, index: int, value: Any) -> str:
        dicts = f'dict {cls._string}' if cls.__name else cls._string
        named = f'{cls._itertype} {cls.__name}' if cls.__name else cls._string
        if cls._itertype == 'dict':
            return f'key {value} in dict {cls._string}'
        elif cls._itertype in ('dict_keys', 'odict_keys'):
            return f'key {value} in {dicts}'
        elif cls._itertype in ('dict_values', 'odict_values'):
            return f'value {value} in {dicts}'
        elif cls._itertype in ('dict_items', 'odict_items'):
            return f'item {value} in {dicts}'
        elif cls._itertype in ('OrderedDict', 'defaultdict'):
            return f'key {value} in {named}'
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
