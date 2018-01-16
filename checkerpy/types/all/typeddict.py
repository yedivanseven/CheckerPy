from ..one import JustDict, Just
from ...functional import CompositionOf
from ...functional.mixins import CompositionClassMixin
from ...validators.one import JustLen


class Registrar(type):
    """Sets composition of class and JustLen validator as attribute."""
    def __init__(cls, class_name: str, bases, attributes: dict) -> None:
        super().__init__(class_name, (), attributes)
        setattr(cls, 'JustLen', CompositionOf(cls, JustLen))


class TypedDict(CompositionClassMixin, metaclass=Registrar):
    """Checks for the type(s) of keys and/or values in a dictionary.

    Parameters
    ----------
    mapping : dict
        The dictionary to check the type(s) of the keys and/or values for.
    name : str, optional
        The name of the dictionary to check the type(s) of keys and/or values
        for. Defaults to None.
    keys : type, tuple(type), optional
        The type(s) the dictionary keys should have. Defaults to ().
    values : type, tuple(type), optional
        The type(s) the dictionary values should have. Defaults to ().

    Returns
    -------
    dict
        The dictionary passed in.

    Methods
    -------
    o(callable) : CompositionOf
        Daisy-chains the dict type checker to another `callable`, returning
        the functional composition of both. The arguments `keys` and `values`
        are passed through to the `TypedDict` checker when when calling the
        composition.
    JustLen(iterable, name, length) : iterable
        Checks for `length` of `iterable` with `name` before passing it (as
        well as the `keys` and `values` keywords) on to `TypedDict`.

    Raises
    ------
    WrongTypeError
        If `mapping` is not a dict or if any of its keys or values do not have
        (one of) the respective type(s).
    TypeError
        If the type specifications `keys` or `values` are not understood.

    See Also
    --------
    Just, CompositionOf

    """

    def __new__(cls, mapping: dict, name=None, keys=(), values=(), **kwargs):
        cls._name = str(name) if name is not None else ''
        cls.__string = cls._name or str(mapping)
        mapping = JustDict(mapping, name=name, **kwargs)
        if keys and keys is not ...:
            for key in mapping:
                _ = Just(keys)(key, name=f'key in dictionary {cls.__string}')
        if values and values is not ...:
            for key, value in mapping.items():
                value_name = f'entry {key} in dictionary {cls.__string}'
                _ = Just(values)(value, name=value_name)
        return mapping
