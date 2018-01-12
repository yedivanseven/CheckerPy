from numpy import uint8, uint16, uint32, uint64
from numpy import int8, int16, int32, int64
from numpy import float16, float32, float64, float128
from numpy import complex64, complex128, complex256
from .justdtype import JustDtype

JustUint8 = JustDtype(uint8, identifier='JustUint8')
JustUint16 = JustDtype(uint16, identifier='JustUint16')
JustUint32 = JustDtype(uint32, identifier='JustUint32')
JustUint64 = JustDtype(uint64, identifier='JustUint64')
JustInt8 = JustDtype(int8, identifier='JustInt8')
JustInt16 = JustDtype(int16, identifier='JustInt16')
JustInt32 = JustDtype(int32, identifier='JustInt32')
JustInt64 = JustDtype(int64, identifier='JustInt64')
JustFloat16 = JustDtype(float16, identifier='JustFloat16')
JustFloat32 = JustDtype(float32, identifier='JustFloat32')
JustFloat64 = JustDtype(float64, identifier='JustFloat64')
JustFloat128 = JustDtype(float128, identifier='JustFloat128')
JustComplex64 = JustDtype(complex64, identifier='JustComplex64')
JustComplex128 = JustDtype(complex128, identifier='JustComplex128')
JustComplex256 = JustDtype(complex256, identifier='JustComplex256')
