from types import FunctionType, MethodType
from .just import Just

JustType = Just(type, identifier='JustType')
JustBool = Just(bool, identifier='JustBool')
JustInt = Just(int, identifier='JustInt')
JustFloat = Just(float, identifier='JustFoat')
JustComplex = Just(complex, identifier='JustComplex')
JustStr = Just(str, identifier='JustStr')
JustTuple = Just(tuple, identifier='JustTuple')
JustList = Just(list, identifier='JustList')
JustSet = Just(set, identifier='JustSet')
JustFrozen = Just(frozenset, identifier='JustFrozen')
JustDict = Just(dict, identifier='JustDict')
JustFunc = Just(FunctionType, identifier='JustFunc')
JustMeth = Just(MethodType, identifier='JustMeth')
