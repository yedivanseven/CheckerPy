from .mixins import FunctionTypeMixin, TO_DECORATE, DECORATED
from .parser import Parser, any_type


class Typed(FunctionTypeMixin):
    """Decorator for checking the types of arguments in functions and methods.

    Parameters
    ----------
    *arg_types
        Type specification for function or method arguments by position. May
        be ellipsis, a type, or an iterable of types. See Examples.
    **kwarg_types
        Type specification for function or method arguments by name. May
        be ellipsis, a type, or an iterable of types. See Examples.

    Examples
    --------
    To arguments for a single type each, simply specify that type.

    >>> @Typed(int, z=str, y=float)
    >>> def f(x, y, z):
    ...     return x + y, z

    Pass the ellipsis literal ... to skip checking the type of the argument
    at that position.
    >>> @Typed(int, ..., str)
    >>> def f(x, y, z):
    ...     return x + y, z

    To allow multiple types for an argument, pass a tuple of types.

    >>> @Typed((int, float), ..., z=(str, bool))
    >>> def f(x, y, z):
    ...     return x, y, z

    To ensure an argument is an iterable with elements of one or more types,
    specify the desired iterable containing the allowed types. To skip type
    checking of dictionary keys or values, pass the ellipsis literal ... for
    one of the two.

    >>> @Typed([int, bool], {float}, {...: (list, tuple)})
    >>> def f(x, y, z):
    ...     return sum(x) + sum(y), z.keys()

    A typed tuple of arbitrary length is specified by including the ellipsis
    literal ... in the sequence of allowed types.

    >>> @Typed((bool, ...))
    >>> def f(x):
    ...     return any(x)

    A tuple of fixed length with one or more permitted types for each element
    is specified by a tuple of tuples of types. Use the 1-tuple (...,) to skip
    type checking for the tuple element at that position.

    >>> @Typed(((str,), (...,), (int, float)))
    >>> def f(x):
    ...     print(f'{x[0]} is {x[2]} years old.')
    ...     return x[1]

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
    Just, All, TypedTuple, TypedDict

    """

    def __init__(self, *arg_types, **kwarg_types) -> None:
        parsed = Parser()
        self.arg_types = parsed(arg_types)
        self.n_arg_types = len(self.arg_types)
        self.kwarg_types = parsed(kwarg_types)

    def __call__(self, function_to_decorate: TO_DECORATE) -> DECORATED:
        first, func_specs = self.type_of(function_to_decorate)
        arg_string = self.arg_string_from(func_specs)
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
            for i_arg in i_args:
                named_args.update({names[i_arg]: args[first+i_arg]})
            for arg_name, arg_value in named_args.items():
                arg_type = self.kwarg_types.get(arg_name, any_type)
                _ = arg_type(arg_value, arg_string.format(arg_name))
            return function_to_decorate(*args, **kwargs)

        typed_function.__name__, typed_function.__module__ = func_specs[1:]
        typed_function.__doc__ = function_to_decorate.__doc__
        return typed_function

    @staticmethod
    def arg_string_from(func_specs: (str, str, str)) -> str:
        func_string = 'to {} {} defined in module {}'.format(*func_specs)
        return 'argument {} ' + func_string
