import logging as log
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
    length : int, tuple(int), optional
        One or more lengths that all elements of `iterable` should have.
        Defaults to 1.

    Returns
    -------
    iterable
        The `iterable` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the length checker to another `callable`, returning the
        functional composition of both. If the optional argument `length` is
        specified when calling the composition, it is passed through to the
        length checker.

    Notes
    -----
    For convenience, type checkers for built-in iterables (str, tuple, list,
    set, and dict) and an emptiness checker for `iterable` are attached as
    methods as well. If the optional argument `length` is specified in calls
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

    def __new__(cls, iterable, name=None, length=1, **kwargs):
        cls._name = str(name) if name is not None else ''
        cls.__string = ' ' + (cls._name or str(iterable))
        cls.__iter_type = ' ' + type(iterable).__name__
        if not hasattr(iterable, '__iter__'):
            message = cls.__not_an_iterable_message_for()
            log.error(message)
            raise IterError(message)
        for index, value in enumerate(iterable):
            value_name = cls.__name_from(index, value)
            _ = JustLen(value, name=value_name, length=length)
        return iterable

    @classmethod
    def __not_an_iterable_message_for(cls) -> str:
        return (f'Variable{cls.__string} with type{cls.__iter_type} does'
                ' not seem to be an iterable with elements to inspect!')

    @classmethod
    def __name_from(cls, index: int, value) -> str:
        if cls.__iter_type == ' dict':
            return f'key {value} in dict{cls.__string}'
        elif cls.__iter_type == ' set':
            return f'{value} in set{cls.__string}'
        return f'{value} at position {index} in{cls.__iter_type}{cls.__string}'
