import logging as log
from typing import Any
from ...functional.mixins import CompositionClassMixin
from ...exceptions import IdentifierError
from .registrars import StrRegistrar


class Identifier(CompositionClassMixin, metaclass=StrRegistrar):
    """Checks if a given string is a valid python identifier.

    Parameters
    ----------
    string
        The string to check for being an identifier.
    name : str, optional
        The name of the variable to check for being an identifier.
        Defaults to None.

    Returns
    -------
    str
        The `string` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the identifier checker to another `callable`, returning
        the functional composition of both.
    JustStr(value, name) : str
        Checks if `value` with optional name `name` is of type str, returns it
        if so, and raises a WrongTypeError if not.

    Raises
    ------
    IdentifierError
        If `string` is either not a string or not a valid identifier.

    See Also
    --------
    CompositionOf, JustStr

    """

    def __new__(cls, string: str, name: str = None, **kwargs) -> str:
        cls.__name = str(name) if name not in [None, ''] else str(string)
        try:
            string_is_identifier = string.isidentifier()
        except AttributeError:
            string_is_identifier = False
        if not string_is_identifier:
            message = cls.__not_identifier_message_for(string)
            log.error(message)
            raise IdentifierError(message)
        return string

    @classmethod
    def __not_identifier_message_for(cls, value: Any) -> str:
        type_of_value = type(value).__name__
        of_type = '' if type_of_value == 'str' else f' of type {type_of_value}'
        name = cls.__name.capitalize()
        return f'{name}{of_type} is not a valid identifier!'
