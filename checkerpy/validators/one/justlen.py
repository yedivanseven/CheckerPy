import logging as log
from typing import Any, Sized
from ...functional.mixins import CompositionClassMixin
from ...exceptions import LenError, IntError
from .registrars import SizedRegistrar, NAMED_TYPES


class JustLen(CompositionClassMixin, metaclass=SizedRegistrar):
    """Checks if the length of an iterable is one of the specified lengths.

    Parameters
    ----------
    iterable
        The iterable to check the length of.
    name : str, optional
        The name of the variable to check the length of. Defaults to None.
    length : int, tuple(int)
        One or more lengths that `iterable` should have.

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
    For convenience, type checkers for built-in iterables are attached as
    methods as well. If the optional argument `length` is specified in calls
    to these methods, it is passed through to the length checker.

    Raises
    ------
    LenError
        If the length of the argument cannot be determined or if the length
        of `iterable` is not among the allowed lengths.
    IntError
        If the specified length(s) cannot be converted to required type int.

    See Also
    --------
    CompositionOf

    """

    def __new__(cls, iterable: Sized, name=None, *, length, **kwargs) -> Sized:
        cls.__name = str(name) if name is not None else ''
        cls.__string = cls.__name or str(iterable)
        cls.__lengths = cls.__valid(length)
        try:
            length_of_iterable = len(iterable)
        except TypeError as error:
            message = cls.__has_no_length_message_for(iterable)
            log.error(message)
            raise LenError(message) from error
        if length_of_iterable not in cls.__lengths:
            message = cls.__wrong_length_message_for(iterable)
            log.error(message)
            raise LenError(message)
        return iterable

    @classmethod
    def __valid(cls, lengths: Any) -> tuple:
        try:
            converted = tuple(map(cls.__converted, lengths))
        except TypeError:
            converted = tuple(map(cls.__converted, [lengths]))
        return converted

    @classmethod
    def __converted(cls, length: int) -> int:
        try:
            length = int(length)
        except (ValueError, TypeError) as error:
            message = cls.__invalid_length_message_for(length)
            raise IntError(message) from error
        return length

    @classmethod
    def __invalid_length_message_for(cls, length: Any) -> str:
        if isinstance(length, NAMED_TYPES):
            with_type = ''
        else:
            with_type = f' with type {type(length).__name__}'
        return (f'Could not convert given length {length}'
                f'{with_type} to required type int!')

    @classmethod
    def __has_no_length_message_for(cls, value: Any) -> str:
        type_name = cls.__type_name_of(value)
        return f'Length of {type_name}{cls.__string} cannot be determined!'

    @classmethod
    def __wrong_length_message_for(cls, iterable: Sized) -> str:
        if len(cls.__lengths) == 1:
            of_length = cls.__lengths[0]
        else:
            of_length = f'one of {cls.__lengths}'
        actual_length = len(iterable)
        type_name = cls.__type_name_of(iterable)
        return (f'Length of {type_name}{cls.__string} must'
                f' be {of_length}, not {actual_length}!')

    @classmethod
    def __type_name_of(cls, iterable: Sized) -> str:
        if isinstance(iterable, NAMED_TYPES) and not cls.__name:
            return ''
        return type(iterable).__name__ + ' '
