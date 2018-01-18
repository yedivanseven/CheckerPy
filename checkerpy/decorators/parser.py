from typing import Union, Dict, Callable, List, Set, Any
from ..types.all import All, TypedDict, TypedTuple
from ..types.one import Just
from ..validators.one import JustLen

CHECKER_DICT = Dict[type, Callable]
TYPE_SPECS = Union[tuple, dict]
TYPE_CHECKERS = Union[List[Callable], Dict[str, Callable]]
TYPE_ID = Union[int, str]


def any_type(value: Any, name: str = None, **kwargs) -> Any:
    """Simply return the first argument"""
    return value


class Parser:
    """Takes tuple or dict of type specifications and returns type checkers"""
    def __init__(self):
        self.__checker_for: CHECKER_DICT = {type(...): self.ellipsis_checker,
                                            tuple: self.tuple_checker,
                                            list: self.list_checker,
                                            set: self.set_checker,
                                            dict: self.dict_checker,
                                            type: self.type_checker}

    def __call__(self, type_specs: TYPE_SPECS) -> TYPE_CHECKERS:
        type_specs, type_checkers = self.__iterators_for(type_specs)
        for type_id, type_spec in type_specs:
            try:
                checker_for = self.__checker_for[type(type_spec)]
            except KeyError as error:
                message = self.__wrong_spec_message_for(type_spec, type_id)
                raise ValueError(message) from error
            type_checkers[type_id] = checker_for(type_spec, type_id)
        return type_checkers

    def __iterators_for(self, type_specs: TYPE_SPECS):
        type_of_type_specs = type(type_specs)
        if type_of_type_specs not in (tuple, dict):
            message = self.__wrong_iterable_message_for(type_specs)
            raise TypeError(message)
        if type_of_type_specs is tuple:
            type_checkers = [any_type for _ in type_specs]
            type_specs = enumerate(type_specs)
        else:
            type_specs = type_specs.items()
            type_checkers = {}
        return type_specs, type_checkers

    @staticmethod
    def ellipsis_checker(_, __) -> Callable:
        return any_type

    @staticmethod
    def tuple_checker(types, _) -> Callable:
        if ... in types:
            types = tuple(type_ for type_ in types if type_ is not ...)
            return All(*types).JustTuple
        elif all(type(type_) in (tuple, list, set) for type_ in types):

            def typed_tuple(value, name: str = None, **kwargs):
                return TypedTuple(value, name=name, types=types, **kwargs)

            return typed_tuple
        else:
            return Just(*types)

    @staticmethod
    def list_checker(types: List[type], _) -> Callable:
        return All(*types).JustList

    @staticmethod
    def set_checker(types: Set[type], _) -> Callable:
        return All(*types).JustSet

    def dict_checker(self, types: dict, type_id: TYPE_ID) -> Callable:
        types_name = self.__arg_types_string_from(type_id)
        types = JustLen.JustDict(types, name=types_name, length=1)
        keys = tuple(types.keys())[0]
        values = tuple(types.values())[0]

        def typed_dict(mapping, name: str = None):
            return TypedDict(mapping, name=name, keys=keys, values=values)

        return typed_dict

    @staticmethod
    def type_checker(type_: type, _) -> Callable:
        return Just(type_)

    def __wrong_spec_message_for(self, types, type_id: TYPE_ID) -> str:
        arg_type_string = self.__arg_types_string_from(type_id)
        return f'Invalid expression {types} ' + arg_type_string + '!'

    @staticmethod
    def __arg_types_string_from(type_id: TYPE_ID) -> str:
        prefix = ' at position' if type(type_id) is int else ''
        return f'for type specification of argument{prefix} {type_id}'

    @staticmethod
    def __wrong_iterable_message_for(type_specs: TYPE_SPECS) -> str:
        return ('Iterator with type specifications must be either '
                'a tuple (if specified in *args format) or a dict '
                '(if specified in **kwargs format), not a '
                f'{type(type_specs).__name__} like {type_specs}!')
