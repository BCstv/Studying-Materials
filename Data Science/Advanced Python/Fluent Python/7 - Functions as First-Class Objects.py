# Functions in Python are first-class objects.
# Programming language researchers define a "first-class object" as a program entity that can be
"""
* Created at runtime
* Assigned to a variable or element in a data structure
* Passed as an argument to a function
* Returned as the result of a function
"""
import builtins
import inspect
import operator


# Treating a Function Like an Object

def factorial(num):
    """returns n!"""
    return 1 if num < 2 else num * factorial(num-1)

print(factorial(10))
print(factorial.__doc__)
# The __doc__ attribute is used to generate the help text of an object.
# returns n!

print(type(factorial))
fact = factorial
print(fact)

mp = list(map(factorial, range(1, 11)))
print(mp)

# ----------------------------------------------------------------------------------------------------------------------

# Higher-Order Functions

# It's a function that takes a function as an argument or returns a function as the result
# One example is a map. Another is a sorted():

fruits = ['apple', 'banana', 'strawberry', 'fig', 'raspberry', 'cherry', 'pear', 'orange']
print(sorted(fruits, key=len))

def reverse(word):
    return word[::-1]

print(list(map(reverse, fruits)))

# ----------------------------------------------------------------------------------------------------------------------

# Modern Replacements for map, filter, and reduce

print(list(map(factorial, range(1, 6))))
print([factorial(i) for i in range(1, 6)])

print(list(map(factorial, filter(lambda n: n % 2 == 0, range(1, 7)))))
print([factorial(num) for num in range(1, 7) if num % 2 == 0])


from functools import reduce  # Starting with Python 3, reduce is no longer a built-in
from operator import add

print(reduce(add, range(1, 10)))
print(sum(range(1, 10)))

# ----------------------------------------------------------------------------------------------------------------------

# Anonymous Functions

# A lambda is an anonymous function
# It cannot use Python statements (while, try, =, e.t.c.)
print(sorted(fruits, key=lambda word: word[::-1]))

# DON'T MAKE YOUR LAMBDA FUNCTION TOO COMPLICATED!
# The lambda is just a syntactic sugar: a lambda expression created a function object just like the def statement.
# This is just one of several kinds of callable objects in Python!

# ----------------------------------------------------------------------------------------------------------------------

# The Nine Flavors of Callable Objects
'''
The call operator -()- may be applied to other objects besides functions.
To determine whether an object is callable - use the callable()
'''

# Nine callable types:
"""
* User-defined functions
    Created with def statements or lambda expressions
* Built-in functions
    A function implemented in C (for CPython), like len or time.strftime 
* Built-in methods
    Methods implemented in C, like dict.get
* Methods
    Functions defined in the body of a class
* Classes
    When invoked, a class runs its __new__ method to create an instance, then __init__ to initialize it, and finally the
    instance is returned to the caller. Because there is no new operator in Python, calling a class is like calling 
    a function
* Class instances
    If a class defines a __call__ method, then its instances may be invoked as functions.
* Generator functions
    Functions or methods that use the yield keyword in their body. When called, they return a generator object
* Native coroutine functions
    Functions or methods defined with async def. When called, they return a coroutine object
* Asynchronous generator functions
    Functions or methods defined with async def that have yield in their body. When called, they return an asynchronous
    generator for use with async for.
"""
print(abs, str, 'Hi!')
print([callable(obj) for obj in (abs, str, 'Hi!')])

# ----------------------------------------------------------------------------------------------------------------------

# User-Defined Callable Types

import random

class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            return LookupError('pick from empty BingoCafe')

    def __call__(self):
        return self.pick()

bingo = BingoCage(range(1, 3))
print(bingo.pick())
print(bingo())
print(bingo())
print(callable(bingo))

# A class implementing __call__ is an easy way to create function-like objects that have some internal state that must be
# kept across invocations, like the remaining items in the BingoCafe

# ----------------------------------------------------------------------------------------------------------------------

# From Positional to Keyword-Only Parameters

def tag(name, *content, class_='', **attrs):
    if class_ != '':
        attrs['class'] = class_
    attr_pairs = (f' {attr}="{value}"' for attr, value in sorted(attrs.items()))
    attr_str = ''.join(attr_pairs)
    if content:
        elements = (f'<{name}{attr_str}> {c} </{name}>'for c in content)
        return '\n'.join(elements)
    else:
        return f'<{name}{attr_str}/>'

print(tag('br'))  # A single positional argument produces an empty tag with that name

print(tag('p', 'hello'))  # Any number of arguments after the first are captures by *content as a tuple
print(tag('p', 'hello', 'world'))

print(tag('p', 'hello', id=33))  # keyword arguments not explicitly named in the tag signature are captured by **attrs as dict

print(tag('p', ('hello', 'world'), class_='sidebar'))  # The class_ parameter can only be passed as a keyword argument

print(tag(content='testing', name='img'))  # The first positional argument can also be passed as a keyword

my_tag = {'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'class_': 'framed'}
print(tag('img', 'Hello, world!', **my_tag))

# ----------------------------------------------------------------------------------------------------------------------

# Positional-Only Parameters

# Since Python 3.8, user-defined function signatures may specify positional-only parameters. This feature always existed
# for built-in functions, such as divmod(a, b), which can only be called with positional parameters, and not as
# divmod(a=10, b=4)

# To define a positional-only function, use / in the parameter list.

# divmod(__y=2, __x=2)
'''
    divmod(__y=2, __x=2)
TypeError: divmod() takes no keyword arguments
'''

def divmod(x, y, /):
    return builtins.divmod(x, y)

print(divmod(1, 3))

# def tag(name, /, *content, class_=None, **attrs)
#               ^ If we want the name parameter to be positional only

from operator import mul, itemgetter
# The operator module provides functions equivalents for dozens of operators so you don't have to code trivial functions
# mul = lambda x, y: x*y
def factorial(num):
    return reduce(mul, range(1, num + 1))

metro_data = [
    ('Beijing', 'CN', 41.1, (-23.2397253, -46.8935983)),
    ('Odessa', 'UA', 0.9, (50.2317253, -1.8952983)),
    ('Moscow', 'RU', 13.6, (-36.1085353, 15.9835983)),
    ('Beijing', 'CN', 41.1, (98.2397253, -6.8935983))
]

for city in sorted(metro_data, key=itemgetter(1)):  # for lambda x: x[1]
    print(city)

cc_name = itemgetter(1, 0)

for city in metro_data:
    print(cc_name(city))  # returns the positions 1 and 0

# cause itemgetter uses the __getitem__ ([]) dunder method, it means that it can be provided with maps (and any other
# class, which supports __getitem__)

from collections import namedtuple
LatLon = namedtuple('LatLon', 'lat lon')  # Use namedtuple to define LatLon
Metropolis = namedtuple('Metropolis', 'name cc pop coord')  # And also Metropolis
metro_areas = [Metropolis(name, cc, pop, LatLon(lat, lon))
               for name, cc, pop, (lat, lon) in metro_data]  # Build metro_areas list with Metropolis instances;
# note the nested tuple unpacking to extract (lat, lon) and use them to build the LatLon for the coord attribute of Metropolis

print(metro_areas[0])
print(metro_areas[0].coord.lat)  # Reach into element metro_areas[0] to get its latitude

from operator import attrgetter
name_lat = attrgetter('name', 'coord.lat')  # Define an attrgetter to retrieve the name and the coord.lat nested attribute

for city in sorted(metro_areas, key=attrgetter('coord.lat')):  # Use attrgetter again to sort list of cities by latitude
    print(name_lat(city))  # Use the attrgetter defined in name_lat to show only the city name and latitude

print([name for name in dir(operator) if not name.startswith('_')])

from operator import methodcaller
s = 'The time has come'
upcase = methodcaller('upper')
print(upcase(s))

hyphenate = methodcaller('replace', ' ', '-')
print(hyphenate(s))

# ----------------------------------------------------------------------------------------------------------------------

# Freezing Arguments with functools.partial

from functools import partial
# This is useful to adapt a function that takes one or more arguments to an API that requires a callback with fewer arguments

triple = partial(mul, 3)  # Create a new triple function from mul, binding the first positional argument to 3

print(triple(7))
print(list(map(triple, range(1, 10))))

# Partial takes a callable as first argument, followed by an arbitrary number of positional and keyword arguments to bind

picture = partial(tag, 'img', class_='pic-frame')
# Create the picture function from tag by fixing the first positional argument with 'img' and the class_ keyword
# argument with 'pic-frame'

print(picture)
print(picture(src='wumpus.jpeg'))
# A partial object has attributes providing access to the original function and the fixed arguments

print(picture.args)
print(picture.keywords)

# Python is not, by design, a functional language-whatever that means. Python just borrows a few good ideas from
# functional languages
