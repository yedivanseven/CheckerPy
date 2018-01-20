from typing import Union, Dict, Callable, List, Set, Any, Tuple
from ..validators.all import AllLimited, LimitedTuple
from ..validators.one import JustLen, Limited
from ..types.one import JustList, JustTuple, JustSet, JustDict

CheckerDict = Dict[type, Callable]  # same
Specs = Union[tuple, dict]  # same
Checkers = Union[List[Callable], Dict[str, Callable]]  # same
SpecID = Union[int, str]  # same
Limit = Tuple[Any, Any]


def identity(value: Any, name: str = None, **kwargs) -> Any:  # same
    """Simply return the first argument"""
    return value


class BoundParser:
    """Takes tuple or dict of limits specs and returns limit checkers"""
    def __init__(self):
        self.__checker_for: CheckerDict = {type(...): self.ellipsis_checker,  # same
                                           list: self.list_checker,
                                           set: self.set_checker,
                                           dict: self.dict_checker,
                                           tuple: self.tuple_checker}

    def __call__(self, specs: Specs) -> Checkers:  # same
        specs, checkers = self.__iterators_for(specs)
        for spec_id, spec in specs:
            try:
                checker_for = self.__checker_for[type(spec)]
            except KeyError as error:
                message = self.__wrong_spec_message_for(spec, spec_id)
                raise TypeError(message) from error
            checkers[spec_id] = checker_for(spec, spec_id)
        return checkers

    def __iterators_for(self, specs: Specs) -> (Specs, Checkers):  # same
        type_of_specs = type(specs)
        if type_of_specs not in (tuple, dict):
            message = self.__wrong_iterable_message_for(specs)
            raise TypeError(message)
        if type_of_specs is tuple:
            checkers = [identity for _ in specs]
            specs = enumerate(specs)
        else:
            specs = specs.items()
            checkers = {}
        return specs, checkers

    @staticmethod
    def ellipsis_checker(_, __) -> Callable:  # same
        return identity

    def list_checker(self, limits: List[Limit], limits_id: SpecID) -> Callable:
        limits_name = self.__limits_string_from(limits_id).format('')
        list_limits_name = self.__limits_string_from(limits_id).format('list ')
        limits = JustList(limits, name=limits_name)
        limits = JustLen(limits, name='for '+limits_name, length=1)
        limits = JustTuple(limits[0], name=list_limits_name)
        lo, hi = JustLen(limits, name='for '+list_limits_name, length=2)

        def limited_list(value, name: str = None):
            return AllLimited.JustList(value, name=name, all_lo=lo, all_hi=hi)

        return limited_list

    def set_checker(self, limits: Set[Limit], limits_id: SpecID) -> Callable:
        limits_name = self.__limits_string_from(limits_id).format('')
        set_limits_name = self.__limits_string_from(limits_id).format('set ')
        limits = JustSet(limits, name=limits_name)
        limits = JustLen(limits, name='for '+limits_name, length=1)
        limits = JustTuple(limits.pop(), name=set_limits_name)
        lo, hi = JustLen(limits, name='for '+set_limits_name, length=2)

        def limited_set(value, name: str = None):
            return AllLimited.JustSet(value, name=name, all_lo=lo, all_hi=hi)

        return limited_set

    def dict_checker(self, limits: dict, limits_id: SpecID) -> Callable:
        limits_name = self.__limits_string_from(limits_id).format('')
        dict_limits_name = self.__limits_string_from(limits_id).format('dict ')
        limits = JustDict(limits, name=limits_name)
        limits = JustLen(limits, name='for '+limits_name, length=1)
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
            _ = AllLimited(mapping, name=name, all_lo=lo_key, all_hi=hi_key)
            _ = AllLimited(mapping.values(), name=name, all_lo=lo, all_hi=hi)
            return mapping

        return limited_dict

    def tuple_checker(self, limits: tuple, limits_id: SpecID) -> Callable:
        limits_name = self.__limits_string_from(limits_id).format('')
        tup_limits_name = self.__limits_string_from(limits_id).format('tuple ')
        if ... in limits:
            limits = tuple(limit for limit in limits if limit is not ...)
            limits = JustLen(limits, name='for '+limits_name, length=1)
            limits = JustTuple(limits[0], name=tup_limits_name)
            lo, hi = JustLen(limits, name='for '+tup_limits_name, length=2)

            def limited_tuple(value, name: str = None):
                return AllLimited.JustTuple(value, name, all_lo=lo, all_hi=hi)

        elif all(type(limit) is tuple for limit in limits):

            def limited_tuple(value, name: str = None):
                return LimitedTuple(value, name=name, limits=limits)

        else:
            limits = JustTuple(limits, name=limits_name)
            lo, hi = JustLen(limits, name='for '+limits_name, length=2)

            def limited_tuple(value, name: str = None):
                return Limited(value, name=name, lo=lo, hi=hi)

        return limited_tuple

    def __wrong_spec_message_for(self, spec, spec_id: SpecID) -> str:
        spec_string = self.__limits_string_from(spec_id).format('')
        return f'Invalid expression {spec} for ' + spec_string + '!'

    @staticmethod
    def __limits_string_from(limits_id: SpecID) -> str:
        postfix = ' at position' if type(limits_id) is int else ''
        return 'limits specification of {}argument' + f'{postfix} {limits_id}'

    @staticmethod
    def __wrong_iterable_message_for(limits_specs: Specs) -> str:  # same
        return ('Iterator with limits specifications must be either '
                'a tuple (if specified in *args format) or a dict '
                '(if specified in **kwargs format), not a '
                f'{type(limits_specs).__name__} like {limits_specs}!')
