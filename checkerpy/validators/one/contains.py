import logging as log
from typing import Any, Collection, Tuple, Union
from collections import defaultdict, deque, OrderedDict
from ...functional.mixins import CompositionClassMixin
from ...exceptions import ItemError, IterError
from .registrars import ContainerRegistrar

Items = Union[Collection, Tuple[str, ...]]

dict_keys = type({}.keys())
dict_values = type({}.values())
dict_items = type({}.items())
named_types = (frozenset, deque, defaultdict, OrderedDict,
               dict_keys, dict_values, dict_items)
NamedTypes = Union[frozenset, deque, defaultdict, OrderedDict,
                   dict_keys, dict_values, dict_items]


class Contains(CompositionClassMixin, metaclass=ContainerRegistrar):
    """Class for checking if an iterable contains any or all of some items.

    Parameters
    ----------
    iterable
        The iterable to check.
    name : str, optional
        The name of the variable to check. Defaults to None
    every : tuple(object), optional
        The item(s) that must (all) be contained in the `iterable`.
        Defaults to and empty tuple.
    some : tuple(object), optional
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
    For convenience, type checkers for built-in containers are attached as
    methods as well. If any of the optional arguments `every` and `some` are
    specified in calls to these methods, it (or they) are passed through to
    `Contains`.

    Raises
    ------
    ItemError
        If `iterable` does not contain any or all of the given items, or if
        the items are not specified as iterable.
    IterError
        If `iterable` is not, in fact, an iterable.

    See Also
    --------
    OneOf, CompositionOf

    """

    def __new__(cls, iterable, name=None, *, every=(), some=(), **kwargs):
        cls.__name = str(name) if name is not None else ''
        cls.__string = cls.__string_for(iterable)
        cls.__every = cls.__valid(every)
        cls.__some = cls.__valid(some)
        try:
            all_in = all(item in iterable for item in cls.__every)
            any_in = any(item in iterable for item in cls.__some)
        except TypeError:
            message = cls.__not_an_iterable_message()
            log.error(message)
            raise IterError(message)
        if cls.__every and not all_in:
            missing = tuple(filter(lambda x: x not in iterable, cls.__every))
            message = cls.__some_missing_message_for(missing)
            log.error(message)
            raise ItemError(message)
        if cls.__some and not any_in:
            message = cls.__all_missing_message()
            log.error(message)
            raise ItemError(message)
        return iterable

    @classmethod
    def __valid(cls, items: Items) -> Items:
        if isinstance(items, str):
            return tuple(items)
        has_len = hasattr(items, '__len__')
        has_in = hasattr(items, '__contains__') or hasattr(items, '__iter__')
        if has_len and has_in:
            return items
        message = cls.__wrong_specification_message_for(items)
        raise ItemError(message)

    @staticmethod
    def __wrong_specification_message_for(items: Any) -> str:
        type_of_items = type(items).__name__
        return ('Item(s) to check must be given as iterable,'
                f' not as {type_of_items} like {items}!')

    @classmethod
    def __not_an_iterable_message(cls) -> str:
        return (f'{cls.__string.capitalize()} does not seem to '
                'be an iterable whose content could be checked!')

    @classmethod
    def __some_missing_message_for(cls, missing: tuple) -> str:
        only_one = len(missing) == 1
        type_of_first = type(missing[0]).__name__.capitalize()
        prefix = type_of_first if only_one else 'Items'
        items = missing[0] if only_one else missing
        verb = 'is' if only_one else 'are'
        return f'{prefix} {items} {verb} not in {cls.__string}!'

    @classmethod
    def __all_missing_message(cls) -> str:
        only_one = len(cls.__some) == 1
        type_of_first = type(cls.__some[0]).__name__.capitalize()
        prefix = type_of_first if only_one else 'None of'
        items = cls.__some[0] if only_one else cls.__some
        verb = 'is not' if only_one else 'are'
        return f'{prefix} {items} {verb} in {cls.__string}!'

    @classmethod
    def __string_for(cls, iterable: NamedTypes) -> str:
        type_name = type(iterable).__name__
        if isinstance(iterable, named_types):
            return type_name+' '+cls.__name if cls.__name else str(iterable)
        return type_name + ' ' + (cls.__name or str(iterable))
