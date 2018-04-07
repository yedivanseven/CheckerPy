import logging as log
from typing import Any, Tuple
from collections import defaultdict, deque, OrderedDict
from ...functional.mixins import CompositionClassMixin
from ...exceptions import MissingAttrError, IdentifierError

dict_keys = type({}.keys())
odict_keys = type(OrderedDict({}).keys())
dict_values = type({}.values())
odict_values = type(OrderedDict({}).values())
dict_items = type({}.items())
odict_items = type(OrderedDict({}).items())
named_types = (frozenset, deque, defaultdict, OrderedDict,
               dict_keys, dict_values, dict_items,
               odict_keys, odict_values, odict_items)


class Has(CompositionClassMixin):
    """Checks if an object has (all of) the given attribute(s).

    Parameters
    ----------
    obj : object
        The object to check the attribute(s) of.
    name : str, optional
        The name of the variable to check the attribute(s) of.
        Defaults to None.
    attr : str, tuple(str), optional
        String or tuple of strings with the name(s) of the
        attributes to check for. Defaults to '__new__'.

    Returns
    -------
    object
        The object passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the attribute checker to another `callable`, returning
        the functional composition of both. If the optional argument `attr` is
        specified when calling the composition, it is passed through to the
        attribute checker.

    Raises
    ------
    IdentifierError
        If (one of) the attribute name(s) to check for is not a valid python
        identifier.
    MissingAttrError
        If `obj` does not have (all of) the specified attribute(s).

    See Also
    --------
    CompositionOf

    """

    def __new__(cls, obj, name: str = None, *, attr='__new__', **kwargs):
        cls.__name = str(name) if name is not None else ''
        cls.__string = cls.__string_for(obj)
        cls.__attrs = cls.__valid(attr)
        for attr in cls.__attrs:
            if not hasattr(obj, attr):
                message = (f'Object {cls.__string} does not '
                           f'have required attribute {attr}!')
                log.error(message)
                raise MissingAttrError(message)
        return obj

    @classmethod
    def __valid(cls, attrs: Any) -> Tuple[str]:
        if isinstance(attrs, str):
            return cls.__checked(attrs),
        try:
            checked = tuple(map(cls.__checked, attrs))
        except TypeError as error:
            message = (f'Attribute specification {attrs} seems '
                       'to be neither str not iterable of str!')
            raise IdentifierError(message) from error
        return checked

    @staticmethod
    def __checked(attr: Any) -> str:
        attr = str(attr)
        if attr.isidentifier():
            return attr
        message = f'Attribute name {attr} is not a valid identifier!'
        raise IdentifierError(message)

    @classmethod
    def __string_for(cls, obj) -> str:
        if isinstance(obj, named_types):
            of_type = ' of type ' + type(obj).__name__ if cls.__name else ''
        else:
            of_type = ' of type ' + type(obj).__name__
        return (cls.__name or str(obj)) + of_type
