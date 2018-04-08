import logging as log
from ...functional.mixins import CompositionClassMixin
from ...exceptions import IdentifierError
from .registrars import StrRegistrar, NAMED_TYPES


class Identifier(CompositionClassMixin, metaclass=StrRegistrar):
    """Checks if a given string is a valid python identifier.

    Parameters
    ----------
    string : str
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
        cls.__name = str(name) if name is not None else ''
        cls.__string = cls.__string_for(string)
        try:
            string_is_identifier = string.isidentifier()
        except AttributeError:
            string_is_identifier = False
        if not string_is_identifier:
            message = f'{cls.__string} is not a valid identifier!'
            log.error(message)
            raise IdentifierError(message)
        return string

    @classmethod
    def __string_for(cls, string: str) -> str:
        if isinstance(string, str):
            with_value = f'Value {string} of str {cls.__name}'
            return with_value if cls.__name else string
        if isinstance(string, NAMED_TYPES):
            type_of = f'{type(string).__name__} ' if cls.__name else ''
        else:
            type_of = f'{type(string).__name__} '
        return type_of + (cls.__name or str(string))
