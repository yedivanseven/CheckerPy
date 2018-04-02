from typing import Any
from ...functional.mixins import CompositionClassMixin
from ..one import Has
from .registrars import IterableRegistrar


class AllHave(CompositionClassMixin, metaclass=IterableRegistrar):
    """Checks if all elements of an iterable have the given attribute(s).

    Parameters
    ----------
    iterable
        The iterable for which to check the attributes of its elements.
    name : str, optional
        The name of the variable to check the attributes of its elements for.
        Defaults to None.
    attrs : str, tuple(str), optional
        String or tuple of strings with the name(s) of the
        attributes to check for. Defaults to '__new__'.

    Returns
    -------
    iterable
        The `iterable` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the attribute checker to another `callable`, returning the
        functional composition of both. If the optional argument `attrs` is
        specified when calling the composition, it is passed through to the
        attribute checker.

    Notes
    -----
    For convenience, type checkers for built-in iterables and an emptiness
    checker for `iterable` are attached as methods as well. If the optional
    argument `attrs` is specified in calls to these methods, it is passed
    through to the attribute checker.

    Raises
    ------
    IdentifierError
        If (one of) the attribute name(s) to check for is not a valid python
        identifier.
    MissingAttrError
        If one of the elements in the iterable does not have (all of)
        the specified attribute(s).

    See Also
    --------
    Has, CompositionOf

    """

    def __new__(cls, iterable, name: str = None, *, attrs='__new__', **kwargs):
        cls.__name = str(name) if name is not None else ''
        cls._string = cls.__name or str(iterable)
        cls._itertype = type(iterable).__name__
        for index, value in cls._enumerate(iterable):
            value_name = cls.__name_from(index, value)
            _ = Has(value, name=value_name, attr=attrs)
        return iterable

    @classmethod
    def __name_from(cls, index: int, value: Any) -> str:
        named = f'{cls._itertype} {cls.__name}' if cls.__name else cls._string
        if cls._itertype == 'dict':
            return f'{value} in keys to dict {cls._string}'
        elif cls._itertype in ('dict_keys', 'odict_keys'):
            return f'{value} in {named}'
        elif cls._itertype in ('dict_values', 'odict_values'):
            return f'{value} in {named}'
        elif cls._itertype in ('dict_items', 'odict_items'):
            return f'{value} in {named}'
        elif cls._itertype in ('OrderedDict', 'defaultdict'):
            return f'{value} in keys to {named}'
        elif cls._itertype == 'frozenset':
            value = set(value) if type(value) is frozenset else value
            return f'{value} in {named}'
        elif cls._itertype == 'deque':
            return f'{value}{cls.__string_for(index)} in {named}'
        return (f'{value}{cls.__string_for(index)} '
                f'in {cls._itertype} {cls._string}')

    @staticmethod
    def __string_for(index: int) -> str:
        return f' with index {index}' if index >= 0 else ''
