import logging as log
from typing import Iterable
from .registrars import AllIterableRegistrar
from ..one import NonEmpty
from ...functional.mixins import CompositionClassMixin
from ...exceptions import IterError


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
    For convenience, type checkers for built-in iterables (str, tuple, list,
    set, and dict) and an emptiness checker for `iterable` are attached as
    methods as well.


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

    def __new__(cls, iterable: Iterable, name=None, **kwargs) -> Iterable:
        cls._name = str(name) if name is not None else ''
        cls._string = cls._name or str(iterable)
        cls._iter_type = type(iterable).__name__
        if not hasattr(iterable, '__iter__'):
            message = cls._not_an_iterable_message_for()
            log.error(message)
            raise IterError(message)
        for index, value in enumerate(iterable):
            _ = NonEmpty(value, name=cls.__name_from(index))
        return iterable

    @classmethod
    def __name_from(cls, index: int) -> str:
        if cls._iter_type == 'dict':
            return f'key in dict {cls._string}'
        if cls._iter_type == 'dict_keys':
            string = f'dict {cls._string}' if cls._name else cls._string
            return 'key in ' + string
        elif cls._iter_type == 'dict_values':
            string = f'dict {cls._string}' if cls._name else cls._string
            return 'value in ' + string
        elif cls._iter_type in ('set', 'frozenset'):
            return f'in {cls._iter_type} {cls._string}'
        return f'with index {index} in {cls._iter_type} {cls._string}'
