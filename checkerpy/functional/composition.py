from typing import Callable
from ..exceptions import CallableError


class CompositionOf:
    """Combines two callables into their functional composition.

    Given two functions f(x) and g(x), or any two callables for that matter,
    their functional composition f(g(x)), often also written as (f . g)(x), is
    simply another function h(x) with h = f . g

    Parameters
    ----------
    first, second : callable
        Both callables must accept (i) a single value, (ii) an optional name
        for that value, and (iii) any number of additional keyword arguments.

    Returns
    -------
    CompositionOf
        The returned object is a callable itself, representing the functional
        composition of the two inputs. Attributes of the second input callable
        are simply re-attached to the returned object if they start with a
        lowercase letter. If an attribute starts with an uppercase letter
        and is callable, then a composition of the returned object and that
        attribute is attached to the returned object as attribute.

    Methods
    -------
    o(callable) : CompositionOf
        Visually reminiscent of the "f . g" notation, this method allows
        daisy-chaining another `callable` to the present object, thus returning
        a (callable) composition of the object it is invoked on and the
        callable given as argument.

    Raises
    ------
    CallableError
        If the arguments passed to the constructor are not callable or if,
        when calling the returned object, they turn out not to support the
        call signature specified in the `Parameters` section.

    """

    def __init__(self, first: Callable, second: Callable) -> None:
        self.__first = self.__callable(first)
        self.__second = self.__callable(second)
        self.__copy_attributes('__doc__', '__annotations__', '__module__')
        if hasattr(self.__second, '__name__'):
            self.__name__ = self.__second.__name__
        else:
            self.__name__ = 'Composition'
        if hasattr(self.__second, '__dict__'):
            for attr_name, attr in self.__second.__dict__.items():
                if attr_name[0].isupper() and callable(attr):
                    setattr(self, attr_name, CompositionOf(self, attr))
                if attr_name[0].islower():
                    setattr(self, attr_name, attr)

    def __call__(self, value, name=None, **kwargs):
        try:
            value = self.__second(value, name, **kwargs)
        except TypeError as error:
            message = self.__not_callable_message_for(self.__second)
            raise CallableError(message) from error
        try:
            value = self.__first(value, name, **kwargs)
        except TypeError as error:
            message = self.__not_callable_message_for(self.__first)
            raise CallableError(message) from error
        return value

    def o(self, other: Callable):
        """Daisy-chain self and other callable into new functional composition.

        Parameters
        ----------
        other: callable
            A callable that accepts (i) a single value, (ii) an optional name
            for that value, and (iii) any number of additional keyword
            arguments.

        Returns
        -------
        CompositionOf
            New functional composition, combining self and the passed argument.

        Raises
        ------
        CallableError
            If the passed argument is not, in fact, a callable.

        """
        return CompositionOf(self, other)

    def __callable(self, value: Callable) -> Callable:
        if not callable(value):
            message = self.__not_callable_message_for(value)
            raise CallableError(message)
        return value

    @staticmethod
    def __not_callable_message_for(value: Callable) -> str:
        name = value.__name__ if hasattr(value, '__name__') else str(value)
        return (f'{name} must be a callable that accepts (i) '
                'a value, (ii) an optional name for that value,'
                ' and (iii) any number of keyword arguments!')

    def __copy_attributes(self, *attributes: str) -> None:
        for attribute in attributes:
            if hasattr(self, attribute):
                setattr(self, attribute, getattr(self.__second, attribute))
