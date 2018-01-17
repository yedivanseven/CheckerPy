from typing import Union, Dict, Callable, List, Set, Any
from ..types.all import All, TypedDict, TypedTuple
from ..types.one import Just
from ..validators.one import JustLen

TYPE_SPECS = Union[tuple, dict]
TYPE_CHECKERS = Union[List[Callable], Dict[str, Callable]]
TYPE_ID = Union[int, str]


def any_type(value: Any, name: str = None, **kwargs) -> Any:
    return value


class Parser:
    def __init__(self):
        self.__checker_for = {...: self.ellipsis_checker,
                              tuple: self.tuple_checker,
                              list: self.list_checker,
                              set: self.set_checker,
                              dict: self.dict_checker,
                              type: self.type_checker}

    def __call__(self, type_specs: TYPE_SPECS) -> TYPE_CHECKERS:
        type_specs, type_checkers = self.__iterators_for(type_specs)
        for type_id, type_spec in type_specs:
            type_of = ... if type_spec is ... else type(type_spec)
            checker = self.__checker_for[type_of](type_spec, type_id)
            type_checkers[type_id] = checker
        return type_checkers

    def __iterators_for(self, type_specs: TYPE_SPECS):
        type_of_type_specs = type(type_specs)
        if type_of_type_specs not in (tuple, dict):
            message = ('Iterator with type specifications must be either '
                       'a tuple (if specified in *args format) or a dict '
                       '(if specified in **kwargs format), not a '
                       f'{type_of_type_specs.__name__} like {type_specs}!')
            raise TypeError(message)
        if type_of_type_specs is tuple:
            type_checkers = [any_type for _ in type_specs]
            type_specs = enumerate(type_specs)
        else:
            type_specs = type_specs.items()
            type_checkers = {}
        return type_specs, type_checkers

    @staticmethod
    def ellipsis_checker(ellipsis=..., type_id: TYPE_ID = None) -> Callable:
        return any_type

    @staticmethod
    def __unity(value: Any, name: str = None, **kwargs) -> Any:
        return value

    @staticmethod
    def tuple_checker(types, type_id: TYPE_ID) -> Callable:
        if ... in types:
            types = tuple(type_ for type_ in types if type_ is not ...)
            return All(*types).JustTuple
        elif all(type(type_) is tuple for type_ in types):

            def typed_tuple(value, name: str = None, **kwargs):
                return TypedTuple(value, name=name, types=types, **kwargs)

            return typed_tuple
        else:
            return Just(*types)

    @staticmethod
    def list_checker(types: List[type], type_id: TYPE_ID) -> Callable:
        return All(*types).JustList

    @staticmethod
    def set_checker(types: Set[type], type_id: TYPE_ID) -> Callable:
        return All(*types).JustSet

    @staticmethod
    def dict_checker(types: dict, type_id: TYPE_ID) -> Callable:
        types_name = f'for type specification of argument {type_id}'
        types = JustLen.JustDict(types, name=types_name, length=1)
        keys = tuple(types.keys())[0]
        values = tuple(types.values())[0]

        def typed_dict(mapping, name: str = None, **kwargs):
            return TypedDict(mapping, name=name, keys=keys, values=values)

        return typed_dict

    @staticmethod
    def type_checker(type_: type, type_id: TYPE_ID) -> Callable:
        return Just(type_)
