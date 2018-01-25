from typing import Callable, List, Set, Any, Tuple
from ..validators.all import AllLimited, LimitedTuple
from ..validators.one import JustLen, Limited
from ..types.one import JustTuple, JustDict
from .mixin import ParserMixin, SpecID

Limit = Tuple[Any, Any]


class BoundsParser(ParserMixin):
    """Takes tuple or dict of limits specs and returns limit checkers"""

    def list_checker(self, limits: List[Limit], limits_id: SpecID) -> Callable:
        limits_name = 'for ' + self.__limits_string_from(limits_id).format('')
        list_limits_name = self.__limits_string_from(limits_id).format('list ')
        limits = JustLen(limits, name=limits_name, length=1)
        limits = JustTuple(limits[0], name=list_limits_name)
        lo, hi = JustLen(limits, name='for '+list_limits_name, length=2)

        def limited_list(value, name: str = None):
            return AllLimited.JustList(value, name=name, alo=lo, ahi=hi)

        return limited_list

    def set_checker(self, limits: Set[Limit], limits_id: SpecID) -> Callable:
        limits_name = 'for ' + self.__limits_string_from(limits_id).format('')
        set_limits_name = self.__limits_string_from(limits_id).format('set ')
        limits = JustLen(limits, name=limits_name, length=1)
        limits = JustTuple(limits.pop(), name=set_limits_name)
        lo, hi = JustLen(limits, name='for '+set_limits_name, length=2)

        def limited_set(value, name: str = None):
            return AllLimited.JustSet(value, name=name, alo=lo, ahi=hi)

        return limited_set

    def dict_checker(self, limits: dict, limits_id: SpecID) -> Callable:
        limits_name = 'for ' + self.__limits_string_from(limits_id).format('')
        dict_limits_name = self.__limits_string_from(limits_id).format('dict ')
        limits = JustLen(limits, name=limits_name, length=1)
        keys = tuple(limits.keys())[0]
        keys = (..., ...) if keys is ... else keys
        keys = JustTuple(keys, name=dict_limits_name)
        lo_key, hi_key = JustLen(keys, name='for '+dict_limits_name, length=2)
        values = tuple(limits.values())[0]
        values = (..., ...) if values is ... else values
        values = JustTuple(values, name=dict_limits_name)
        lo, hi = JustLen(values, name='for '+dict_limits_name, length=2)

        def limited_dict(mapping, name: str = None):
            mapping = JustDict(mapping, name=name)
            _ = AllLimited(mapping, name=name, alo=lo_key, ahi=hi_key)
            _ = AllLimited(mapping.values(), name=name, alo=lo, ahi=hi)
            return mapping

        return limited_dict

    def tuple_checker(self, limits: tuple, limits_id: SpecID) -> Callable:
        limits_name = 'for ' + self.__limits_string_from(limits_id).format('')
        tup_limits_name = self.__limits_string_from(limits_id).format('tuple ')
        if ... in limits:
            limits = tuple(limit for limit in limits if limit is not ...)
            limits = JustLen(limits, name=limits_name, length=1)
            limits = JustTuple(limits[0], name=tup_limits_name)
            lo, hi = JustLen(limits, name='for '+tup_limits_name, length=2)

            def limited_tuple(value, name: str = None):
                return AllLimited.JustTuple(value, name, alo=lo, ahi=hi)

        elif all(type(limit) is tuple for limit in limits):

            def limited_tuple(value, name: str = None):
                return LimitedTuple(value, name=name, limits=limits)

        else:
            lo, hi = JustLen(limits, name=limits_name, length=2)

            def limited_tuple(value, name: str = None):
                return Limited(value, name=name, lo=lo, hi=hi)

        return limited_tuple

    def _wrong_spec_message_for(self, spec, spec_id: SpecID) -> str:
        spec_type = type(spec).__name__
        prefix = f'Invalid expression {spec} of type {spec_type} for '
        spec_string = self.__limits_string_from(spec_id).format('')
        postfix = '! Must be one of tuple, list, set, dict, or ellipsis.'
        return prefix + spec_string + postfix

    @staticmethod
    def __limits_string_from(limits_id: SpecID) -> str:
        postfix = ' at position' if type(limits_id) is int else ''
        return 'limits specification of {}argument' + f'{postfix} {limits_id}'
