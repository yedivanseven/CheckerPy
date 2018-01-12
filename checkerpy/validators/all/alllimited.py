import logging as log
from typing import Iterable
from .registrars import IterableRegistrar, TYPES
from ..one import Limited
from ...types.all import _ALL_COMPARABLES
from ...functional import CompositionOf
from ...functional.mixins import CompositionClassMixin
from ...exceptions import IterError, LimitError


class AllComparableRegistrar(IterableRegistrar):
    """Set compositions of class and all-comparable type checkers as attr's."""
    def __init__(cls, class_name: str, bases: TYPES, attributes: dict) -> None:
        super().__init__(class_name, bases, attributes)
        for comparable in _ALL_COMPARABLES:
            setattr(cls, comparable.__name__, CompositionOf(cls, comparable))


class AllLimited(CompositionClassMixin, metaclass=AllComparableRegistrar):
    """Checks if all elements of an iterable lie outside given limits.

    Parameters
    ----------
    iterable
        The iterable for which to check if its elements lie outside limits.
    name : str, optional
        The name of the variable to check the elements of. Defaults to None.
    lo : optional
        Lower bound for all elements of `iterable`. Defaults to Ellipsis.
    hi : optional
        Upper bound for all elements of `iterable`. Defaults to Ellipsis.

    Returns
    -------
    iterable
        The `iterable` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the limits checker to another `callable`, returning the
        functional composition of both. If `lo` and/or `hi` is specified when
        calling the composition, it (or they) are passed through to the limits
        checker.

    Notes
    -----
    For convenience, type checkers for built-in comparables (i.e., everything
    but dict) and iterables as well as an emptiness checker for `iterable`
    are attached as methods. If `lo` and/or `hi` is specified in calls to these
    methods, it (or they) are passed through to the limits checker.

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

    def __new__(cls, iterable, name=None, lo=..., hi=..., **kwargs):
        cls._name = str(name) if name is not None else ''
        cls.__string = ' ' + (cls._name or str(iterable))
        if not hasattr(iterable, '__iter__'):
            message = cls.__not_an_iterable_message_for(iterable)
            log.error(message)
            raise IterError(message)
        for value in iterable:
            try:
                _ = Limited(value, None, lo=lo, hi=hi, **kwargs)
            except LimitError as error:
                message = cls.__out_of_bounds_message_for(iterable)
                log.error(message)
                raise LimitError(message) from error
        return iterable

    @classmethod
    def __not_an_iterable_message_for(cls, value) -> str:
        type_name = type(value).__name__
        return (f'Variable{cls.__string} with type {type_name} does not'
                ' seem to be an iterable with elements to inspect!')

    @classmethod
    def __out_of_bounds_message_for(cls, iterable: Iterable) -> str:
        type_name = type(iterable).__name__
        return f'An element of the {type_name}{cls.__string} is out of bounds!'
