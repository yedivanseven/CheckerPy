from .all import All
from .base import AllType, AllBool, AllInt, AllFloat, AllComplex
from .base import AllStr, AllTuple, AllList, AllSet, AllDict
from .base import AllFunc, AllMeth
from .compound import AllNum, AllIter, AllSequence, AllFuncMeth
from .typeddict import TypedDict
from .typedtuple import TypedTuple

__all__ = ['All', 'AllType', 'AllBool', 'AllInt', 'AllFloat',
           'AllStr', 'AllTuple', 'AllList', 'AllSet', 'AllDict',
           'AllNum', 'AllIter', 'AllSequence',
           'TypedDict', 'TypedTuple']

_ALL_COMPARABLES = (AllBool, AllInt, AllFloat,
                    AllStr, AllTuple, AllList, AllSet,
                    AllNum, AllSequence,
                    TypedTuple, TypedDict)
_ALL_ITERABLES = (AllStr, AllTuple, AllList, AllSet, AllDict,
                  AllIter, AllSequence,
                  TypedDict, TypedTuple)
