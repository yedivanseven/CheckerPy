from types import FunctionType, MethodType
from collections import deque, defaultdict, OrderedDict
from .just import Just

OrderedDictKey = type(OrderedDict({}).keys())
OrderedDictValue = type(OrderedDict({}).values())
OrderedDictItem = type(OrderedDict({}).items())

JustNum = Just(int, float, identifier='JustNum')
JustSequence = Just(str, tuple, list, deque, identifier='JustSequence')
JustIter = Just(str, tuple, list, set, dict, frozenset,
                deque, defaultdict, OrderedDict,
                type({}.keys()), type({}.items()), type({}.values()),
                OrderedDictKey, OrderedDictItem, OrderedDictValue,
                identifier='JustIter')
JustFuncMeth = Just(FunctionType, MethodType, identifier='JustFuncMeth')
JustSets = Just(set, frozenset, identifier='JustSets')
JustLists = Just(list, deque, identifier='JustLists')
JustDicts = Just(dict, defaultdict, OrderedDict, identifier='JustDicts')
JustKeys = Just(type({}.keys()), OrderedDictKey, identifier='JustKeys')
JustValues = Just(type({}.values()), OrderedDictValue, identifier='JustValues')
JustItems = Just(type({}.items()), OrderedDictItem, identifier='JustItems')
