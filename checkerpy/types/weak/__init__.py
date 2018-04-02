from .like import Like

__all__ = [
    'LikeContainer',
    'LikeHashable',
    'LikeIterable',
    'LikeIterator',
    'LikeReversible',
    'LikeSized',
    'LikeGenerator',
    'LikeCollection',
    'LikeTuple',
    'LikeSequence',
    'LikeMutableSequence',
    'LikeSet',
    'LikeMutableSet',
    'LikeMapping',
    'LikeMutableMapping'
]

LikeContainer = Like(
    '__contains__',
    identifier='LikeContainer'
)
LikeHashable = Like(
    '__hash__',
    identifier='LikeHashable'
)
LikeIterable = Like(
    '__iter__',
    identifier='LikeIterable'
)
LikeIterator = Like(
    '__iter__',
    '__next__',
    identifier='LikeIterator'
)
LikeReversible = Like(
    '__iter__',
    '__reversed__',
    identifier='LikeReversed'
)
LikeSized = Like(
    '__len__',
    identifier='LikeSized'
)
LikeGenerator = Like(
    '__iter__',
    '__next__',
    'send',
    'throw',
    'close',
    identifier='LikeGenerator'
)
LikeCollection = Like(
    '__contains__',
    '__iter__',
    '__len__',
    identifier='LikeCollection'
)
LikeTuple = Like(
    '__contains__',
    '__iter__',
    '__len__',
    '__getitem__',
    'index',
    'count',
    identifier='LikeTuple'
)
LikeSequence = Like(
    '__contains__',
    '__iter__',
    '__reversed__',
    '__len__',
    '__getitem__',
    'index',
    'count',
    identifier='LikeSequence'
)
LikeMutableSequence = Like(
    '__contains__',
    '__iter__',
    '__reversed__',
    '__len__',
    '__getitem__',
    '__setitem__',
    '__iadd__',
    '__delitem__',
    'index',
    'count',
    'insert',
    'pop',
    'append',
    'reverse',
    'extend',
    'remove',
    identifier='LikeMutableSequence'
)
LikeSet = Like(
    '__contains__',
    '__iter__',
    '__len__',
    '__le__',
    '__lt__',
    '__eq__',
    '__ne__',
    '__gt__',
    '__ge__',
    '__and__',
    '__or__',
    '__sub__',
    '__xor__',
    'isdisjoint',
    identifier='LikeSet'
)
LikeMutableSet = Like(
    '__contains__',
    '__iter__',
    '__len__',
    '__le__',
    '__lt__',
    '__eq__',
    '__ne__',
    '__gt__',
    '__ge__',
    '__and__',
    '__or__',
    '__sub__',
    '__xor__',
    '__ior__',
    '__iand__',
    '__ixor__',
    '__isub__',
    'isdisjoint',
    'add',
    'discard',
    'clear',
    'pop',
    'remove',
    identifier='LikeMutableSet'
)
LikeMapping = Like(
    '__contains__',
    '__iter__',
    '__len__',
    '__getitem__',
    '__eq__',
    '__ne__',
    'keys',
    'items',
    'values',
    'get',
    identifier='LikeMapping'
)
LikeMutableMapping = Like(
    '__contains__',
    '__iter__',
    '__len__',
    '__getitem__',
    '__setitem',
    '__delitem__'
    '__eq__',
    '__ne__',
    'keys',
    'items',
    'values',
    'get',
    'pop',
    'popitem',
    'clear',
    'update',
    'setdefault',
    identifier='LikeMutableMapping'
)

_LIKE_CONTAINERS = (
    LikeContainer,
    LikeIterable,
    LikeIterator,
    LikeReversible
)

_LIKE_ITERABLES =(
    LikeCollection,
    LikeTuple,
    LikeSequence,
    LikeMutableSequence,
    LikeSet,
    LikeMutableSet,
    LikeMapping,
    LikeMutableMapping
)

_LIKE_COMPARABLES = (
    LikeSet,
    LikeMutableSet
)
