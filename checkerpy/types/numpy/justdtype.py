import logging as log
from typing import Tuple, Union, Iterable, Any
from numpy import dtype
from .docstring import DOC_HEADER, DOC_BODY
from .justndarray import JustNdarray
from ...functional import CompositionOf
from ...functional.mixins import CompositionMixin
from ...exceptions import WrongTypeError, DtypeError

Types = Union[type, Iterable[type]]


class JustDtype(CompositionMixin):
    """Class for easily defining dtype-checker objects for numpy arrays.

    Parameters
    ----------
    types : type
        One or more numpy types to check for.
    identifier : str, optional
        A valid python identifier as name of the dtype checker object.
        Defaults to 'JustD'.

    Raises
    ------
    AttributeError
        If no `types` to check for are found when instantiating the
        dtype-checker object.
    TypeError
        If the `types` to check for specified when instantiating the
        dtype-checker object contain one or more entries that are not of
        type ``type`` themselves.
    ValueError
        If the (optional) `identifier` is not a valid python identifier.

    See Also
    --------
    Just

    """

    def __init__(self, *types: Types, identifier: str = 'JustD') -> None:
        self._name = None
        self.__dtypes = self.__registered(types)
        self.__doc__ = self.__doc_string()
        self.__name__ = self.__identified(identifier)
        setattr(self, 'JustNdarray', CompositionOf(self, JustNdarray))

    @property
    def dtypes(self) -> Tuple[dtype, ...]:
        return self.__dtypes

    def __call__(self, value: Any, name: str = None, **kwargs):
        self._name = str(name) if name is not None else ''
        try:
            value_dtype = value.dtype
        except AttributeError as error:
            message = self.__has_no_dtype_message_for(value)
            log.error(message)
            raise DtypeError(message) from error
        if value_dtype not in self.__dtypes:
            message = self.__error_message_for(value)
            log.error(message)
            raise WrongTypeError(message)
        return value

    def __has_no_dtype_message_for(self, value: Any) -> str:
        value_name = self._name or str(value)
        value_type = type(value).__name__
        return (f'Variable {value_name} of type '
                f'{value_type} has no attribute dtype!')

    def __error_message_for(self, value: Any) -> str:
        name = ' of '+self._name if self._name else ''
        value_type = value.dtype.name
        dtypes = tuple(dtype_.name for dtype_ in self.__dtypes)
        of_type = dtypes[0] if len(dtypes) == 1 else f'one of {dtypes}'
        return f'Dtype{name} must be {of_type}, not {value_type} like {value}!'

    @staticmethod
    def __identified(identifier: str) -> str:
        identifier = str(identifier)
        if not identifier.isidentifier():
            raise ValueError(f'Dtype-checker name {identifier}'
                             f' is not a valid identifier!')
        return identifier

    def __registered(self, types: Tuple[type, ...]) -> Tuple[dtype, ...]:
        if not types:
            raise AttributeError('Found no types to check for!')
        type_is_iter = len(types) == 1 and type(types[0]) in (tuple, list, set)
        types = types[0] if type_is_iter else types
        return tuple(map(self.__dtype_from, types))

    def __dtype_from(self, type_: type) -> dtype:
        try:
            dtype_ = dtype(type_)
        except TypeError:
            message = self.__invalid_type_message_for(type_)
            raise TypeError(message)
        return dtype_

    @staticmethod
    def __invalid_type_message_for(type_: Any) -> str:
        name = type_.__name__ if hasattr(type_, '__name__') else type_
        type_name = type(type_).__name__
        return f'Type of {name} must be type, not {type_name}!'

    def __doc_string(self) -> str:
        dtypes = tuple(dtype_.name for dtype_ in self.__dtypes)
        dtypes_string = dtypes[0] if len(dtypes) == 1 else f'one of {dtypes}'
        doc_string = DOC_HEADER.format(dtypes_string)
        doc_string += DOC_BODY
        return doc_string
