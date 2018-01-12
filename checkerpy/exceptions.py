__all__ = ['WrongTypeError', 'CallableError', 'DtypeError', 'LenError',
           'EmptyError', 'IntError', 'LimitError', 'IterError', 'NdimError',
           'ShapeError', 'IterError']


class WrongTypeError(Exception):
    pass


class CallableError(Exception):
    pass


class DtypeError(Exception):
    pass


class LenError(Exception):
    pass


class EmptyError(Exception):
    pass


class IntError(Exception):
    pass


class LimitError(Exception):
    pass


class IterError(Exception):
    pass


class NdimError(Exception):
    pass


class ShapeError(Exception):
    pass


class ItemError(Exception):
    pass
