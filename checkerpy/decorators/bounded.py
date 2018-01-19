from types import FunctionType, MethodType
from typing import Union, Callable
from .mixins import FunctionTypeMixin, TO_DECORATE, DECORATED
from .boundsparser import BoundsParser, identity

Func = Union[FunctionType, MethodType]


class Bounded(FunctionTypeMixin):
    """Decorator checks if arguments of functions or methods are within limits.

    Examples
    --------
    If all or only the first couple of arguments of a function or method are
    to be checked for limits, then these limits may be passed to the decorator
    like so:

    >>> @Bounded((1, 3), (4, 6))
    >>> def f(x, y=6, *args, **kwargs):
    ...     return x + y + sum(args) + kwargs['z']
    ...
    >>> f(1, 5, 3, 4, z=2)
    15

    If no check is desired for, say, the second of three arguments, it may be
    skipped like so:
    >>> @Bounded((1, 3), ..., (4, 6))
    >>> def f(x, y, z):
    ...     return x + y + z
    ...
    >>> f(2, True, 5.0)
    8.0

    If, however, only one or a few arguments of a function of method are to be
    checked for limits, then directly assigning the limits to these arguments
    by `name` might be more convenient.

    >>> class Test:
    ...     @Bounded((1, 3), v=(4, 6), z=(7, ...))
    ...     def m(self, x, y, z, u, v):
    ...         return x + y + z + u + v
    ...
    >>> t = Test()
    >>> t.m(2, 1, 8, 3, 5)
    19

    Here, argument `x` must lie in the (closed) interval [1, 3], `v` in [4, 6],
    and `z` must be greater of equal than 7.

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
        If one or more limits are not specified as tuples.
    ValueError
        If one or more of the tuples specifying limits are not of length 2.
    WrongTypeError
        If a function or method argument cannot be compared with the limits
        specified for that argument.
    LimitError
        If an argument of a function or method lies above, below, or outside
        the limit(s) specified for it.

    See Also
    --------
    Limited

    """

    def __init__(self, *arg_limits, **kwarg_limits) -> None:
        parsed = BoundsParser()
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
