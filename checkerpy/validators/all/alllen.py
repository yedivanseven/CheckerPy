import logging as log
from typing import Any
from .registrars import AllIterableRegistrar
from ..one import JustLen
from ...functional.mixins import CompositionClassMixin
from ...exceptions import IterError


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
        cls._name = str(name) if name is not None else ''
        cls._string = cls._name or str(iterable)
        cls._iter_type = type(iterable).__name__
        if not hasattr(iterable, '__iter__'):
            message = cls._not_an_iterable_message_for()
            log.error(message)
            raise IterError(message)
        for index, value in enumerate(iterable):
            value_name = cls.__name_from(index, value)
            _ = JustLen(value, name=value_name, length=alen)
        return iterable

    @classmethod
    def __name_from(cls, index: int, value: Any) -> str:
        if cls._iter_type == 'dict':
            return f'key {value} in dict {cls._string}'
        elif cls._iter_type == 'dict_keys':
            string = f'dict {cls._string}' if cls._name else cls._string
            return f'key {value} in ' + string
        elif cls._iter_type == 'dict_values':
            string = f'dict {cls._string}' if cls._name else cls._string
            return f'value {value} in ' + string
        elif cls._iter_type in ('set', 'frozenset'):
            return f'{value} in {cls._iter_type} {cls._string}'
        return (f'{value} with index {index} in '
                f'{cls._iter_type} {cls._string}')
