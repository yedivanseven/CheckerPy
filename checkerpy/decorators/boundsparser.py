from typing import Union, Dict, Callable, List, Set, Any, Tuple
from ..validators.all import AllLimited, LimitedTuple
from ..validators.one import JustLen, Limited

CheckerDict = Dict[type, Callable]
Specs = Union[tuple, dict]
Checkers = Union[List[Callable], Dict[str, Callable]]
SpecID = Union[int, str]
Limit = Tuple[Any, Any]


def identity(value: Any, name: str = None, **kwargs) -> Any:
    """Simply return the first argument"""
    return value


class BoundsParser:
    """Takes tuple or dict of limits specs and returns limit checkers"""
    def __init__(self):
        self.__checker_for: CheckerDict = {type(...): self.ellipsis_checker,
                                           list: self.list_checker,
                                           set: self.set_checker,
                                           dict: self.dict_checker,
                                           tuple: self.tuple_checker}

    def __call__(self, specs: Specs) -> Checkers:
        specs, checkers = self.__iterators_for(specs)
        for spec_id, spec in specs:
            try:
                checker_for = self.__checker_for[type(spec)]
            except KeyError as error:
                message = self.__wrong_spec_message_for(spec, spec_id)
                raise ValueError(message) from error
            checkers[spec_id] = checker_for(spec, spec_id)
        return checkers

    def __iterators_for(self, specs: Specs) -> (Specs, Checkers):
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
    def ellipsis_checker(_, __) -> Callable:
        return identity

    def list_checker(self, limits: List[Limit], limits_id: SpecID) -> Callable:
        limits_name = self.__limits_string_from(limits_id)
        limits = JustLen.JustList(limits, name=limits_name, length=1)
        lo, hi = JustLen.JustTuple(limits[0], name=limits_name, length=2)

        def limited_list(value, name: str = None):
            return AllLimited.JustList(value, name=name, lo=lo, hi=hi)

        return limited_list

    def set_checker(self, limits: Set[Limit], limits_id: SpecID) -> Callable:
        limits_name = self.__limits_string_from(limits_id)
        limits = JustLen.JustSet(limits, name=limits_name, length=1)
        lo, hi = JustLen.JustTuple(limits.pop(), name=limits_name, length=2)

        def limited_set(value, name: str = None):
            return AllLimited.JustSet(value, name=name, lo=lo, hi=hi)

        return limited_set

    def dict_checker(self, limits: dict, limits_id: SpecID) -> Callable:
        limits_name = self.__limits_string_from(limits_id)
        limits = JustLen.JustDict(limits, name=limits_name, length=1)
        keys = tuple(limits.keys())[0]
        keys = (..., ...) if keys is ... else keys
        lo_key, hi_key = JustLen.JustTuple(keys, name=limits_name, length=2)
        values = tuple(limits.values())[0]
        values = (..., ...) if values is ... else values
        lo_val, hi_val = JustLen.JustTuple(values, name=limits_name, length=2)

        def limited_dict(mapping, name: str = None):
            _ = AllLimited(mapping, name=name, all_lo=lo_key, all_hi=hi_key)
            _ = AllLimited(mapping.values(), name, all_lo=lo_val, all_hi=hi_val)
            return mapping

        return limited_dict

    def tuple_checker(self, limits: tuple, limits_id: SpecID) -> Callable:
        limits_name = self.__limits_string_from(limits_id)
        if ... in limits:
            limits = tuple(limit for limit in limits if limit is not ...)
            limits = JustLen(limits, name=limits_name, length=1)
            lo, hi = JustLen.JustTuple(limits[0], name=limits_name, length=2)

            def limited_tuple(value, name: str = None):
                return AllLimited.JustTuple(value, name, all_lo=lo, all_hi=hi)

        elif all(type(limit) is tuple for limit in limits):

            def limited_tuple(value, name: str = None):
                return LimitedTuple(value, name=name, limits=limits)

        else:
            lo, hi = JustLen.JustTuple(limits, name=limits_name, length=2)

            def limited_tuple(value, name: str = None):
                return Limited(value, name=name, lo=lo, hi=hi)

        return limited_tuple

    def __wrong_spec_message_for(self, spec, spec_id: SpecID) -> str:
        spec_string = self.__limits_string_from(spec_id)
        return f'Invalid expression {spec} ' + spec_string + '!'

    @staticmethod
    def __limits_string_from(limits_id: SpecID) -> str:
        prefix = ' at position' if type(limits_id) is int else ''
        return f'for limits specification of argument{prefix} {limits_id}'

    @staticmethod
    def __wrong_iterable_message_for(limits_specs: Specs) -> str:
        return ('Iterator with limits specifications must be either '
                'a tuple (if specified in *args format) or a dict '
                '(if specified in **kwargs format), not a '
                f'{type(limits_specs).__name__} like {limits_specs}!')
