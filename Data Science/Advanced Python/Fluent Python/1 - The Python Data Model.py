# The Python interpreter invokes special methods to perform basic object operations, often triggered by special syntax
# The special method names are always written with leading and trailing double underscore.
# For example:

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]

_ = lst.__getitem__(0) == lst[0]  # collection.__getitem__(key) == collection[key]
print(_)

# We implement special methods when we want our objects to support and interact with fundamental language constructs.
# Such as:
'''
* Collections
* Attribute access
* Iteration (Including asynchronous iteration using async for)
* Operator overloading
* Function and method invocation
* String representation and formatting
* Asynchronous programming using await
* Object creation and destruction
* Managed contexts using the with async with statements
'''

# P.S. Special methods are usually called magic or dunder (double underscore before and after) methods

# ----------------------------------------------------------------------------------------------------

# A pythonic Card Deck
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks
                       for suit in self.suits]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


beer_card = Card('7', 'diamonds')
print(beer_card)

deck = FrenchDeck()
print(len(deck))

print(deck.__getitem__(51), '=', deck[51])

print(deck[:4])

from random import choice

print(choice(deck))

for card in reversed(deck):
    print(card)

print(Card(rank='A', suit='poop') in deck)
print(Card(rank='2', suit='clubs') in deck)

print(deck._cards.index(Card('A', 'diamonds')))

# We've just seen two advantages of using special methods to leverage the Python Data Model:
# 1 - Users of your classes don't have to memorize arbitrary method names for standard operations
#     ("How to get the number of items? Is it .size(), .length(), or what?")
# 2 - It's easier to benefit from the rich Python standard library and avoid reinventing the wheel!

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


for card in sorted(deck, key=spades_high):
    print(card)

l = [12, 32, '1', 14, '38', '17', 17]
print(sorted(l, key=int, reverse=True))


# Normally, your code should not have many direct calls to special methods. Unless you are doing a lot of
# metaprogramming, you should be implementing special methods more often than invoking them explicitly

# -------------------------------------------------------------------------------------------------------

# Emulating Numeric Types

import math


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x!r}, {self.y!r})'  # !r is used here to get the standard representation of the attributes to be displayed.
        # It shows the difference between Vector('x', 'y') and Vector(x, y)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))
    # Another way of how to implement a bool dunder method is:
    '''
    def __bool__(self):
        return bool(self.x or self.y)
    '''
    # This is harder to read, but it avoids a trip through abs method

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


v1 = Vector(1, 5)
v2 = Vector(3, 4)

print(v1 + v2)
print(v1 * 10)
print(abs(v1))
print(bool(v1))

# -----------------------------------------------------------------------------------

# String Representation

# The __repr__ special method is called by the repr built-in to get the string representation of the object for inspection
# Without a custom __repr__, Python's console would display a Vector instance as <Vector object at 0x23e232552>

x = 'Programming is fun!'
print(str(x))

y = "But sometimes it's weird"
print(repr(y))

# So basically the main difference between str and repr is that str creates a user-friendly string variable, while repr
# Creates a reusable representation of class' variables with which we can later recreate an object

# P.S. Programmers usually prefer __str__ dunder method, but it's better to use __repr__

# ----------------------------------------------------------------------------------------------------------------------

# Boolean Value of a Custom Type

# By default, instances of user-defined classes are considered truthy, unless either __bool__ or __len__
# is implemented. Basically, bool(x) calls x.__bool__() and uses the result. If __bool__ is not implemented, Python tries
# to invoke x.__len__(), and if that returns zero, bool returns False. Otherwise, bool returns True

# ----------------------------------------------------------------------------------------------------------------------
# Special method names

'''
Category                                         __Method name__

String/bytes representation                      repr, str, format, bytes, fspath
Conversion to number                             bool, complex, int, float, hash, index
Emulating collections                            len, getitem, setitem, delitem, contains
Iteration                                        iter, aiter, next, reversed
Callable or coroutine execution                  call, await
Context management                               enter, exit, aexit, aenter
Instance creation and destruction                new, init, del
Attribute management                             getattr, getattribute, setattr, delattr, dir
Attribute descriptors                            get, set, delete, set_name
Abstract base classes                            instancecheck, subclasscheck
Class metaprogramming                            prepare, init_subclass, class_getitem, mro_entries
'''

# Special method names and symbols for operators
'''
Operator Category           Symbols                   __Method name__

Unary metric                -, +, abs()               neg, pos, abs
Rich comparison             <, <=, ==, !=, >, >=      lt, le, eq, ne, gt, ge
Arithmetic                  +, -, *, /, //, %, @,     add, sub, mul, truediv, floordiv, mod, matmul 
                            divmod(), round(), **     divmod, round, pow
                            pow()
Reversed arithmetic         All the same, but operands are reversed (10 - 5 => 5 - 10) etc
Augmented assignment        +=, -=, *=, /=, //= %=,   iadd, isub, imul, itruediv, ifloordiv, imod,
arithmetic                  @=, **=                   imatmul, ipow
Bitwise                     &, |, ^, <<, >>, ~        and, or, xor, lshift, rshift, invert
Reversed bitwise            (bitwise operators with   rand, ror, rxor, rlshift, rshift
                            swapped operands)
Augmented assignment        &=, |=, ^=, <<=, >>=      iand, ior, ixor, ilshift, irshift
bitwise 
'''

# ----------------------------------------------------------------------------------------------------------------------

# Why len is not a method

# Len is not called as a method because it gets special treatment as part of the Python Data Model, just like abs.
# but thanks to the special method __len__, you can also make len work with your own custom objects
