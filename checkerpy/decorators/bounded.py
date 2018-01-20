from types import FunctionType, MethodType
from typing import Union, Callable
from .mixins import FunctionTypeMixin, TO_DECORATE, DECORATED
from .boundparser import BoundParser, identity

Func = Union[FunctionType, MethodType]


class Bounded(FunctionTypeMixin):
    """Decorator checks if arguments of functions or methods are within limits.

    Parameters
    ----------
    *arg_limits
        Limits specification for function or method arguments by position. May
        be ellipsis, a 2-tuple, or an iterable of 2-tuples. See Examples.
    **kwarg_limits
        Limits specification for function or method arguments by name. May
        be ellipsis, a 2-tuple, or an iterable of 2-tuples. See Examples.

    Examples
    --------
    To arguments to lie between, above, or below given limits, specify bounds
    as 2-tuple (lo, hi). Use the ellipsis literal ... to skip lo or hi.

    >>> @Bounded((1, ...), (4, 6), (..., 'z'))
    >>> def f(x, y=6, z='foo'):
    ...     return x + y, z

    Use the ellipsis literal also to skip checking an argument.
    >>> @Bounded((1, 3), ..., ('a', 'z'))
    >>> def f(x, y, z):
    ...     return x + y, z

    To ensure an argument is an iterable with all elements between, above, or
    below given limits, specify the desired iterable containing a 2-tuple
    (lo, hi) with the desired bounds. To skip checking dictionary keys or
    values, pass the ellipsis literal ... one of the two.

    >>> @Bounded({(1, 3)}, [(4, ...)] , {('a', 'z'): ...})
    >>> def f(x, y, z):
    ...     return sum(x) + sum(y), z['c']

    To check that an argument is a tuple of arbitrary length and that all its
    elements are between, above, or blow given bounds, specify a 2-tuple
    containing the 2-tuple (lo, hi) and the ellipsis literal ...

    >>> @Bounded(((1, 3), ...), ('a', 'z'))
    >>> def f(x, y):
    ...     return sum(x), y

    To check that an argument is a tuple of fixed length, specify 2-tuples
    (lo, hi) for all its elements. Use (..., ...) to skip checking an element.

    >>> @Bounded(((1, 3), (..., ...), (4, 6)), y=('a', 'z'))
    >>> def f(x, y):
    ...     return x[0] + x[1] + x[2]


    Notes
    -----
    The first argument of (class) methods must be called `self`, `cls`, or
    `mcs`. Also, specifying limits for more arguments than present in the
    function or method call is never a problem and neither is specifying
    limits for named keyword arguments that do not actually occur in the
    function or method signature. Specifying limits per named keyword argument
    takes precedence over limit specification by positional argument.

    Raises
    ------
    TypeError
        If one or more limits are not specified as tuple, list, set, or dict.
    LenError
        If one or more of the tuples specifying limits are not of length 2.
    WrongTypeError
        If (an element of) a function or method argument cannot be compared
        with the limits specified for that argument.
    LimitError
        If (an element of) an argument of a function or method lies on the
        wrong side or outside the limit(s) specified for it.

    See Also
    --------
    Limited, AllLimited, Just, LimitedTuple

    """

    def __init__(self, *arg_limits, **kwarg_limits) -> None:
        parsed = BoundParser()
        self.arg_limits = parsed(arg_limits)
        self.n_arg_limits = len(self.arg_limits)
        self.kwarg_limits = parsed(kwarg_limits)

    def __call__(self, function_to_decorate: TO_DECORATE) -> DECORATED:
        first, func_specs = self.type_of(function_to_decorate)
        arg_string = self.arg_string_from(func_specs)
        arg_count = function_to_decorate.__code__.co_argcount
        kwonly_arg_count = function_to_decorate.__code__.co_kwonlyargcount
        tot_arg_count = arg_count + kwonly_arg_count
        names = function_to_decorate.__code__.co_varnames[first:tot_arg_count]
        n_names = len(names)
        arg_range = range(min(n_names, self.n_arg_limits))
        for arg in arg_range:
            if names[arg] not in self.kwarg_limits.keys():
                self.kwarg_limits.update({names[arg]: self.arg_limits[arg]})

        def bounded_function(*args, **kwargs):
            named_args = kwargs.copy()
            n_args = len(args)
            i_args = range(min(n_args-first, n_names))
            for i in i_args:
                named_args.update({names[i]: args[first+i]})
            for arg_name, arg_value in named_args.items():
                arg_limit = self.kwarg_limits.get(arg_name, identity)
                _ = arg_limit(arg_value, arg_string.format(arg_name))
            return function_to_decorate(*args, **kwargs)

        return self.transfer_attributes(function_to_decorate, bounded_function)

    @staticmethod
    def arg_string_from(func_specs: (str, str, str)) -> str:
        func_string = 'to {} {} defined in module {}'.format(*func_specs)
        return 'argument {} ' + func_string

    @staticmethod
    def transfer_attributes(original: Func, decorated: Callable) -> Func:
        decorated.__annotations__ = original.__annotations__
        decorated.__dict__ = original.__dict__
        decorated.__doc__ = original.__doc__
        decorated.__module__ = original.__module__
        decorated.__name__ = original.__name__
        return decorated
