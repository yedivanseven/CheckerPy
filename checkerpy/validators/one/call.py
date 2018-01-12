import logging as log
from typing import Callable
from ...functional.mixins import CompositionClassMixin
from ...exceptions import CallableError


class Call(CompositionClassMixin):
    """Class for checking if an object is callable.

    Parameters
    ----------
    callbl
        The object to check.
    name : str, optional
        The name of the variable to check. Defaults to None

    Returns
    -------
    callbl
        The callable passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the value checker to another `callable`, returning the
        functional composition of both.

    Raises
    ------
    CallableError
        If `callbl` is not, in fact, callable.

    See Also
    --------
    CompositionOf

    """

    def __new__(cls, callbl: Callable, name=None, **kwargs):
        if name is not None:
            cls._name = str(name)
        elif hasattr(callbl, '__name__'):
            cls._name = callbl.__name__
        else:
            cls._name = ''
        if not callable(callbl):
            message = cls.__not_callable_message_for(callbl)
            log.error(message)
            raise CallableError(message)
        return callbl

    @classmethod
    def __not_callable_message_for(cls, callbl: Callable) -> str:
        name = cls._name or callbl
        type_name = type(callbl).__name__
        return f'Object {name} of type {type_name} is not callable!'
