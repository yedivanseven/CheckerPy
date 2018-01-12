import logging as log
from typing import Union, Tuple
from .mixins import FunctionTypeMixin, TO_DECORATE, DECORATED
from ..types.one import Just
from ..exceptions import WrongTypeError

TYPES = Union[type, Tuple[type, ...]]


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

    If, however, only one or a few arguments of a function of method are to be
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
    The first argument of (class) methods must be called `self` or `cls`. Also,
    specifying types for more arguments than present in the function or method
    call is never a problem and neither is specifying types for named keyword
    arguments that do not actually occur in the function or method signature.

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

    def __init__(self, *arg_types: TYPES, **kwarg_types: TYPES) -> None:
        self.arg_types = []
        for type_ in arg_types:
            type_checker = Just(type_) if self.single(type_) else Just(*type_)
            self.arg_types.append(type_checker)
        self.n_arg_types = len(self.arg_types)
        self.kwarg_types = {}
        for name, type_ in kwarg_types.items():
            type_checker = Just(type_) if self.single(type_) else Just(*type_)
            self.kwarg_types.update({name: type_checker})

    def __call__(self, function_to_decorate: TO_DECORATE) -> DECORATED:
        first, func_specs = self.type_of(function_to_decorate)
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
                arg_type = self.kwarg_types.get(arg_name, lambda x, y: x)
                try:
                    _ = arg_type(arg_value, arg_name)
                except WrongTypeError as error:
                    message = self.error_message_with(func_specs)
                    log.error(message)
                    raise WrongTypeError(message) from error
            return function_to_decorate(*args, **kwargs)

        return typed_function

    @staticmethod
    def single(value: TYPES) -> bool:
        return type(value) not in (tuple, list, set)

    @staticmethod
    def error_message_with(func_specs: (str, str, str)) -> str:
        func_type, func_name, module = func_specs
        return (f'An argument of {func_type} {func_name}'
                f' {module} is of wrong type!')
