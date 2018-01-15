from types import FunctionType, MethodType
from .all import All

AllType = All(type, identifier='AllType')
AllBool = All(bool, identifier='AllBool')
AllInt = All(int, identifier='AllInt')
AllFloat = All(float, identifier='AllFloat')
AllComplex = All(complex, identifier='AllComplex')
AllStr = All(str, identifier='AllStr')
AllTuple = All(tuple, identifier='AllTuple')
AllList = All(list, identifier='AllList')
AllSet = All(set, identifier='AllSet')
AllDict = All(dict, identifier='AllDict')
AllFunc = All(FunctionType, identifier='AllFunc')
AllMeth = All(MethodType, identifier='AllMeth')
