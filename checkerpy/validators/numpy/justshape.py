import logging as log
from typing import Union, Any
from numpy import ndarray
from .registrar import Registrar
from ...functional.mixins import CompositionClassMixin
from ...exceptions import ShapeError, IntError

Shape = Union[tuple, list]


class JustShape(CompositionClassMixin, metaclass=Registrar):
    """Class for checking the shape of a numpy array.

    Parameters
    ----------
    array : ndarray
        The numpy array to check the shape of.
    name : str, optional
        The name of the variable to check the shape of. Defaults to None-
    shape : tuple(int), list(tuple(int)), optional
        The allowed shape(s) that `array` can have. Defaults to (...,)

    Returns
    -------
    ndarray
        The `array` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the shape checker to another `callable`, returning the
        functional composition of both. If the optional argument `shape` is
        specified when calling the composition, it is passed through to the
        shape checker.

    Notes
    -----
    For convenience, type checkers for numpy arrays are attached as method as
    well. If the optional argument `shape` is specified in calls to these
    methods, it is passed through to the shape checker.

    Examples
    --------
    One or more dimensions of any of the given shapes can be set to
    ``Ellipsis`` if that dimension is not to be checked for.

    >>> import numpy as np
    >>> a = np.array([[1, 2, 3], [4, 5, 6]])
    >>> JustShape(a, shape=((2, 2), (..., 3)))
    array([[1, 2, 3],
           [4, 5, 6]])

    Raises
    ------
    IntError
        If the specified shape(s) cannot be converted to tuple(s) of integers.
    ShapeError
        If the `shape` argument is not a tuple or list, if the variable passed
        to the shape checker either has not attribute `shape` or if the shape
        of `array` is not among the allowed shapes.

    See Also
    --------
    JustNdim, CompositionOf

    """

    def __new__(cls, array, name=None, *, shape: Shape = (...,), **kwargs):
        cls._name = str(name) if name is not None else ''
        cls.__string = cls._name or str(array)
        cls._shapes = cls.__validated(shape)
        ndims = [len(shape) for shape in cls._shapes]
        try:
            array_shape = array.shape
        except AttributeError as error:
            message = cls.__has_no_shape_message_for(array)
            log.error(message)
            raise ShapeError(message) from error
        array_ndim = len(array_shape)
        ok_indices = [i for i, ndim in enumerate(ndims) if ndim == array_ndim]
        possible_shapes = [cls._shapes[index] for index in ok_indices]
        has_permitted_shape = cls.__compare(array_shape, possible_shapes)
        if not has_permitted_shape:
            message = cls.__wrong_shape_message_for(array_shape)
            log.error(message)
            raise ShapeError(message)
        return array

    @classmethod
    def __validated(cls, shapes: Shape) -> Shape:
        type_of_shape = type(shapes)
        if type_of_shape not in (tuple, list):
            message = cls.__wrong_shape_spec_message_for(shapes)
            raise ShapeError(message)
        if any(type(shape) not in (tuple, list) for shape in shapes):
            shapes = cls.__type_converted(shapes),
        else:
            shapes = list(shapes)
            for i_shape, shape in enumerate(shapes):
                shapes[i_shape] = cls.__type_converted(shape)
        return tuple(shapes)

    @classmethod
    def __type_converted(cls, shape: Shape) -> tuple:
        list_shape = list(shape)
        for i_size, size in enumerate(list_shape):
            if size is not Ellipsis:
                try:
                    list_shape[i_size] = int(size)
                except (ValueError, TypeError) as error:
                    message = cls.__wrong_shape_spec_message_for(shape)
                    raise IntError(message) from error
        return tuple(list_shape)

    @classmethod
    def __compare(cls, array_shape: tuple, possible_shapes: list) -> bool:
        there_are_shapes_of_matching_length = len(possible_shapes)
        shape_matches = ()
        if there_are_shapes_of_matching_length:
            for shape in possible_shapes:
                shape_matches += cls.__compare_sizes_in(array_shape, shape),
        return there_are_shapes_of_matching_length and any(shape_matches)

    @staticmethod
    def __compare_sizes_in(array_shape: tuple, possible_shape: tuple) -> bool:
        sizes_match = ()
        for i_size, size in enumerate(possible_shape):
            sizes_match += (array_shape[i_size] == size) or (size is Ellipsis),
        return all(sizes_match)

    @staticmethod
    def __wrong_shape_spec_message_for(value: Any) -> str:
        type_of_value = type(value).__name__
        return ('Shape argument must be either a single tuple or a list of'
                f' tuples of integers, not a {type_of_value} like {value}!')

    @classmethod
    def __has_no_shape_message_for(cls, variable: Any) -> str:
        variable_type = type(variable).__name__
        return (f'Cannot determine shape of variable {cls.__string} with '
                f'type {variable_type} because it has no attribute shape!')

    @classmethod
    def __wrong_shape_message_for(cls, array_shape: tuple) -> str:
        if len(cls._shapes) == 1:
            of_shape = cls._shapes[0]
        else:
            of_shape = f'one of {cls._shapes}'
        return (f'Shape of array {cls.__string} must'
                f' be {of_shape}, not {array_shape}!')
