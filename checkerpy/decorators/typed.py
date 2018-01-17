import logging as log
from .mixins import FunctionTypeMixin, TO_DECORATE, DECORATED
from .parser import Parser, any_type
from ..exceptions import WrongTypeError, LenError


class Typed(FunctionTypeMixin):
    """Decorator for checking the types of arguments in functions and methods.

    Examples
    --------
    If all or only the first couple of arguments of a function or method are
    to be type checked, then one or more types per argument may be passed to
    the decorator like so:

    >>> @Typed(int, (int, float))
    >>> def f(x, y=6, *args, **kwargs):
    ...     return x + y + sum(args) + kwargs['z']
    ...
    >>> f(1, 2, 3, 4, z=4)
    15

    If no type check is desired for, say, the second of three arguments, it
    may be skipped like so:
    >>> @Typed(int, ..., str)
    >>> def f(x, y, z):
    ...    return x, y, z
    ...
    >>> f(1, True, 'bar')
    (1, True, 'bar')

    If, however, only one or a few arguments of a function or method are to be
    type checked, then directly assigning one or more types to these arguments
    by `name` might be more convenient.

    >>> class Test:
    ...     @Typed((int, float), v=float, z=str)
    ...     def m(self, x, y, z, u, v):
    ...         return x + y + int(z) + u + v
    ...
    >>> t = Test()
    >>> t.m(1.0, 2, '3', 4, 5.0)
    15.0

    Here, argument `x` is type checked for int or float, `v` for float, and
    `z` for str, whereas arguments `y` and `u` are not type checked at all.

    Notes
    -----
    The first argument of (class) methods must be called `self`, `cls`, or
    `mcs`. Also, specifying types for more arguments than present in the
    function or method call is never a problem and neither is specifying types
    for named keyword arguments that do not actually occur in the function or
    method signature. Specifying types per named keyword argument takes
    precedence over type specification by positional argument.

    Raises
    ------
    TypeError
        If the specified types to check for contain one or more entries that
        are not of type ``type`` themselves.
    WrongTypeError
        If one function or method argument has a type that is not among the
        types specified for that argument.

    See Also
    --------
    Just

    """

    def __init__(self, *arg_types, **kwarg_types) -> None:
        parsed = Parser()
        self.arg_types = parsed(arg_types)
        self.n_arg_types = len(self.arg_types)
        self.kwarg_types = parsed(kwarg_types)

    def __call__(self, function_to_decorate: TO_DECORATE) -> DECORATED:
        first, func_specs = self.type_of(function_to_decorate)
        arg_string = 'argument {}' + self.func_string_from(func_specs)
        arg_count = function_to_decorate.__code__.co_argcount
        names = function_to_decorate.__code__.co_varnames[first:arg_count]
        n_names = len(names)
        arg_range = range(min(n_names, self.n_arg_types))
        for arg in arg_range:
            if names[arg] not in self.kwarg_types.keys():
                self.kwarg_types.update({names[arg]: self.arg_types[arg]})

        def typed_function(*args, **kwargs):
            named_args = kwargs.copy()
            n_args = len(args)
            i_args = range(min(n_args-first, n_names))
            for i in i_args:
                named_args.update({names[i]: args[first+i]})
            for arg_name, arg_value in named_args.items():
                arg_type = self.kwarg_types.get(arg_name, any_type)
                _ = arg_type(arg_value, arg_string.format(arg_name))
            return function_to_decorate(*args, **kwargs)

        typed_function.__name__, typed_function.__module__ = func_specs[1:]
        typed_function.__doc__ = function_to_decorate.__doc__
        return typed_function

    @staticmethod
    def func_string_from(func_specs: (str, str, str)) -> str:
        return ' to {} {} defined in module {}'.format(*func_specs)
