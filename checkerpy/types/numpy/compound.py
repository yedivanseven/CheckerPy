from numpy import int32, int64, float32, float64
from .justdtype import JustDtype

JustNpNum = JustDtype(int32, int64, float32, float64, identifier='JustNpNum')
