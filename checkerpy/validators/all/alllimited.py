from ...functional.mixins import CompositionClassMixin
from ..one import Limited
from .registrars import AllComparableRegistrar


class AllLimited(CompositionClassMixin, metaclass=AllComparableRegistrar):
    """Checks if all elements of an iterable lie outside given limits.

    Parameters
    ----------
    iterable
        The iterable for which to check if its elements lie outside limits.
    name : str, optional
        The name of the variable to check the elements of. Defaults to None.
    alo : optional
        Lower bound for all elements of `iterable`. Defaults to Ellipsis.
    ahi : optional
        Upper bound for all elements of `iterable`. Defaults to Ellipsis.

    Returns
    -------
    iterable
        The `iterable` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the limits checker to another `callable`, returning the
        functional composition of both. If `alo` and/or `ahi` is
        specified when calling the composition, it (or they) are passed
        through to the limits checker.

    Notes
    -----
    For convenience, type checkers for built-in comparables and iterables as
    well as an emptiness checker for `iterable` are attached as methods. If
    `alo` and/or `ahi` is specified in calls to these methods, it (or they)
    are passed through to the limits checker.

    Raises
    ------
    IterError
        If the variable passed to the length checker is not an iterable.
    WrongTypeError
        If any element of `iterable` cannot be compared to the given limit(s).
    LimitError
        If any of the elements of `iterable` lie on the wrong side or outside
        the respective limit(s).

    See Also
    --------
    Limited, CompositionOf

    """

    def __new__(cls, iterable, name=None, *, alo=..., ahi=..., **kwargs):
        cls._name = str(name) if name is not None else ''
        cls._string = cls._name or str(iterable)
        cls._itertype = type(iterable).__name__
        for index, value in cls._enumerate(iterable):
            value_name = cls.__name_from(index)
            _ = Limited(value, name=value_name, lo=alo, hi=ahi)
        return iterable

    @classmethod
    def __name_from(cls, index: int) -> str:
        named = f'{cls._itertype} {cls._name}' if cls._name else cls._string
        if cls._itertype == 'dict':
            return f'key in dict {cls._string}'
        elif cls._itertype in ('dict_keys', 'odict_keys'):
            return f'key in dict {cls._string}' if cls._name else cls._string
        elif cls._itertype in ('dict_values', 'odict_values'):
            return f'dict value in {cls._string}' if cls._name else cls._string
        elif cls._itertype in ('dict_items', 'odict_items'):
            return f'item in dict {cls._string}' if cls._name else cls._string
        elif cls._itertype in ('OrderedDict', 'defaultdict'):
            return f'key in {named}'
        elif cls._itertype == 'frozenset':
            return f'element in {named}'
        elif cls._itertype == 'deque':
            return f'{named} at index {index}'
        prefix, postfix = cls.__fixes_for(index)
        return f'{prefix}{cls._itertype} {cls._string}{postfix}'

    @staticmethod
    def __fixes_for(index: int) -> (str, str):
        prefix = '' if index >= 0 else 'element in '
        postfix = f' at index {index}' if index >= 0 else ''
        return prefix, postfix
