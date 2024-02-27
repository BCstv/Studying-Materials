# Type hints are the biggest change in the history of Python since the unification of types and classes in Python 2.2
import math


# However, type hints do not benefit all Python users equally. That's why they should always be optional
# They are a useful feature while static analysis (without actually running the code)

# The best usability feature of gradual typing is that annotations are always optional

# ----------------------------------------------------------------------------------------------------------------------

# Gradual Typing in Practice

def show_count(count: int, sp_word: str) -> str:
    return f'{'no' if count == 0 else count} {sp_word + 's' if count >= 2 or count == 0 else sp_word}'

print(show_count(0, 'bird'))

# Starting with MyPy

from pytest import mark

@mark.parametrize('qty, expected', [
    (1, '1 part'),
    (2, '2 parts')
])
def test_show_count(qty: int, expected: str) -> None:
    got = show_count(qty, 'part')
    assert got == expected

def test_show_count_zero():
    got = show_count(0, 'part')
    assert got == 'no parts'

def show_count(count: int, singular: str, plural: str = '') -> str:
    return (f'{'no' if count == 0 else count} '  # The count part
            f'{(singular + 's' if count >= 2 or count == 0 else singular) if plural == '' 
                else (plural if count >= 2 or count == 0 else singular)}')  # An updated word's part
del show_count
def test_irregular() -> None:
    got = show_count(2, 'child', 'children')
    assert got == '2 children'

# The following details are considered good style for type hints:

# * No space between the parameter name and the : ; one space after the :
# * Spaces on both sides of the = that precedes a default parameter value
# * PEP 8 says that there should be no space between = if there is no type hint
# plural=''
# plural: str = ''

# ----------------------------------------------------------------------------------------------------------------------

# Using None as a Default

from typing import Optional
# It's good practice to use the syntax from typing import X to reduce the length of the function signatures

def show_count(count: int, singular: str, plural: Optional[str] = None) -> str:
    return (f'{'no' if count == 0 else count} '  # The count part
            f'{(singular + 's' if count >= 2 or count == 0 else singular) if not plural 
                else (plural if count >= 2 or count == 0 else singular)}')  # An updated word's part

'''
Optional is not a great name, because that annotation does not make the parameter optional. What makes it optional is
assigning a default value to the parameter. Optional[str] just means: the type of this parameter may be !str or NoneType!
'''

# ----------------------------------------------------------------------------------------------------------------------

# Types Are Defined by Supported Operations

# for example, from the point of view of applicable operations, what are the valid types for x in the following function:

def double(x):
    return 2 * x

# The x parameter may be:
# numeric (int, complex, Fraction, numpy, uint32, etc.)
# sequence (str, tuple, list, array)
# N-dimensional (numpy.array)
# and many other type that implements or inherits a __mul__ method that accepts an int argument
del double


from collections import abc
def double(x: abc.Sequence):
    return x * 2
# A type checker reject that code. If you tell MyPy that x is of type abc.Sequence, it will flag x * 2 as an error because
# the Sequence does not implement or inherit the __mul__ method. At runtime, that code will work with concrete sequences
# such as str, tuple, list, array, etc., as well as numbers, because at runtime the type hints are ignored!

# In a gradual type system, we have the interplay if two different views of types:
'''
Duck typing
    The view adopted by SmallTalk - the pioneering object-oriented language - as well as Python, JavaScript, and Ruby.
    Objects have types, but variables (including parameters) are untyped. In practice, it doesn't matter what the 
    declared type of the object is only what operations it actually supports. If I can invoke birdie.quack(), then birdie
    is a duck in this context. By definition, duck typing is only enforces at runtime, when operations on objects are 
    attempted. This is more flexible than nominal typing, at the cost of allowing more errors at runtime.
'''

'''
Nominal Typing
    The view adopted by C++, Java, and C#, supported by annotated Python. Objects and variables have types. But objects
    only exist at runtime, and the type checker only cares about the source code where variables (including parameters)
    are annotated with type hints. If Duck is a subclass of Bird, you can assign a Duck instance to a parameter 
    annotated as birdie: Bird. But in the body of the function, the type checker considers the call birdie.quack() 
    illegal, because birdie is nominally a Bird and that class does not provide the .quack() method. It doesn't matter 
    if the actual argument at runtime is a Duck, because nominal typing is enforced statically. The type checker doesn't
    run any part of the program, it only reads the source code. This is more rigid than duck typing, with the advantage
    of catching some bugs earlier in a build pipeline, or even as the code is typed in an IDE 
'''

class Bird:
    pass

class Duck(Bird):  # Duck is a subclass of Bird
    def quack(self):
        print('Quack')

def alert(birdie):  # alert has no type hints, so the type checker ignores it
    birdie.quack()

def alert_duck(birdie: Duck) -> None:  # alert_duck takes one argument of type Duck
    birdie.quack()

def alert_bird(birdie: Bird) -> None:  # alert_bird takes one argument of type Bird
    birdie.quack()


daffy = Duck()
alert(daffy)  # Valid call, because alert has no type hints
alert_duck(daffy)  # Valid call, because alert_duck takes a Duck argument, and daffy is a Duck
alert_bird(daffy)  # Valid call, because alert_bird takes a Bird argument, and daffy is also a Bird - the superclass of Duck

woody = Bird()
# alert(woody)  # MyPy could not detect this error because there are no type hints in alert
# alert_duck(woody)  # MyPy reported the problem: Argument 1 to "alert_duck" has incompatible type "Bird"; expected "Duck"
# alert_bird(woody)  # MyPy has been telling us that the body of the alert_bird function is wrong: "Bird" has no attribute "quack"

# Every duck is a bird, but not every bird is a duck

# This little experiment shows that duck typing is easier to get started and is more flexible, but allows unsupported
# operations to cause errors at runtime. Nominal typing detects errors before runtime, but sometimes can reject code
# that actually runs (such as alert_bird(daffy))

# ----------------------------------------------------------------------------------------------------------------------

# Types Usable in Annotations

# The Any Type
from typing import Any
# The keystone of any gradual type system is the Any type, also known as the dynamic type
# When a type checker sees an untyped function like this:
del double
def double(x):
    return x * 2
del double

# It actually sees it like:
def double(x: Any) -> Any:
    return x * 2
del double

# Contrast Any with object, because every type is a subtype-of object
def double(x: object) -> object:
    return x * 2

# However, a type checker will reject this function, because an object does not support the __mul__ operation.
print(double('One'))

# ----------------------------------------------------------------------------------------------------------------------

# Optional and Union Types

# def show_count(count: int, singular: str, plural: Optional[str] = None) -> str:
# Optional[str] is actually a shortcut for Union[str, None]

"""
!!!
Since Python 3.10, we don't have to use optional/union.

Optional[str] -> str | None
Union[str, bytes, Union[int]] -> str | bytes | int 

!!!
"""

# ----------------------------------------------------------------------------------------------------------------------

# Generic Collections

# Most Python collections are heterogeneous. For example, you can put any mixture of different types in a list.
# However, in practice that's not very useful: if you put objects in a collection, you are likely to want to operate on
# them later, and usually this means they must share at least one common method

# It's written in the book that
lst: list[str] = ['one', 'two', 'three']
# Tells to the type checker that lst contains only str
del lst

# But I am somehow able to write this:
lst: list[str] = [1, 2, 3, '4']
print(lst)
# Hopefully, in Mojo this problem will disappear, because it's a strongly typed language

'''
The annotations stuff: list, and stuff: list[Any] are basically the same thing
'''

# The simplest form of a generic type is: container[item]

'''
* list              * set               * frozenset
* collections.deque * abc.Container     * abc.Collection
* abc.Sequence      * abc.Set           * abc.MutableSequence
                    * abc.MutableSet 
'''

# The tuple and mapping types support more complex type hints

# As of Python 3.10, there is no good way to annotate array.array, taking into account the typecode constructor argument

# ----------------------------------------------------------------------------------------------------------------------

# Tuple Types

# There are three ways to annotate tuple types

# 1 - Tuple as records
'''
If you're using a tuple as a record, use the tuple built-in and declare the types of the fields within []
'''
tpl: tuple[int, float, str] = (50, 35.6, 'Shanghai')

# 2 - Tuples as records with named fields
from typing import NamedTuple
from geolib import geohash as gh  # type: ignore
# This comment stops Mypy from reporting that the geolib package doesn't have type hints

PRECISION = 9
shanghai = 31.2304, 121.4737

class LatLon(NamedTuple):
    lat: float
    lon: float

type tLatLon = tuple[float, float]

def geohash(lat_lon: LatLon | tLatLon) -> str:
    return gh.encode(*lat_lon)

# 3 - Tuples as immutable sequences

'''
To annotate tuples of unspecified length that are used as immutable lists, you must specify a single type, followed 
by a comma and ...
'''

tis: tuple[int, ...] = (50, 1, 3, 1)
# tuple[Any, ...] -> tuple is the same thing (a tuple of an unspecified length with objects of any type)

# Here is a columnize function that transforms a sequence into a table of rows and cells in the form of a list of tuples
# with unspecified lengths
from collections.abc import Sequence
def columnize(sequence: Sequence[str], num_columns: int = 0) -> list[tuple[str, ...]]:
    if num_columns == 0:
        num_columns = round(len(sequence) ** 0.5)
    num_rows, reminder = divmod(len(sequence), num_columns)
    num_rows += bool(reminder)
    return [tuple(sequence[i::num_rows]) for i in range(num_rows)]


animals = 'drake fawn heron ibex koala lynx tiger xus yak zap'.split()
print(columnize(animals))
for row in columnize(animals):
    print(''.join(f'{word:10}' for word in row))

# ----------------------------------------------------------------------------------------------------------------------

# Generic Mappings

# Generic mapping types are annotated as MappingType[KeyType, ValueType]. The built-in dict and the mapping types in
# collections and collections.abc accept that notation in Python 3.9<=

import sys
import re
import unicodedata
from collections.abc import Iterator  # Iterator uses next

RE_WORD = re.compile(r'\w+')
STOP_CODE = sys.maxunicode + 1

def tokenize(text: str) -> Iterator[str]:  # Tokenize a generator function
    """return iterable of uppercased words"""
    for match in RE_WORD.finditer(text):
        yield match.group().upper()

# Given starting and ending Unicode character codes, name_index returns a dict[str, set[str]], which is an inverted
# index mapping each word to a set of characters that have that word in their names

type t_index = dict[str, set[str]]
def name_index(start: int = 32, end: int = STOP_CODE) -> t_index:
    index: t_index = {}  # Have to be declared with the type hint, because otherwise, MyPy will swear((
    for char in (chr(i) for i in range(start, end)):
        if name := unicodedata.name(char, ''):  # I used the walrus operator := in the if condition. It assigns the
            # the result of the unicodedata.name() call to name, and the whole expression evaluates to that result
            for word in tokenize(name):
                index.setdefault(word, set()).add(char)
    return index

index = name_index(32, 66)
print(index)
print(index['GREATER'])
print(index['DIGIT'] ^ (index['NINE'] | index['EIGHT']))


# Abstract Base Classes

from collections.abc import Mapping

# Using Mapping allows the caller to provide an instance of dict, defaultdict, ChainMap, a UserDict subclass or any
# other type that is a type

type color_map = Mapping[str, int]
color1_map: color_map = {'1': 1}


# ----------------------------------------------------------------------------------------------------------------------

# The fall of the numeric tower

from numbers import Number, Complex, Real, Rational, Integral  # In a decreasing order

# This tower is a linear hierarchy of ABCs, with Number at the top

# Those ABCs work perfectly well for runtime type checking, but they are not supported for static type checking

# If you want to annotate numeric arguments for static type checking, you have a few options:
'''
1. Use one of the concrete types int, float, or complex - as recommended by PEP 484
2. Declare a union type like Union[float, Decimal, Fraction] (since 3.9: float | Decimal | Fraction)
3. If you want to avoid hardcoding concrete types, use numeric protocols like SupportsFloat
'''

# ----------------------------------------------------------------------------------------------------------------------

# Iterable
from collections.abc import Iterable  # Iterable uses getitem

def zip_replace(text: str, changes: Iterable[tuple[str, str]]) -> str:
    for from_, to_ in changes:
        text = text.replace(from_, to_)
    return text

l33t: list[tuple[str, str]] = [('a', '4'), ('e', '3'), ('i', '1'), ('o', '0')]
text = 'mad skilled noob powned leet'

print(zip_replace(text, l33t))

# ----------------------------------------------------------------------------------------------------------------------

# abc.Iterable versus abc.Sequence

# zip_replace have to iterate over the entire Iterable arguments to return a result. Given an endless iterable such as
# the itertools.cycle generator as input, this function would consume all memory and crash the Python process. Despite
# this potential danger, it is fairly common in modern Python to offer functions that accept an Iterable input even if
# they must process it completely to return a result. That gives the caller the option of providing input data as a
# generator instead of a prebuilt sequence, potentially saving a lot of memory if the number of input item is large

# On other hand, the columnize function needs a Sequence parameter, and nit an Iterable, because it must get the len()
# of the input to compute the numbers of rows up front

# ----------------------------------------------------------------------------------------------------------------------

# Parameterized Generics and TypeVar
# PAGE 282














