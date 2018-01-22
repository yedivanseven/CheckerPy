from .typeparser import TypeParser
from .decorator import Decorator


class Typed(Decorator):
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
    To check arguments for a single type each, simply specify that type.

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
    The first argument of (class) methods must be called `self`, `cls`, `mcs`,
    or `mcls`. Also, specifying types for more arguments than present in the
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

    def __init__(self, *arg_specs, **kwarg_specs) -> None:
        super().__init__(TypeParser(), *arg_specs, **kwarg_specs)
