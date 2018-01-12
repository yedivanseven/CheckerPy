import logging as log
from typing import Tuple
from .registrar import IterableRegistrar
from ...functional.mixins import CompositionClassMixin
from ...exceptions import LenError, IntError


class JustLen(CompositionClassMixin, metaclass=IterableRegistrar):
    """Checks if the length of an iterable is one of the specified lengths.

    Parameters
    ----------
    iterable
        The iterable to check the length of.
    name : str, optional
        The name of the variable to check the length of. Defaults to None.
    length : int, tuple(int), optional
        One or more lengths that `iterable` should have. Defaults to 1.

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
    set, and dict) are attached as methods as well. If the optional argument
    `length` is specified in calls to these methods, it is passed through to
    the length checker.

    Raises
    ------
    LenError
        If the length of the argument cannot be determined or if the length
        of `iterable` is not among the allowed length.
    IntError
        If the specified length(s) cannot be converted to required type int.

    See Also
    --------
    CompositionOf


    """

    def __new__(cls, iterable, name=None, length=1, **kwargs):
        cls._name = str(name) if name is not None else ''
        cls.__string = cls._name or str(iterable)
        cls._lengths = ()
        lengths = length if type(length) in (tuple, list, set) else (length, )
        for length in lengths:
            cls._lengths += cls.__validated(length)
        try:
            length_of_iterable = len(iterable)
        except TypeError as error:
            message = cls.__has_no_length_message_for(iterable)
            log.error(message)
            raise LenError(message) from error
        if length_of_iterable not in cls._lengths:
            message = cls.__wrong_length_message_for(iterable)
            log.error(message)
            raise LenError(message)
        return iterable

    @classmethod
    def __validated(cls, length: int) -> Tuple[int]:
        try:
            length = int(length)
        except (ValueError, TypeError) as error:
            message = cls.__invalid_type_message_for(length)
            raise IntError(message) from error
        return length,

    @staticmethod
    def __invalid_type_message_for(value) -> str:
        type_name = type(value).__name__
        return (f'Could not convert given length {value} of'
                f' type {type_name} to required type int!')

    @classmethod
    def __has_no_length_message_for(cls, variable) -> str:
        var_name = cls.__string + ' with'
        type_name = type(variable).__name__
        return f'Length of {var_name} type {type_name} cannot be determined!'

    @classmethod
    def __wrong_length_message_for(cls, iterable) -> str:
        if len(cls._lengths) == 1:
            of_length = cls._lengths[0]
        else:
            of_length = f'one of {cls._lengths}'
        actual_len = len(iterable)
        type_name = type(iterable).__name__
        return (f'Length of {type_name} {cls.__string} must'
                f' be {of_length}, not {actual_len}!')
