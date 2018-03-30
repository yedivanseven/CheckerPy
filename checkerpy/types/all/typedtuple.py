from typing import Tuple, Union, Any, Sequence
from collections import deque
from ...validators.one import JustLen
from ...functional.mixins import CompositionClassMixin
from ..one import Just

Types = Union[type, Sequence[type]]


class TypedTuple(CompositionClassMixin):
    """Checks for different type(s) of each element in a defined-length tuple.

    Parameters
    ----------
    value : tuple
        The tuple to check the length and element types of.
    name : str, optional
        The name of the tuple to check the length and the element type(s) of.
        Defaults to None.
    types : tuple(type), tuple(tuple(type))
        Tuple of the length to check for with either one type for each element
        of `value` or a tuple of types for each element of `value`. Use the
        ellipsis literal ... to skip type checking of the tuple element at
        that position.

    Returns
    -------
    tuple
        The tuple passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the tuple length and type checker to another `callable`,
        returning the functional composition of both. The argument `types` is
        passed through to the `TypedTuple` checker when when calling the
        composition.

    Raises
    ------
    WrongTypeError
        If `value` is not a tuple or if any of its elements do not have (one
        of) the permitted type(s).
    LenError
        If the tuple passed in does not have the same length as `types` or
        if the type specification does not have a meaningful length.
    TypeError
        If `types` is not a tuple or any of its elements are not of type type.

    See Also
    --------
    All, JustLen, CompositionOf

    """

    def __new__(cls, value: tuple, name=None, *, types=(), **kwargs) -> tuple:
        cls.__name = str(name) if name is not None else ''
        cls.__string = cls.__name or str(value)
        types, length = cls.__valid(types)
        value = JustLen.JustTuple(value, name=name, length=length)
        for index, element in enumerate(value):
            if not cls.__is_or_contains_ellipsis(types[index]):
                element_name = f'element {index} in tuple {cls.__string}'
                _ = Just(types[index])(element, name=element_name)
        return value

    @classmethod
    def __valid(cls, types: Sequence[Types]) -> Tuple[Types, int]:
        if type(types) not in (tuple, list, deque):
            message = cls.__wrong_type_message_for(types)
            raise TypeError(message)
        return types, len(types)

    @staticmethod
    def __wrong_type_message_for(types: Any) -> str:
        type_name = type(types).__name__
        return ('Type of types argument must be tuple,'
                f' not {type_name} like {types}!')

    @staticmethod
    def __is_or_contains_ellipsis(types: Types) -> bool:
        is_ellipsis = types is ...
        try:
            contains_ellipsis = ... in types
        except TypeError:
            contains_ellipsis = False
        return is_ellipsis or contains_ellipsis
