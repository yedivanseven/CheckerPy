from typing import Union, Dict, Callable, List, Any

CheckerDict = Dict[type, Callable]
Specs = Union[tuple, dict]
Checkers = Union[List[Callable], Dict[str, Callable]]
SpecID = Union[int, str]


def identity(value: Any, name: str = None, **kwargs) -> Any:
    """Simply return the first argument"""
    return value


class ParserMixin:
    """Provides basic functionality for *args and **kwargs parsers"""
    def __init__(self):
        self._checker_for: CheckerDict = {type(...): self.ellipsis_checker,
                                          list: self.list_checker,
                                          set: self.set_checker,
                                          dict: self.dict_checker,
                                          tuple: self.tuple_checker}

    def __call__(self, specs: Specs) -> Checkers:
        specs, checkers = self._iterators_for(specs)
        for spec_id, spec in specs:
            try:
                checker_for = self._checker_for[type(spec)]
            except KeyError as error:
                message = self._wrong_spec_message_for(spec, spec_id)
                raise TypeError(message) from error
            checkers[spec_id] = checker_for(spec, spec_id)
        return checkers

    def _iterators_for(self, specs: Specs) -> (Specs, Checkers):
        type_of_specs = type(specs)
        if type_of_specs not in (tuple, dict):
            message = self._wrong_iterable_message_for(specs)
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

    @staticmethod
    def _wrong_iterable_message_for(check_specs: Specs) -> str:
        return ('Iterator with specifications for argument checkers must'
                ' be a tuple (if specified in *args format) or a dict '
                '(if specified in **kwargs format), not '
                f'{type(check_specs).__name__} like {check_specs}!')
