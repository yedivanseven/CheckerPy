import logging as log
from typing import Any, Iterable
from .registrars import IterableRegistrar
from ...functional.mixins import CompositionClassMixin
from ...exceptions import ItemError, IterError

dict_keys = type({}.keys())
dict_values = type({}.values())
dict_items = type({}.items())

Iterables = (tuple, list, set, frozenset, dict,
             dict_keys, dict_values, dict_items)
SpecialTypes = (dict_keys, dict_values, dict_items, frozenset)


class Contains(CompositionClassMixin, metaclass=IterableRegistrar):
    """Class for checking if an iterable contains any or all of some items.

    Parameters
    ----------
    iterable
        The iterable to check.
    name : str, optional
        The name of the variable to check. Defaults to None
    every : list(object), optional
        The item(s) that must (all) be contained in the `iterable`.
        Defaults to and empty tuple.
    some : list(object), optional
        The item(s) of which at least one must be contained in the `iterable`.
        Defaults to and empty tuple.

    Returns
    -------
    iterable
        The `iterable` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the value checker to another `callable`, returning the
        functional composition of both. If any of the optional arguments
        `every` and `some` are specified when calling the composition, it
        (or they) are passed through to 'Contains'.

    Notes
    -----
    For convenience, type checkers for built-in iterables (str, tuple, list,
    set, and dict) are attached as methods as well. If any of the optional
    arguments `every` and `some` are specified in calls to these methods, it
    (or they) are passed through to 'Contains'.

    Raises
    ------
    ItemError
        If `iterable` does not contain any or all of the given items.
    IterError
        If `iterable` is not, in fact, an iterable.

    See Also
    --------
    OneOf, CompositionOf

    """

    def __new__(cls, iterable, name=None, *, every=(), some=(), **kwargs):
        cls._name = str(name) if name is not None else ''
        cls.__string = cls.__string_for(iterable)
        cls._every = cls.__validated(every)
        cls._some = cls.__validated(some)
        try:
            all_in = all(item in iterable for item in cls._every)
            any_in = any(item in iterable for item in cls._some)
        except TypeError:
            message = cls.__not_an_iterable_message()
            log.error(message)
            raise IterError(message)
        if cls._every and not all_in:
            missing = list(filter(lambda x: x not in iterable, cls._every))
            message = cls.__some_missing_message_for(missing)
            log.error(message)
            raise ItemError(message)
        if cls._some and not any_in:
            message = cls.__all_missing_message()
            log.error(message)
            raise ItemError(message)
        return iterable

    @classmethod
    def __validated(cls, items: Iterable) -> Iterable:
        if type(items) not in Iterables:
            message = cls.__wrong_specification_message_for(items)
            raise ItemError(message)
        return list(items)

    @staticmethod
    def __wrong_specification_message_for(items: Any) -> str:
        type_of_value = type(items).__name__
        return ('Item(s) to check must be given as a list,'
                f' not as {type_of_value} like {items}!')

    @classmethod
    def __not_an_iterable_message(cls) -> str:
        return (f'{cls.__string.capitalize()} does not seem to '
                'be an iterable whose content could be checked!')

    @classmethod
    def __some_missing_message_for(cls, missing: list) -> str:
        only_one = len(missing) == 1
        prefix = type(missing[0]).__name__.title() if only_one else 'Items'
        items = missing[0] if only_one else missing
        verb = 'is' if only_one else 'are'
        return f'{prefix} {items} {verb} not in {cls.__string}!'

    @classmethod
    def __all_missing_message(cls) -> str:
        only_one = len(cls._some) == 1
        prefix = type(cls._some[0]).__name__.title() if only_one else 'None of'
        items = cls._some[0] if only_one else cls._some
        verb = 'is not' if only_one else 'are'
        return f'{prefix} {items} {verb} in {cls.__string}!'

    @classmethod
    def __string_for(cls, iterable: Iterable) -> str:
        type_of_iterable = type(iterable)
        type_name = type_of_iterable.__name__
        if type_of_iterable in SpecialTypes:
            return type_name+' '+cls._name if cls._name else str(iterable)
        return type_name + ' ' + (cls._name or str(iterable))
