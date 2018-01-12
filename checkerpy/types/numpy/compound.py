from numpy import int16, int32, int64, float16, float32, float64
from .justdtype import JustDtype

JustNpNum = JustDtype(int16, int32, int64, float16, float32, float64,
                      identifier='JustNpNum')
