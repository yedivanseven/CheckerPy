from .all import All
from .base import AllType, AllBool, AllInt, AllFloat, AllStr
from .base import AllTuple, AllList, AllSet, AllDict
from .compound import AllNum, AllIter, AllSequence

__all__ = ['All', 'AllType', 'AllBool', 'AllInt', 'AllFloat',
           'AllStr', 'AllTuple', 'AllList', 'AllSet',
           'AllDict', 'AllNum', 'AllIter', 'AllSequence']

_ALL_COMPARABLES = (AllBool, AllInt, AllFloat, AllStr, AllTuple,
                    AllList, AllSet, AllNum, AllSequence)
_ALL_ITERABLES = (AllStr, AllTuple, AllList, AllSet,
                  AllDict, AllIter, AllSequence)
