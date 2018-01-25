import logging as log
from .nonempty import NonEmpty
from .justlen import JustLen
from ...functional.mixins import CompositionClassMixin
from ...functional import CompositionOf
from ...types.one import _COMPARABLES
from ...exceptions import LimitError, WrongTypeError


class ComparableRegistrar(type):
    """Sets compositions of class and type/non-empty checkers as attributes."""
    def __init__(cls, class_name: str, bases, attributes: dict) -> None:
        super().__init__(class_name, (), attributes)
        for comparable in _COMPARABLES:
            setattr(cls, comparable.__name__, CompositionOf(cls, comparable))
        setattr(cls, 'NonEmpty', CompositionOf(cls, NonEmpty))
        setattr(cls, 'JustLen', CompositionOf(cls, JustLen))


class Limited(CompositionClassMixin, metaclass=ComparableRegistrar):
    """Checks if a value lies above, below, or outside given limits.

    Parameters
    ----------
    value
        The value to check.
    name : str, optional
        The name of the variable to check. Defaults to None.
    lo : optional
        Lower bound for `value`. Defaults to Ellipsis.
    hi : optional
        Upper bound for `value`. Defaults to Ellipsis.

    Returns
    -------
    value
        The `value` passed in.

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
    but dict) are attached as methods as well. If `lo` and/or `hi` is specified
    in calls to these methods, it (or they) are passed through to the limits
    checker.

    Raises
    ------
    WrongTypeError
        If `value` cannot be compared to the given limit(s).
    LimitError
        If `value` lies on the wrong side or outside the respective limit(s).

    See Also
    --------
    CompositionOf

    """

    def __new__(cls, value, name: str = None, *, lo=..., hi=..., **kwargs):
        cls._name = str(name) if name is not None else ''
        try:
            value_too_small = False if lo is Ellipsis else value < lo
            value_too_large = False if hi is Ellipsis else value > hi
        except TypeError as error:
            message = cls.__uncomparabel_type_message_for(value, lo, hi)
            log.error(message)
            raise WrongTypeError(message) from error
        if value_too_small or value_too_large:
            message = cls.__value_out_of_bounds_message_for(value, lo, hi)
            log.error(message)
            raise LimitError(message)
        return value

    @classmethod
    def __uncomparabel_type_message_for(cls, value, lo, hi) -> str:
        lo_type = type(lo).__name__
        hi_type = type(hi).__name__
        value_type = type(value).__name__
        value_name = cls._name or str(value)
        return (f'Cannot compare type {value_type} of {value_name}'
                f' with limits of types {lo_type} and {hi_type}!')

    @classmethod
    def __value_out_of_bounds_message_for(cls, value, lo, hi) -> str:
        left = '(-inf' if lo in (float('-inf'), Ellipsis) else f'[{lo}'
        right = 'inf)' if hi in (float('+inf'), Ellipsis) else f'{hi}]'
        value_name = ' of '+cls._name if cls._name else ''
        return (f'Value {value}{value_name} lies outside the'
                f' allowed interval {left}, {right}!')
