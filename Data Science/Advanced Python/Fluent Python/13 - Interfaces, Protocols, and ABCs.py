# OOP is all about interfaces. The best approach to understanding a type in Python is knowing the methods it provides
# --it's interface--


"""
Duck typing
Python's default approach to typing from the beginning

Goose typing
The approach supported by ABCs, which relies on runtime checks of objects against ABCs

Static typing
The traditional approach of statically-typed languages like C and Java; supported since Python 3.5 by the typing module
and enforced by external type checkers.

Statick duck typing
An approach made popular by the Go language; supported by subclasses of typing.Protocol also enforced by external type checkers
"""
import builtins
from abc import ABC


class Vowels:
    def __getitem__(self, item):
        return 'AEIOU'[item]

# The getitem is not a protocol by itself, but it helps to implement the Sequence Protocol in Python

print(Vowels()[0])

for c in Vowels():
    print(c, end='')

print('\n','E' in Vowels())

# ----------------------------------------------------------------------------------------------------------------------

# Protocols

'''
Dynamic Protocol
    The informal protocols Python always had. Dynamic protocols are implicit, defined by convention, and described in 
    the documentation. Python's most important dynamic protocols are supported by the interpreter by itself.
Static Protocol
    Structural subtyping. Has an explicit definition: a typing.Protocol subclass
'''

# f.e., A sequence protocol has to implement such methods as: getitem, contains, iter, reversed, index, count

# There is no __iter__ method, yet Vowels instances are iterable because if Python finds a __getitem__ method, it tries
# to iterate over the object by calling that method with integer indexes starting with 0. So, basically, it doesn't have
# __iter__ and __contains__, but still, smart enough to make them (sequentially)

# ----------------------------------------------------------------------------------------------------------------------

# Monkey Patching

# It is a dynamically changing a module, class, or function at runtime, to add features or fix bugs

# print(len(Vowels()))  TypeError: object of type 'Vowels' has no len()
def length(vowels):
    return len(vowels[:])

Vowels.__len__ = length  # A monkey Patch

print(Vowels().__len__())

# ----------------------------------------------------------------------------------------------------------------------

# Goose Typing

# An abstract class represents an interface, @Bjarne Stroustrup

# Python doesn't have an interface keyword. We use ABCs to define interfaces for explicit type checking at runtime -
# also supported by static type checkers.

'''
    ABCs complement duck typing by providing a way to define interfaces when other techniques like hasattr() would be
    clumsy or subtly wrong (f.e., with dunder methods). ABCs introduce virtual subclasses, which are classes that don't
    inherit from a class but still recognized by isinstance() and issubclass()
'''

# Goose typing entails:

'''
* Subclassing from ABCs to make it explicit that you are implementing a previously defined interface
* Runtime type checking using ABCs instead of concrete classes as the second argument for isinstance and issubclass
'''

# ----------------------------------------------------------------------------------------------------------------------

# Subclassing an ABC

from collections.abc import MutableSequence
print(MutableSequence.__doc__)


print(builtins.classmethod.__new__.__doc__)

'''
Iterable, Container, Sized
    Every collection should either inherit from these ABCs or implement compatible protocols. Iterable supports 
    iteration with __iter, Container supports the in operator with __contains__, and Sized supports len() with __len__

Collection
    This ABC has no methods of its own, but was added in Python to make it easier to subclass from Iterable, Container, 
    and Sized

Sequence, Mapping, Set
    These are the main immutable collection types, and each has a mutable subclass.
    
MappingView
    In Python3, the objects returned from the mapping methods .items(), .keys(), .values() implement the interfaces 
    defined in ItemsView, KeysView, ValuesView respectively.

Callable, Hashable
    These are not collections, but collections.abc was the first package to define ABCs in the standard library, and 
    these two were deemed important enough to be included. They support type checking objects that must be callable or 
    hashable
'''

# ----------------------------------------------------------------------------------------------------------------------

# Defining and Using an ABC

'''
ABCs like descriptors and meta-classes, are tools for building frameworks. Therefore, only a small minority of Python 
developers can create ABCs without imposing unreasonable limitations and needless work on fellow programmers
'''

# Let's create a class named Tombola (a thingy which is loaded with balls in bingo)
'''
Abstract methods: 
    .load(...)
        Put items into the container
    .pick(...)
        Remove one item from the container and returning it

Concrete methods:
    .inspect()
        Return a tuple build from the items currently in the container, without changing its contents 
        
    .loaded()
        Returns True if there is something in the Tombola
'''
import abc
from collections.abc import Iterable
class Tombola(abc.ABC):  # to define an abstract class, subclass abc.ABC
    @abc.abstractmethod
    def load(self, iterable: Iterable) -> None:
        """
        Put items into the container
        :return: None
        """
    @abc.abstractmethod
    def pick(self) -> int:
        """
        Remove item at random, returning it

        It should raise an 'LookupError' when the instance is empty
        """

    def inspect(self):
        """Return a sorted tuple with the items currently inside"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return sorted(tuple(items))
        # Yeah, this code is silly, but it shows that we can relly on abstract methods

    def loaded(self):
        """Returns true if the Tombola has at least one item, otherwise - false """
        return bool(self.inspect())

class Fake(Tombola):
    def pick(self) -> int:
        return 13

# Fake() will raise a TypeError: Can't instantiate abstract class Fake without an implementation for abstract method 'load'

class MyABC(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def an_abstract_classmethod(cls, something):
        pass

    # When abstractmethod decorator is applied, it should be the closes decorator to the function

import random
class BingoCafe(Tombola):

    def load(self, iterable: Iterable) -> None:
        self._items.extend(iterable)
        self._randomizer.shuffle(self._items)  # Instead of the plain random.shuffle() function, we use the .shuffle() method

    def __init__(self, items):
        self._randomizer = random.SystemRandom()  # Pretend we'll use this for online gaming. random.SystemRandom()
        # implements the random API on top of the os.urandom function, which provides random bytes "suitable for
        # cryptographic use"
        self._items = []
        self.load(items)

    def pick(self) -> int:
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from an empty BingoCage')

    def __call__(self):
        return self.pick()

b = BingoCafe([41, 52, 13, 53, 61])
print(b.pick())
print(b.inspect())
print(b.loaded())
print(b())

class LotoBlower(Tombola):

    def __init__(self, iterable: Iterable) -> None:
        self._balls = list(iterable)

    def load(self, iterable: Iterable) -> None:
        self._balls.extend(iterable)

    def pick(self) -> int:
        size = len(self._balls)
        if size == 0:
            raise LookupError('pick from an empty LotoBlower')
        return self._balls.pop(random.randrange(size))

    def loaded(self):
        return bool(self._balls)

    def inspect(self):
        return tuple(self._balls)

l = LotoBlower([41, 13, 52, 12, 59])
print(l.inspect())
print(l.loaded())
print(l.pick())

# ----------------------------------------------------------------------------------------------------------------------

# A Virtual Subclass of an ABC

@Tombola.register  # We promise that it will behave like an ABC of Tombola
class TombolaList(list):
    def pick(self) -> int:
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pick from an empty TombolaList')

    load = list.extend  # TombolaList.load is the same as list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(self)


l = TombolaList([12, 25, 31, 4])
print(l.pick())
l.load([1, 2, 3])

print(issubclass(TombolaList, Tombola))
print(isinstance(l, Tombola))

# ----------------------------------------------------------------------------------------------------------------------

# Structural Typing with ABCs

class Sized(metaclass=abc.ABCMeta):
    __slots__ = ()

    @abc.abstractmethod
    def __len__(self):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Sized:
            if any("__len__" in B.__dict__ for B in C.__mro__):  # If there is an attribute named __len__ in the
                # __dict__ of any class listed in C.__mro__ and it's superclasses
                return True  # return True, signaling that C is a virtual subclass of Sized
        return NotImplemented


print(issubclass(list, Sized))

# ----------------------------------------------------------------------------------------------------------------------

# Static Protocols

from typing import TypeVar, Protocol
T = TypeVar('T')

class Repeatable(Protocol):
    def __mul__(self: T, repeat_count: int) -> T: ...

RT = TypeVar('RT', bound=Repeatable)

def double(x: RT) -> RT:
    return x*2

print(double(21))



