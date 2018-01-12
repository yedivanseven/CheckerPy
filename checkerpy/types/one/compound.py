from .just import Just

JustNum = Just(int, float, identifier='JustNum')
JustSequence = Just(str, tuple, list, identifier='JustSequence')
JustIter = Just(str, tuple, list, set, dict, identifier='JustIter')
