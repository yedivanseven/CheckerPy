from .all import All
from ..one import JustDict


class TypedDict:
    def __new__(cls, mapping: dict, name=None, keys=(), values=(), **kwargs):
        cls._name = str(name) if name is not None else ''
        mapping = JustDict(mapping)
        if keys:
            _ = All(keys)(mapping, name=name)
        if values:
            _ = All(values)(mapping.values(), name=name)
        return mapping
