import logging as log
from .registrars import AllComparableRegistrar
from ..one import Limited
from ...functional.mixins import CompositionClassMixin
from ...exceptions import IterError


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
    For convenience, type checkers for built-in comparables (i.e., everything
    but dict) and iterables as well as an emptiness checker for `iterable`
    are attached as methods. If `alo` and/or `ahi` is specified in calls
    to these methods, it (or they) are passed through to the limits checker.

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
        cls._iter_type = type(iterable).__name__
        if not hasattr(iterable, '__iter__'):
            message = cls._not_an_iterable_message_for()
            log.error(message)
            raise IterError(message)
        for index, value in enumerate(iterable):
            value_name = cls.__name_from(index)
            _ = Limited(value, name=value_name, lo=alo, hi=ahi)
        return iterable

    @classmethod
    def __name_from(cls, index: int) -> str:
        if cls._iter_type == 'dict':
            return f'dict key in {cls._string}'
        elif cls._iter_type == 'dict_keys':
            return f'key in dict {cls._string}' if cls._name else cls._string
        elif cls._iter_type == 'dict_values':
            s = f'dict value in {cls._string}' if cls._name else cls._string
            return s
        elif cls._iter_type in ('set', 'frozenset'):
            return f'element in {cls._iter_type} {cls._string}'
        return f'{cls._iter_type} {cls._string} at index {index}'
