try:
    from .justndarray import JustNdarray
    from .justdtype import JustDtype
    from .base import JustInt8, JustInt16, JustInt32, JustInt64
    from .base import JustUint8, JustUint16, JustUint32, JustUint64
    from .base import JustFloat16, JustFloat32, JustFloat64, JustFloat128
    from .base import JustComplex64, JustComplex128, JustComplex256
    from .compound import JustNpNum
except ImportError as error:
    __all__ = []
    message = ('Could not import numpy. Is it correctly'
               ' installed and on the python path?')
    raise ImportError(message) from error
else:
    __all__ = ['JustNdarray', 'JustDtype',
               'JustInt8', 'JustInt16', 'JustInt32', 'JustInt64',
               'JustUint8', 'JustUint16', 'JustUint32', 'JustUint64',
               'JustFloat16', 'JustFloat32', 'JustFloat64', 'JustFloat128',
               'JustComplex64', 'JustComplex128', 'JustComplex256',
               'JustNpNum']
    _NUMPY_TYPES = (JustNdarray,
                    JustInt8, JustInt16, JustInt32, JustInt64,
                    JustUint8, JustUint16, JustUint32, JustUint64,
                    JustFloat16, JustFloat32, JustFloat64, JustFloat128,
                    JustComplex64, JustComplex128, JustComplex256,
                    JustNpNum)
