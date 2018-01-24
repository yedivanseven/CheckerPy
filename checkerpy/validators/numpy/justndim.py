import logging as log
from typing import Tuple, Union, List, Any
from numpy import ndarray
from .registrar import Registrar
from ...functional.mixins import CompositionClassMixin
from ...exceptions import IntError, NdimError

NdimType = Union[int, Tuple[int, ...], List[int]]


class JustNdim(CompositionClassMixin, metaclass=Registrar):
    """Class for checking the number of dimensions of a numpy array.

    Parameters
    ---------
    array : ndarray
        The numpy array to check the number of dimensions of.
    name : str, optional
        The name of the variable to check the number of dimensions of.
        Defaults to None.
    ndim : int, tuple(int), optional
        The number of dimensions `array` must have. Defaults to 1

    Returns
    -------
    ndarray
        The `array` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the ndim checker to another `callable`, returning the
        functional composition of both. If the optional argument `ndim` is
        specified when calling the composition, it is passed through to the
        ndim checker.

    Notes
    -----
    For convenience, type checkers for numpy arrays are attached as method as
    well. If the optional argument `ndim` is specified in calls to these
    methods, it is passed through to the ndim checker.

    Raises
    ------
    IntError
        If the specified ndim(s) cannot be converted to required type int.
    NdimError
        If the variable passed to the ndim checker either has not attribute
        `ndim` or if number of dimensions of `array` is not among the
        allowed ndims.

    See Also
    --------
    CompositionOf

    """

    def __new__(cls, array, name: str = None, *, ndim: NdimType = 1, **kwargs):
        cls._name = str(name) if name is not None else ''
        cls.__string = cls._name or str(array)
        ndims = ndim if type(ndim) in (tuple, list, set) else (ndim,)
        cls._ndims = tuple(map(cls.__validate, ndims))
        try:
            array_ndim = array.ndim
        except AttributeError as error:
            message = cls.__has_no_ndim_message_for(array)
            log.error(message)
            raise NdimError(message) from error
        if array_ndim not in cls._ndims:
            message = cls.__error_message_for(array)
            log.error(message)
            raise NdimError(message)
        return array

    @classmethod
    def __validate(cls, ndim: int) -> int:
        try:
            ndim = int(ndim)
        except (ValueError, TypeError) as error:
            message = cls.__invalid_ndim_message_for(ndim)
            raise IntError(message) from error
        return ndim

    @staticmethod
    def __invalid_ndim_message_for(value: Any) -> str:
        type_name = type(value).__name__
        return (f'Could not convert given ndim {value} of'
                f' type {type_name} to required type int!')

    @classmethod
    def __has_no_ndim_message_for(cls, variable: Any) -> str:
        variable_type = type(variable).__name__
        return ('Cannot determine the number of dimensions of variable'
                f' {cls.__string} with type {variable_type} because it'
                ' has no attribute ndim!')

    @classmethod
    def __error_message_for(cls, array: ndarray) -> str:
        if len(cls._ndims) == 1:
            of_ndims = cls._ndims[0]
        else:
            of_ndims = f'one of {cls._ndims}'
        return (f'The number of dimensions of array {cls.__string}'
                f' must be {of_ndims}, not {array.ndim}!')
