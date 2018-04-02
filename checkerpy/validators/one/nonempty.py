import logging as log
from typing import Sized
from ...functional.mixins import CompositionClassMixin
from ...exceptions import EmptyError
from .registrars import SizedRegistrar


class NonEmpty(CompositionClassMixin, metaclass=SizedRegistrar):
    """Checks if an iterable is empty that should not be empty.

    Parameters
    ----------
    iterable
        The iterable to check for emptiness.
    name : str, optional
        The name of the variable to check for emptiness. Defaults to None.

    Returns
    -------
    iterable
        The `iterable` passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the emptiness checker to another `callable`, returning
        the functional composition of both.

    Notes
    -----
    For convenience, type checkers for built-in iterables are attached as
    methods as well.

    Raises
    ------
    EmptyError
        If the emptiness of the argument cannot be determined or if
        `iterable` is empty.

    See Also
    --------
    CompositionOf

    """

    def __new__(cls, iterable: Sized, name: str = None, **kwargs) -> Sized:
        cls.__name = str(name) if name is not None else ''
        try:
            length_of_sizable = len(iterable)
        except TypeError as error:
            message = cls.__cannot_be_empty_message_for(iterable)
            log.error(message)
            raise EmptyError(message) from error
        if length_of_sizable == 0:
            message = cls.__is_empty_message_for(iterable)
            log.error(message)
            raise EmptyError(message)
        return iterable

    @classmethod
    def __cannot_be_empty_message_for(cls, variable) -> str:
        var_name = (cls.__name or str(variable)) + ' with '
        type_name = type(variable).__name__
        return f'Emptiness of {var_name}type {type_name} cannot be determined!'

    @classmethod
    def __is_empty_message_for(cls, iterable: Sized) -> str:
        iter_name = ' '+cls.__name if cls.__name else ''
        type_name = type(iterable).__name__
        return type_name.capitalize() + iter_name + ' must not be empty!'
