from typing import Any, Tuple, Union, Iterable
from ...functional.mixins import CompositionClassMixin
from ...validators.one.has import Has
from .docstring import DOC_HEADER, DOC_BODY

Attributes = Union[str, Iterable[str]]


class Like(CompositionClassMixin):
    """Class for easily and concisely defining attribute-checker objects.

    Parameters
    ----------
    attrs : *str
        One or more attribute(s) to check for.
    identifier : str, optional
        A valid python identifier as name of the attribute-checker object.
        Defaults to 'Like'.

    Raises
    ------
    AttributeError
        If no attributes to check for are found when instantiating the
        attribute-checker object.
    ValueError
        If either the (optional) `identifier` or (any of) the specified
        attribute names are not valid python identifiers.

    """

    def __init__(self, *attrs: Attributes, identifier: str = 'Like') -> None:
        self.__attrs = self.__registered(attrs)
        self.__name__ = self.__identified(identifier)
        self.__doc__ = self.__doc_string()

    @property
    def attrs(self) -> Tuple[str]:
        return self.__attrs

    def __call__(self, value: Any, name: str = None, **kwargs):
        return Has(value, name=name, attr=self.__attrs)

    def __registered(self, attrs: Any) -> Tuple[str]:
        if not attrs:
            raise AttributeError('Found no attributes to check for!')
        if any(type(attr) is str for attr in attrs):
            return tuple(map(self.__checked, attrs))
        try:
            attrs = tuple(map(self.__checked, attrs[0]))
        except TypeError:
            attrs = tuple(map(self.__checked, attrs))
        return attrs

    @staticmethod
    def __checked(attr: Any) -> str:
        attr = str(attr)
        if attr.isidentifier():
            return attr
        raise ValueError(f'Attribute name {attr} is not a valid identifier!')

    @staticmethod
    def __identified(identifier: str) -> str:
        identifier = str(identifier)
        if not identifier.isidentifier():
            raise ValueError(f'Attribute-checker name {identifier}'
                             f' is not a valid identifier!')
        return identifier

    def __doc_string(self) -> str:
        if len(self.__attrs) == 1:
            attrs_string = ' ' + self.__attrs[0]
        else:
            attrs_string = f's {self.__attrs}'
        doc_string = DOC_HEADER.format(attrs_string)
        doc_string += DOC_BODY
        return doc_string
