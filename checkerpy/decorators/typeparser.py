from typing import Callable, List, Set
from ..types.all import All, TypedDict, TypedTuple
from ..types.one import Just
from ..validators.one import JustLen
from .mixin import ParserMixin, SpecID


class TypeParser(ParserMixin):
    """Takes tuple or dict of type specifications and returns type checkers"""
    def __init__(self):
        super().__init__()
        self._checker_for.update({type: self.type_checker})

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

    def dict_checker(self, types: dict, type_id: SpecID) -> Callable:
        types_name = self.__types_string_from(type_id)
        types = JustLen.JustDict(types, name=types_name, length=1)
        keys = tuple(types.keys())[0]
        values = tuple(types.values())[0]

        def typed_dict(mapping, name: str = None):
            return TypedDict(mapping, name=name, keys=keys, values=values)

        return typed_dict

    @staticmethod
    def type_checker(type_: type, _) -> Callable:
        return Just(type_)

    def _wrong_spec_message_for(self, types, type_id: SpecID) -> str:
        types_type = type(types).__name__
        prefix = f'Invalid expression {types} of type {types_type} '
        type_string = self.__types_string_from(type_id)
        postfix = '! Must be one of type, tuple, list, set, dict, or ellipsis.'
        return prefix + type_string + postfix

    @staticmethod
    def __types_string_from(type_id: SpecID) -> str:
        postfix = ' at position' if type(type_id) is int else ''
        return f'for type specification of argument{postfix} {type_id}'
