import logging as log
from typing import Any
from numpy import ndarray
from .registrar import Registrar
from ...functional.mixins import CompositionClassMixin
from ...exceptions import IntError, SizeError


class JustSize(CompositionClassMixin, metaclass=Registrar):
    """Class for checking the number of elements in a numpy array.

    Parameters
    ---------
    array : ndarray
        The numpy array to check the number of elements of.
    name : str, optional
        The name of the variable to check the number of elements of.
        Defaults to None.
    ndim : int, tuple(int), optional
        The number of elements that should be in `array`. Defaults to 1

    Returns
    -------
    ndarray
        The `array` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the size checker to another `callable`, returning the
        functional composition of both. If the optional argument `size` is
        specified when calling the composition, it is passed through to the
        size checker.

    Notes
    -----
    For convenience, type checkers for numpy arrays are attached as method as
    well. If the optional argument `size` is specified in calls to these
    methods, it is passed through to the size checker.

    Raises
    ------
    IntError
        If the specified size(s) cannot be converted to required type int.
    SizeError
        If the variable passed to the size checker either has not attribute
        `size` or if number of elements in `array` is not among the
        allowed sizes.

    See Also
    --------
    CompositionOf

    """

    def __new__(cls, array: ndarray, name: str = None, *, size=1, **kwargs):
        name = str(name) if name is not None else ''
        cls.__string = name or str(array)
        cls.__sizes = cls.__valid(size)
        try:
            array_size = array.size
        except AttributeError as error:
            message = cls.__has_no_size_message_for(array)
            log.error(message)
            raise SizeError(message) from error
        if array_size not in cls.__sizes:
            message = cls.__error_message_for(array_size)
            log.error(message)
            raise SizeError(message)
        return array

    @classmethod
    def __valid(cls, sizes: Any) -> tuple:
        try:
            converted = tuple(map(cls.__converted, sizes))
        except TypeError:
            converted = tuple(map(cls.__converted, [sizes]))
        return converted

    @classmethod
    def __converted(cls, size: int) -> int:
        try:
            size = int(size)
        except (ValueError, TypeError) as error:
            message = cls.__invalid_size_message_for(size)
            raise IntError(message) from error
        return size

    @staticmethod
    def __invalid_size_message_for(value: Any) -> str:
        type_name = type(value).__name__
        return (f'Could not convert given size {value} of'
                f' type {type_name} to required type int!')

    @classmethod
    def __has_no_size_message_for(cls, variable: Any) -> str:
        variable_type = type(variable).__name__
        return ('Cannot determine the number of elements in variable '
                f'{cls.__string} with type {variable_type} because it'
                ' has no attribute size!')

    @classmethod
    def __error_message_for(cls, size: int) -> str:
        if len(cls.__sizes) == 1:
            of_sizes = cls.__sizes[0]
        else:
            of_sizes = f'one of {cls.__sizes}'
        return (f'The number of elements in array {cls.__string}'
                f' must be {of_sizes}, not {size}!')
