from .all import All

AllNum = All(int, float, identifier='AllNum')
AllSequence = All(str, tuple, list, identifier='AllSequence')
AllIter = All(str, tuple, list, set, dict, identifier='AllIter')
