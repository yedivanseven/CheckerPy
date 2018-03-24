import logging as log
from typing import Any
from ...functional.mixins import CompositionClassMixin
from ...exceptions import ItemError


class OneOf(CompositionClassMixin):
    """Class for checking if a value is one of the given items.

    Parameters
    ----------
    value
        The value to check.
    name : str, optional
        The name of the variable to check. Defaults to None
    items : object, tuple(object), optional
        The item(s) for which to check if `value` is one of them.
        Defaults to and empty tuple.

    Returns
    -------
    value
        The `value` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the value checker to another `callable`, returning the
        functional composition of both.

    Raises
    ------
    ItemError
        If `value` is not among the given items or
        if membership cannot be determined.

    Notes
    -----
    If `value` is an iterable that is to be checked for equality with just
    a single `item` that is also an iterable, the latter must be enclosed in
    a tuple of length one.

    >>> OneOf([1, 2, 3], items=([1, 2, 3], ))
    [1, 2, 3]

    See Also
    --------
    CompositionOf

    """

    def __new__(cls, value, name: str = None, *, items=(), **kwargs):
        cls.__name = ' of '+str(name) if name not in ['', None] else ''
        cls.__items = items
        try:
            value_not_in_items = value not in items
        except TypeError as error:
            message = cls.__cant_determine_membership_message_for(value)
            log.error(message)
            raise ItemError(message) from error
        if value_not_in_items:
            message = cls.__not_in_items_message_for(value)
            log.error(message)
            raise ItemError(message)
        return value

    @classmethod
    def __cant_determine_membership_message_for(cls, value: Any) -> str:
        with_type, one_of_items = cls.__strings_for(value)
        return (f'Cannot determine if value {value}{cls.__name}'
                f' {with_type} is {one_of_items}!')

    @classmethod
    def __not_in_items_message_for(cls, value: Any) -> str:
        with_type, one_of_items = cls.__strings_for(value)
        return f'Value {value}{cls.__name} {with_type} is not {one_of_items}!'

    @classmethod
    def __strings_for(cls, value: Any) -> (str, str):
        try:
            number_of_items = len(cls.__items)
        except TypeError:
            number_of_items = ...
        if number_of_items == 1:
            try:
                items_string = cls.__items[0]
            except (TypeError, IndexError, KeyError):
                items_string = f'one of {cls.__items}'
        elif isinstance(cls.__items, str):
            items_string = f'in str {cls.__items}'
        else:
            items_string = f'one of {cls.__items}'
        return 'with type '+type(value).__name__, items_string
