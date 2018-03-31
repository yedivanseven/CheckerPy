from types import FunctionType, MethodType
from collections import deque, defaultdict, OrderedDict
from .all import All

OrderedDictKey = type(OrderedDict({}).keys())
OrderedDictValue = type(OrderedDict({}).values())
OrderedDictItem = type(OrderedDict({}).items())

AllNum = All(int, float, identifier='AllNum')
AllSequence = All(str, tuple, list, deque, identifier='AllSequence')
AllIter = All(str, tuple, list, set, dict, frozenset,
              deque, defaultdict, OrderedDict,
              type({}.keys()), type({}.items()), type({}.values()),
              OrderedDictKey, OrderedDictItem, OrderedDictValue,
              identifier='AllIter')
AllFuncMeth = All(FunctionType, MethodType, identifier='AllFuncMeth')
AllLists = All(list, deque, identifier='AllLists')
AllSets = All(set, frozenset, identifier='AllSets')
AllDicts = All(dict, defaultdict, OrderedDict, identifier='AllDicts')
AllKeys = All(type({}.keys()), OrderedDictKey, identifier='AllKeys')
AllValues = All(type({}.values()), OrderedDictValue, identifier='AllValues')
AllItems = All(type({}.items()), OrderedDictItem, identifier='AllItems')
