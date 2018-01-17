import logging as log
from typing import Dict, Tuple, Any, Union
from .mixins import FunctionTypeMixin, TO_DECORATE, DECORATED
from ..validators.one import Limited
from ..exceptions import WrongTypeError, LimitError

LIMITS = Tuple[Any, Any]
ARG_LIMITS = Tuple[LIMITS, ...]
KWARG_LIMITS = Dict[str, Tuple[Any, Any]]


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

    def __init__(self, *arg_limits: LIMITS, **kwarg_limits: LIMITS) -> None:
        self.arg_limits = self.arg_format_checked(arg_limits)
        self.n_arg_limits = len(self.arg_limits)
        self.kwarg_limits = self.kwarg_format_checked(kwarg_limits)

    def __call__(self, function_to_decorate: TO_DECORATE) -> DECORATED:
        first, func_specs = self.type_of(function_to_decorate)
        arg_count = function_to_decorate.__code__.co_argcount
        names = function_to_decorate.__code__.co_varnames[first:arg_count]
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
                limit = self.kwarg_limits.get(arg_name, (..., ...))
                try:
                    _ = Limited(named_args[arg_name], arg_name, *limit)
                except LimitError as error:
                    message = self.out_of_bounds_message_with(func_specs)
                    log.error(message)
                    raise LimitError(message) from error
                except WrongTypeError as error:
                    message = self.uncomparable_message_with(func_specs)
                    log.error(message)
                    raise WrongTypeError(message) from error
            return function_to_decorate(*args, **kwargs)

        bounded_function.__name__, bounded_function.__module__ = func_specs[1:]
        bounded_function.__doc__ = function_to_decorate.__doc__
        return bounded_function

    def arg_format_checked(self, arg_limits: ARG_LIMITS) -> ARG_LIMITS:
        arg_limits = list(arg_limits)
        for arg_number, limit in enumerate(arg_limits):
            arg_limits[arg_number] = (..., ...) if limit is ... else limit
            self.check(arg_number+1, arg_limits[arg_number])
        return tuple(arg_limits)

    def kwarg_format_checked(self, kwarg_limits: KWARG_LIMITS) -> KWARG_LIMITS:
        for arg_name, limit in kwarg_limits.items():
            self.check(arg_name, limit)
        return kwarg_limits

    @staticmethod
    def check(arg_id: Union[int, str], limit: LIMITS) -> None:
        type_of_limit = type(limit)
        if type_of_limit is not tuple:
            message = (f'Type of limits on argument {arg_id} must be tuple,'
                       f' not {type_of_limit.__name__} like {limit}!')
            raise TypeError(message)
        length_of_limit = len(limit)
        if length_of_limit != 2:
            message = ('There must be exactly 2 limits (lo and hi) for'
                       f' argument {arg_id}, not {length_of_limit}!')
            raise ValueError(message)

    @staticmethod
    def out_of_bounds_message_with(func_specs: (str, str, str)) -> str:
        func_type, func_name, module = func_specs
        return (f'An argument of {func_type} {func_name}'
                f' {module} is out of bounds!')

    @staticmethod
    def uncomparable_message_with(func_specs: (str, str, str)) -> str:
        func_type, func_name, module = func_specs
        return (f'An argument of {func_type} {func_name} {module} '
                f'cannot be compared with the corresponding limits!')
