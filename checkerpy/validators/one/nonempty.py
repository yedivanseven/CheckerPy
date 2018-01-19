from typing import Iterable
import logging as log
from .registrar import IterableRegistrar
from ...functional.mixins import CompositionClassMixin
from ...exceptions import EmptyError


class NonEmpty(CompositionClassMixin, metaclass=IterableRegistrar):
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
    For convenience, type checkers for built-in iterables (str, tuple, list,
    set, and dict) are attached as methods as well.

    Raises
    ------
    EmptyError
        If the emptiness of the argument cannot be determined or if
        `iterable` is empty.

    See Also
    --------
    CompositionOf

    """

    def __new__(cls, iterable, name: str = None, **kwargs):
        cls._name = str(name) if name is not None else ''
        try:
            length_of_iterable = len(iterable)
        except TypeError as error:
            message = cls.__cannot_be_empty_message_for(iterable)
            log.error(message)
            raise EmptyError(message) from error
        if length_of_iterable == 0:
            message = cls.__is_empty_message_for(iterable)
            log.error(message)
            raise EmptyError(message)
        return iterable

    @classmethod
    def __cannot_be_empty_message_for(cls, variable) -> str:
        var_name = (cls._name or str(variable)) + ' with '
        type_name = type(variable).__name__
        return f'Emptiness of {var_name}type {type_name} cannot be determined!'

    @classmethod
    def __is_empty_message_for(cls, iterable: Iterable) -> str:
        iter_name = ' '+cls._name if cls._name else ''
        type_name = type(iterable).__name__
        return type_name.capitalize() + iter_name + ' must not be empty!'
