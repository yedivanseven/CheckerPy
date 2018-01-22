# CheckerPy

_Provides type and value checkers both as callables and as decorators_

## Introduction
The purpose of this package is provide a series of type and value checkers.
They all work in the same way:
- A variable or literal is passed as argument to the checker.
- If it passes the check(s), it is returned unaltered in type and value.
- If it does _not_ pass the checks, an informative error is raised and logged.
To make the error messages more expressive, an optional variable name can be
passed to all checkers.

Some of these type and value checkers are bundled in _decorators_ to
conveniently check the arguments of functions or methods. 

#### Installation
This package is available on the
[Python Package Index](https://pypi.python.org/pypi/checkerpy) `PyPI`.
To install, open a terminal and simply type:
```
pip install checkerpy
```

#### Related work
You might want to consider also
[pycheck](https://pypi.python.org/pypi/pycheck/0.1), 
[pychecked](https://github.com/a-tal/pychecked), 
[typechecker](https://pypi.python.org/pypi/typechecker/0.1.1), 
[typecheck3](https://pypi.python.org/pypi/typecheck3/0.1.0), 
[enforce](https://github.com/RussBaz/enforce), 
[pysignature](https://github.com/intelimetrica/pysignature), 
[pytypes](https://pypi.python.org/pypi/pytypes/1.0b3), 
[typecheck-decorator](https://github.com/prechelt/typecheck-decorator),
[typeguard](https://github.com/agronholm/typeguard), or
[mypy](http://mypy-lang.org/). I apologize if I have
missed your favorite package in this list.

## Usage
1. [Single Values](#chapter1)
2. [Iterables](#chapter2)
3. [Numpy Support](#chapter3)
4. [Combining Validators](#chapter4)
5. [Decorators](#chapter5)
-----------------------

### 1. Single Values <a name=chapter1></a>
#### 1.1 Type checking
Type checkers are created by instantiating the class `Just`. To, for example,
create one for integers, you would do:
```python
from checkerpy.types.one import Just

JustInt = Just(int, identifier='JustInt')
```
The `identifier` keyword is entirely _optional_. Its sole purpose is to enable
the dynamic creation of nicer docstrings. The types a type checker is checking
for (`int` in this case) are stored in its `types` property.
```python
>>> JustInt.types
(int, )
```

Once instantiated, the type checker can be used on a literal
```python
out = JustInt(1)
```
or a variable.
```python
inp = 2
out = JustInt(inp)
```
As a matter of fact, `CheckerPy` already comes with type checkers for all
built-in types predefined. So you could just do
```python
from checkerpy.types.one import * 

i = JustInt(1)
s = JustStr('foo')
l = JustList(['foo', 'bar', 'egg'])
... 
```
You can also be less restrictive and, for example, allow a variable to be
either a `list` or a `tuple`. In this case, you would instantiate and use the
type checker like so:
```python
JustListTuple = Just(list, tuple)
out = JustListTuple(['foo', 'bar', 'egg'])
```
Some of these combined types are already predefined in `CheckerPy`. To check 
for `int` _or_ `float`, for example, you could do:
```python
n = JustNum(2.0)
```
Moreover, you can easily build checkers for your own types.
```python
class MyFirst:
    def foo(self, x):
        return x


class MySecond:
    def bar(self, y):
        print(y)
        
JustMyTypes = Just(MyFirst, MySecond, identifier='JustMyTypes')

inp = MySecond()
out = JustMyTypes(inp, 'the ultimate object')
```

#### 1.2 Value checking
Other than checking for type, `CheckerPy` also comes with validators for 
bounds and membership of a set as well as emptiness and length of iterables.
```python
from checkerpy.validators.one import Limited, OneOf, NonEmpty, JustLen, JustCall
```
##### 1.2.1 NonEmpty
As the name implies, `NonEmpty` raises and logs an error if an (optionally
named) iterable is empty and passes it right through if it isn't. So, in the
case of,
```python
out = NonEmpty(('foo', 'bar', 'egg'))
```
`out` will be the tuple `('foo', 'bar', 'egg'')`, whereas
```python
out = NonEmpty({}, name='of cheeses')
```
will raise and log an `EmptyError: Dict of cheeses must not be empty!` Likewise,
an error is raised and logged if the emptiness of the value passed to the
validator cannot be determined, that is,
```python
out = NonEmpty(1, 'brain')
```
will result in an `EmptyError: Emptiness of brain with type int cannot be
determined!`

##### 1.2.2 JustLen
If an (optionally named) iterable should have a certain length or one of a
couple of lengths, you can simply do
```python
out = JustLen({'foo', 'bar', 'egg'}, length=3)
```
or:
```python
out = JustLen(('Stilton', 'Camembert'), name='cheeses', length=(3, 5))
```
An error is not only logged and raised if the length of the iterable is not 
among the specified lengths, but also if the value passed in is not, in fact,
an iterable.

##### 1.2.3 Limited
To check if an (optionally named) value is above, below or outside given
bounds, you use
```python
out = Limited(3, name='level of detail', lo=1, hi=5)
```
Note that the limits are inclusive and, therefore, both 1 and 5 would pass the
test. If you want to check for a lower limit only or for an upper bound only,
just don't specify the respective other limit.

##### 1.2.4 OneOf
If you want to make sure that an (optionally named) variable has one of a given
set of values, you simply do:
```python
out = OneOf('medium', name='steak', items=('rare', 'medium', 'well done'))
```

##### 1.2.5 JustCall
If you want ot make sure that an (optionally named) object is callable, you
can write:
```python
def cheese_shop(x):
    return f'No, sorry, we are out of {x} ...'
    
out = JustCall(cheese_shop, name='silly function')
```

### 2. Iterables <a name=chapter2></a>
-------------------------------------------------------------------------------
[Single Values](#chapter1) | **Iterables** | [Numpy Support](#chapter3) | 
[Combining Validators](#chapter4) | [Decorators](#chapter5)
-------------------------------------------------------------------------------

This sections assumes that you have already read section (1) because the
validators for iterables simply extend what has been introduced there to all
elements of an iterable.
#### 2.1 Type checking
##### 2.1.1 Simple iterables
Type checkers for all elements of an iterable are created by instantiating the
class `All`. To, for example, create one for integers, you would do:
```python
from checkerpy.types.all import All

AllInt = All(int, identifier='AllInt')
```
As for single values, you don't actually have to do this, because checkers for
all built-in types are predefined.
```python
from checkerpy.types.all import *

i = AllInt((1, 2, 3))
f = AllFloat([4.0, 5.0, 6.0])
n = AllNum({1: 'one', 2.0: 'two'})
s = AllStr({'foo', 'bar', 'egg'})
...
```
You would probably use `All` only to create type checkers for you own types
or for custom combination of types.

If just one element of the iterable in question is not of one of the allowed
types, or if the variable passed to the validator is not, in fact, an iterable,
an informative error is raised and logged.

##### 2.1.2 TypedDict
In the example

#### 2.2 Value Checking
With the exception of `OneOf`, all value checkers introduced in subsection
(1.2) are also available for the elements of an iterable.
```python
from checkerpy.validators.all import AllLimited, AllNonEmpty, AllLen 
```
If, for example, you want to check a list of 2-tuples, use:
```python
out = AllNonEmpty([(1, 2), (3, 4), (5, 6)], name='short')
out = AllLen([(1, 2), (3, 4), (5, 6)], 'short', length=2)
out = AllLimited([(1, 2), (3, 4), (5, 6)], 'short', lo=(1, 1))
```
Again, you get two errors raised (and logged) if an iterable does not pass the
test.
```
>>> out = AllNonEmpty([(), (3, 4), (5, 6)], name='short')
...
EmptyError: Tuple must not be empty!
...
EmptyError: An element of the list short is empty!
```
```
>>> out = AllLen([(1,), (3, 4), (5, 6)], 'short', length=2)
...
LenError: Length of tuple (1,) must be 2, not 1!
...
LenError: An element of the list short has the wrong length!
```
```
>>> out = AllLimited([(0, 1), (3, 4), (5, 6)], 'short', lo=(1, 1))
...
LimitError: Value (0, 1) lies outside the allowed interval [(1, 1), Ellipsis)!
...
LimitError: An element of the list short is out of bounds!
```
If you try to check something that is not an iterable, the `IterError`
introduced in subsection (2.1) is raised and logged.

### 3. Numpy Support <a name=chapter3></a>
You don't need to have `numpy` installed to use `CheckerPy`. If you nevertheless try
to import something from a _numpy_ subpackage, you'll simply get an
`ImportError`. If, however, you do have `numpy` installed, then you have a
couple of additional validators available to you.

#### 3.1 Simple type checking
You can, of course, simply use `Just` to check for the type of numpy _scalars_.
```python
import numpy as np
from checkerpy.types.one import Just

JustNumber = Just(np.int32, np.int64, np.float32, np.float64)
a = np.array([1, 2, 3])
out = JustNumber(a[0])
```
Of course, you can also check if a variable is a numpy array,
```python
JustNdarray = Just(np.ndarray, identifier='JustArray')

inp = np.array([4.0, 5.0, 6.0])
out = JustNdarray(inp)
```
but you don't actually have to do this yourself because the type checker
for `ndarray` is predefined already.
```python
from checkerpy.types.numpy import JustNdarray
```

#### 3.2 Dtype checking
Both numpy scalars and arrays have a `dtype` that you can check for. In full
analogy to the `Just` class introduced in subsection (1.1), `CheckerPy`
provides a just `JustDtype` class that you can use to create dtype checkers 
for numpy arrays.
```python
from checkerpy.types.numpy import JustDtype

JustUint8 = JustDtype(np.uint8)

a = np.array([1, 2, 3], dtype='uint8')
out = JustUint8(a, name='small ints')
```
Again, you don't have to do this manually because `CheckerPy` comes with
type checkers for many of the numeric numpy dtypes predefined. The dtypes
they check for are stored in their `dtypes` property.
```python
>>> JustUint8.dtypes
(dtype('uint8'),)
```

If the numpy array or scalar to be checked does not have (one of) the required
dtypes, the same `WrongTypeError` as introduced in subsection (1.1) is raised
and logged. The only difference is that _Type_ is replaced by _Dtype_ in the
error and log messages.

If you pass something that doesn't have a `dtype` attribute to these dtype
checkers,
```python
out = JustUint8(4)
```
you get a `DtypeError: Variable 4 of type int has no attribute dtype!` raised
and logged.

#### 3.3 Checking the number of dimensions
The dimensionality of numpy arrays is stored in their `ndim` attribute. If you
want to make sure that a numpy array has (one of) a certain number of
dimensions, you do
```python
from checkerpy.validators.numpy import JustNdim

a = np.array([[1, 2, 3], [4, 5, 6]])
out = JustNdim(a, ndim=(1, 2))
```
or just:
```python
out = JustNdim(a, name='numbers', ndim=2)
```
If the number of dimensions is not among the permitted dimensions,
```python
a = np.array([1, 2, 3])
out = JustNdim(a, ndim=2)
```
you get a `NdimError: The number of dimensions of array [1 2 3] must be 2,
not 1!` raised and logged and, if the value to be checked is not a numpy array,
```python
out = JustNdim('foo', ndim=2)
```
yout get a `NdimError: Cannot determine the number of dimensions of variable
foo with type str because it has no attribute ndim!` raised and logged.

#### 3.4 Checking for shape
The actual shape of numpy arrays is stored in their `shape` attribute. To
check if a given numpy array has a certain shape, use
```python
from checkerpy.validators.numpy import JustShape

a = np.array([[1, 2, 3], [4, 5, 6]])
out = JustShape(a, name='2x3', shape=(2, 3))
```
If you want to be less restrictive, you can specify more than one shape.
```python
out = JustShape(a, shape=[(2, 3), (2, 2), (1, 3)])
```
You can also just specify some dimension of the required shape(s) and leave
the others open. Specifying, for example,
```python
out = JustShape(a, shape=[(..., 3), (2, ...)])
```
checks that array _a_ either has 3 columns and an arbitrary number of rows, or
2 rows and an arbitrary number of columns. If it does not,
```python
a = np.array([1, 2, 3])
out = JustShape(a, shape=[(..., 3), (2, ...)])
```
you get a `ShapeError: Shape of array [1 2 3] must be one of ((Ellipsis, 3),
(2, Ellipsis)), not (3,)!` raised and logged. If the value passed to the
validator does not have a `shape` attribute,
```python
out = JustShape(1, shape=[(..., 3), (2, ...)])
```
you get a `ShapeError: Cannot determine shape of variable 1 with type int
because it has no attribute shape!` raised and logged.

### 4. Combining Validators <a name=chapter4></a>
What if you want to check for more than one property, for example, type _and_
value? The simplest thing you could do would be to call the second validator
on the result of the first.
```python
from checkerpy.types.one import JustList
from checkerpy.validators.one import NonEmpty

inp = ['foo', 'bar', 'egg']
mid = JustList(inp)
out = NonEmpty(mid)
```
You could also try to squeeze everything on one line.
```python
out = NonEmpty(JustList(inp, name='placeholders'), name='placeholders')
```
This, however is not only ugly but also has the drawback that the name of the
variable `inp`, specified in the inner call to `JustList` is not passed on to
the outer call of `NonEmpty` and, consequently, has to be specified again.

Fortunately, `CheckerPy` offers a more elegant way of achieving exactly the same
thing. All type and value checkers have a method `o`, whose name was chosen
to resemble the circular symbol used in mathematics to indicate the
_composition_ of two functions. To use it, simply type
```python
out = NonEmpty.o(JustList)(inp, name='placeholders')
```
Now,`inp` is piped first through `JustList` and then trough `NonEmpty` taking
the `name` argument with it. What's best, however, is that the functional
composition you get by combining two validators with the `o` method again
has an `o` method, thus allowing you to continue the chain indefinitely.
```python
from checkerpy.types.all import AllStr

out = AllStr.o(NonEmpty).o(JustList)(inp, 'placeholders')
```
Not only is the `name` argument piped through the whole chain, but also all
other keyword arguments you have encountered so far are piped through in the
same way. When calling, for example,
```python
from checkerpy.validators.all import AllLimited

out = AllLimited.o(AllStr).o(NonEmpty).o(JustList)(inp, lo='aaa', hi='zzz')
```
the keyword arguments `lo` and `hi` are passed all the way through to
`AllLimited`.

In order to further save you some typing, some useful functional compositions
are already attached to most validators as methods. The example above, for
instance, can also be written as:
```python
out = AllLimited.AllStr.NonEmpty.JustList(inp, lo='aaa', hi='zzz')
```

The same is true for the `numpy` validators. Provided you have imported
`JustInt64` from `checkerpy.types.numpy`, calling
```python
out = JustNdim(JustInt64(JustNdarray(a, 'again'), 'again'), 'again', ndim=1)
```
is equivalent to calling
```python
out = JustNdim.o(JustInt64).o(JustNdarray)(a, 'once', ndim=1)
```
and equivalent to calling
```python
out = JustNdim.JustInt64.JustNdarray(a, 'once', ndim=1)
```
Just use tab-completion to find out which validator-methods are already set
before you chain them using the `o` method.
### 5. Decorators <a name=chapter5></a>
For checking the values and types of function (or method) arguments, `CheckerPy`
provides two dedicated decorators.
```python
from checkerpy.decorators import Typed, Bounded
```

#### 5.1 Typed
There are two ways in which you can specify one or more types that each
argument of a function should have. The first is:
```python
@Typed(str, (int, float))
def show_age(name, age):
    print(f'{name} is {age} years old.')
```
Here, argument `name` is checked for being of type `str` and the type of
argument `age` must be either `int` or `float`.

**Note**: _Specifying `(int, float)` for the second argument does_ not
_mean that `age` must be a 2-tuple of an integer and a float!_

You can always specify more types in the decorator than there are arguments
to the function. The extra types at the end are simply ignored. Also, you
don't have to specify types for all arguments. In the example above, you might
be happy with just:
```python
@Typed(str)
def show_age(name, age):
    print(f'{name} is {age} years old.')
```
What, however, if you don't want to check the type of only the first, but only
of the _second_ argument? In that case, you can pass the types to check for
as _named_ arguments to the decorators using, of course, the name of the
argument to check.
```python
@Typed(age=(int, float))
def show_age(name, age):
    print(f'{name} is {age} years old.')
```
If you specify one or more type(s) with a name that is not among the arguments
of the function, it will be ignored. So, there is nothing wrong with:
```python
@Typed(name=str, age=(int, float), weight=float)
def show_age(name, age):
    print(f'{name} is {age} years old.')
```
Should a checked argument be of the wrong type, then _two_ errors are raised
and logged. Calling, for example, the function just defined as
```python
show_age('Terry Gilliam', age='None of your business')
```
will get you both a `WrongTypeError: Type of age must be int, not str like 
None of your business!` and a `WrongTypeError: An argument of function 
show_age defined in module __main__ is of wrong type!` raised and logged.

#### 5.2 Bounded
To check if one or more arguments of a function (or method) are above, below,
or outside given bounds, you can write
```python
@Bounded(('aaa', ...), (1, 99))
def show_age(name, age):
    print(f'{name} is {age} years old.')
```
Here, the argument `name` must be equal or greater than 'aaa' and `age` must
be anywhere between 1 and 99 (including the interval boundaries). The
ellipsis literal `...` is used to indicated the absence of a lower or upper
bound. As with the `Typed` decorator introduced above in subsection (5.1), you
can pass as many or as few limits to the decorator as you like, both named
and unnamed, but

**Note**: _Limits must strictly be given as_ tuples _of length 2!_

If a checked argument lies outside the specified bounds, then _two_ errors are
raised and logged. Calling, for example, the function just defined with,
```python
show_age('Methusalem', 120)
```
will get you both a `LimitError: Value 120 of age lies outside the allowed
interval [1, 99]!` and a `LimitError: An argument of function show_age defined
in module __main__ is out of bounds!` raised and logged. Likewise, calling
```python
show_age('Terry Gilliam', age='None of your business')
```
gets you both a `WrongTypeError: Cannot compare type str of age with limits of
types int and int!` and a `WrongTypeError: An argument of function show_age
defined in module __main__ cannot be compared with the corresponding limits!`
raised and logged.

#### 5.3 Methods vs. functions
Methods can be decorated just like functions provided, however, that their
first argument is called _self_, _cls_ , or _mcs_ (static methods are
obviously unaffected by this). If you insist on not sticking to this naming
convention, use named keyword arguments to specify types or bounds.

#### 5.4 Limitations
When using the decorators just introduced, be aware of the following
limitations:
1. The two decorators `Typed` and `Bounded` cannot be combined on the same
function or method.
2. `Typed` and `Bounded` should always be the _first_ decorators you apply to
a function or method, that is, they should be at the _lowest_ position,
directly above the function definition.
3. Optional _*args_ and _**kwargs_ are not checked.
