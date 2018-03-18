import logging as log
from typing import Callable
from ...functional.mixins import CompositionClassMixin
from ...exceptions import CallableError


class JustCall(CompositionClassMixin):
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

    def __new__(cls, callbl: Callable, name: str = None, **kwargs) -> Callable:
        if name is not None:
            cls.__name = str(name)
        elif hasattr(callbl, '__name__'):
            cls.__name = callbl.__name__
        else:
            cls.__name = ''
        if not callable(callbl):
            message = cls.__not_callable_message_for(callbl)
            log.error(message)
            raise CallableError(message)
        return callbl

    @classmethod
    def __not_callable_message_for(cls, callable: Callable) -> str:
        name = cls.__name or callable
        type_name = type(callable).__name__
        return f'Object {name} of type {type_name} is not callable!'
