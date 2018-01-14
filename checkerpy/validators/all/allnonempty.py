import logging as log
from typing import Iterable
from .registrars import AllIterableRegistrar
from ..one import NonEmpty
from ...functional.mixins import CompositionClassMixin
from ...exceptions import IterError, EmptyError


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
        cls.__string = cls._name or str(iterable)
        if not hasattr(iterable, '__iter__'):
            message = cls.__not_an_iterable_message_for(iterable)
            log.error(message)
            raise IterError(message)
        try:
            _ = tuple(map(NonEmpty, iterable))
        except EmptyError as error:
            message = cls.__is_empty_message_for(iterable)
            log.error(message)
            raise EmptyError(message) from error
        return iterable

    @classmethod
    def __not_an_iterable_message_for(cls, value) -> str:
        type_name = type(value).__name__
        return (f'Variable {cls.__string} with type {type_name} does not'
                ' seem to be an iterable with elements to inspect!')

    @classmethod
    def __is_empty_message_for(cls, iterable: Iterable) -> str:
        type_name = type(iterable).__name__
        return f'An element of the {type_name} {cls.__string} is empty!'
