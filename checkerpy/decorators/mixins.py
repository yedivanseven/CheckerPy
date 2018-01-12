from types import FunctionType, MethodType
from typing import Union, Callable, Tuple, Dict, Any

TO_DECORATE = Union[FunctionType, MethodType]
DECORATED = Callable[[Tuple[Any, ...], Dict[str, Any]], Any]


class FunctionTypeMixin:
    @staticmethod
    def type_of(function_to_decorate: TO_DECORATE) -> (int, (str, str, str)):
        """Extracts type (function or method), name, and module of callable."""
        func_name = function_to_decorate.__name__
        arg_names = function_to_decorate.__code__.co_varnames
        module = 'defined in module ' + function_to_decorate.__module__
        if len(arg_names) == 0:
            return 0, ('function', func_name, module)
        type_code = 1 if arg_names[0] in ('cls', 'self', 'mcs') else 0
        func_type = 'method' if type_code else 'function'
        return type_code, (func_type, func_name, module)
