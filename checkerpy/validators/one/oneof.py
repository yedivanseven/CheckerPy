import logging as log
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
        If `value` is not among the given items.

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

    def __new__(cls, value, name: str = None, *, items=(), **kwargs) -> None:
        cls._name = str(name) if name is not None else ''
        cls._items = cls.__formatted(items)
        if value not in cls._items:
            message = cls.__not_one_of_items_message_for(value)
            log.error(message)
            raise ItemError(message)
        return value

    @staticmethod
    def __formatted(items):
        if type(items) in (tuple, list, set, frozenset):
            if len(items) == 0:
                return items,
            else:
                return items
        return items,

    @classmethod
    def __not_one_of_items_message_for(cls, value) -> str:
        name = ' of '+cls._name if cls._name else ''
        with_type = 'with type ' + type(value).__name__
        if len(cls._items) == 1:
            one_of_items = cls._items[0]
        else:
            one_of_items = f'one of {cls._items}'
        return f'Value {value}{name} {with_type} is not {one_of_items}!'
