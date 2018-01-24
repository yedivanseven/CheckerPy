from types import FunctionType, MethodType
from .just import Just

JustNum = Just(int, float, identifier='JustNum')
JustSequence = Just(str, tuple, list, identifier='JustSequence')
JustIter = Just(str, tuple, list, set, dict, frozenset, identifier='JustIter')
JustFuncMeth = Just(FunctionType, MethodType, identifier='JustFuncMeth')
