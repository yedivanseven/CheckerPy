from typing import Tuple, Any
from .registrars import CustomRegistrar
from ...functional.mixins import CompositionClassMixin
from ...validators.one import JustLen, Limited

Limits = Tuple[Tuple[Any, Any], ...]


class LimitedTuple(CompositionClassMixin, metaclass=CustomRegistrar):
    """Checks if the elements of defined-length tuples lie inside given limits.

    Parameters
    ----------
    value : tuple
        The tuple to check the length and the element values of.
    name : str, optional
        The name of the tuple to check the length and the element values of.
        Defaults to None.
    limits : tuple(tuple(lo, hi))
        Tuple of the length to check for containing 2-tuples of limits (lo and
        hi) for each element. Use the ellipsis literal ... to skip value
        checking of the tuple element at that position.

    Returns
    -------
    tuple
        The tuple passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the tuple length and value to another `callable`,
        returning the functional composition of both. The argument `limits` is
        passed through to `LimitedTuple` when when calling the composition.

    Notes
    -----
    For convenience, type checkers for built-in comparables (i.e., everything
    but dict) are also attached as methods. If `limits` are specified in calls
    to these methods, they are passed through to `LimitedTuple`.

    Raises
    ------
    WrongTypeError
        If `value` is not a tuple or if an element of `value` cannot be
        compared to its limit(s).
    LimitError
        If an element of `value` lies on the wrong side or outside its
        respective limit(s).
    LenError
        If `value` is not of the same lenth as `limits`.
    TypeError
        If `limits` is not a tuple or any of its elements are not tuples.
    ValueError
        If one or more of the tuples specifying limits are not of length 2.

    See Also
    --------
    AllLimited, JustLen, Limited, CompositionOf

    """

    def __new__(cls, value: tuple, name: str = None, *, limits=()) -> tuple:
        cls._name = str(name) if name is not None else ''
        cls.__string = cls._name or str(value)
        limits, length = cls.__length_of(limits)
        value = JustLen.JustTuple(value, name=name, length=length)
        for index, element in enumerate(value):
            element_name = f'element {index} in tuple {cls.__string}'
            lo, hi = limits[index]
            _ = Limited(element, name=element_name, lo=lo, hi=hi)
        return value

    @classmethod
    def __length_of(cls, limits: Limits) -> Tuple[Limits, int]:
        if type(limits) not in (tuple, list):
            message = cls.__has_no_length_message_for(limits)
            raise TypeError(message)
        limits = [(..., ...) if limit is ... else limit for limit in limits]
        for index, limit in enumerate(limits):
            type_of_limit = type(limit)
            if type_of_limit is not tuple:
                message = (f'Type of limits on argument {index} must be tuple,'
                           f' not {type_of_limit.__name__} like {limit}!')
                raise TypeError(message)
            length_of_limit = len(limit)
            if length_of_limit != 2:
                message = ('There must be exactly 2 limits (lo and hi) for'
                           f' argument {index}, not {length_of_limit}!')
                raise ValueError(message)
        return tuple(limits), len(limits)

    @staticmethod
    def __has_no_length_message_for(limits: Limits) -> str:
        type_name = type(limits).__name__
        return ('Type of limits argument must be tuple,'
                f' not {type_name} like {limits}!')
