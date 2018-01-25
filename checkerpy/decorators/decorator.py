from types import FunctionType, MethodType
from typing import Union, Callable, Tuple, Any, Dict
from .mixin import identity

Func = Union[FunctionType, MethodType]
FuncSpecs = Tuple[int, Tuple[str, str, str], tuple]
Decorated = Callable[[Tuple[Any, ...], Dict[str, Any]], Any]


class Decorator:
    def __init__(self, parser: Callable, *arg_specs, **kwarg_specs) -> None:
        self.parsed = parser
        self.arg_checks = self.parsed(arg_specs)
        self.n_arg_specs = len(self.arg_checks)
        self.kwarg_checks = self.parsed(kwarg_specs)

    def __call__(self, function_to_decorate: Func) -> Decorated:
        first_index, func_specs, names = self.type_of(function_to_decorate)
        arg_string = self.arg_string_from(func_specs)
        function_to_decorate.__argnames__ = names
        names = names[first_index:]
        n_names = len(names)
        arg_range = range(min(n_names, self.n_arg_specs))
        for arg in arg_range:
            if names[arg] not in self.kwarg_checks.keys():
                self.kwarg_checks.update({names[arg]: self.arg_checks[arg]})

        def typed_function(*args, **kwargs):
            named_args = kwargs.copy()
            n_args = len(args)
            i_args = range(min(n_args-first_index, n_names))
            for i_arg in i_args:
                named_args.update({names[i_arg]: args[first_index + i_arg]})
            for arg_name, arg_value in named_args.items():
                kwarg_check = self.kwarg_checks.get(arg_name, identity)
                _ = kwarg_check(arg_value, arg_string.format(arg_name))
            return function_to_decorate(*args, **kwargs)

        return self.transfer_attributes(function_to_decorate, typed_function)

    def type_of(self, function_to_decorate: Func) -> FuncSpecs:
        func_name = function_to_decorate.__name__
        module = function_to_decorate.__module__
        if hasattr(function_to_decorate, '__argnames__'):
            arg_names = function_to_decorate.__argnames__
        else:
            arg_names = self.arg_names_from(function_to_decorate)
        if len(arg_names) == 0:
            return 0, ('function', func_name, module), ()
        type_code = 1 if arg_names[0] in ('cls', 'self', 'mcs', 'mcls') else 0
        func_type = 'method' if type_code else 'function'
        return type_code, (func_type, func_name, module), arg_names

    @staticmethod
    def arg_names_from(function_to_decorate: Func) -> tuple:
        arg_count = function_to_decorate.__code__.co_argcount
        kwonly_arg_count = function_to_decorate.__code__.co_kwonlyargcount
        tot_arg_count = arg_count + kwonly_arg_count
        return function_to_decorate.__code__.co_varnames[:tot_arg_count]

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
