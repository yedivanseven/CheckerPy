try:
    from .justndim import JustNdim
    from .justshape import JustShape
except ImportError as error:
    __all__ = []
    message = ('Could not import numpy. Is it correctly'
               ' installed and on the python path?')
    raise ImportError(message) from error
else:
    __all__ = ['JustNdim', 'JustShape']
