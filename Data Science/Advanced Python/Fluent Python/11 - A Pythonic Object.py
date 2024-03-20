# For a library or framework to be Pythonic is to make it as easy and natural as possible for a Python programmer to
# pick up how to perform a task

# ----------------------------------------------------------------------------------------------------------------------

# Object Representations
# Every OOP Language has at least one standard way of getting a string representation from any object. Python has:
"""
repr()
    Return a string representing the object as the developer wants to see it. It's what you get when the Python console
    or a debugger shows an object

str()
    Return a string representing the object as the user wants to see it. It's what you get when you print() an object

------------------------------------------------------------------------------------------------------------------------

bytes()
    Returns an object represented as a byte sequence

format()
    Returns a string displays of objects using special formatting codes
"""

# ----------------------------------------------------------------------------------------------------------------------

# Vector Class Redux

from array import array
import math


class Vector2d:
    typecode = 'd'  # it is a class attribute we'll use when converting Vector2d instances to/from bytes

    def __init__(self, x, y):
        self.x = float(x)  # To catch early errors
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y))  # Iter makes a Vector2d iterable; this is what makes unpacking work

    # e.g, x, y = my_vector. We implement it simply by using a generator expression to yield the components one after the other

    def __repr__(self):
        class_name = type(self).__name__
        if 'it\'s a boring way':
            return f'{class_name}({self.x!r}, {self.y!r})'
#       else:
#           return '{}({!r}, {!r}'.format(class_name, *self)

    def __str__(self):
        return str(tuple(self))  # From an iterable Vector2d, it's easy to build a tuple for display as an ordered pair

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +  # To generate bytes, we convert typecode to bytes and concatenate
                bytes(array(self.typecode, self)))  # bytes converted from an array built by iterating over the instance

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))


v1 = Vector2d(3, 4)
print(v1.x, v1.y)  # Components of
x, y = v1
print(x, y)
v1_clone = eval(repr(v1))  # Using eval here shows that the repr of a Vector2d can be is a faithful representation of
# its constructor call
print(v1_clone)

print(v1 == v1_clone, v1 is v1_clone)

print(bool(v1))

octets = bytes(v1)
print(octets)

print(bool(v1), bool(Vector2d(0, 0)))

# ----------------------------------------------------------------------------------------------------------------------

# An Alternative Constructor

"""
Since we can export a Vector2d as bytes, naturally we need a method that imports a Vector2d from a binary sequence.
Looking at the standard library for inspiration, we find that array.array has a class method named .frombytes that suits
our purpose. We adopt its name and use its functionality in a class method for Vector2d
"""


class Vector2d(Vector2d):
    @classmethod  # The classmethod decorator modifies a method, so it can be called directly on a class
    def frombytes(cls, octets):  # No self argument; instead, the class itself is passed as the first
        # argument - conventionally named cls
        typecode = chr(octets[0])  # Read the typecode from the first byte
        memv = memoryview(octets[1:]).cast(typecode)  # Create a memoryview from the octets binary sequence and use the
        # typecode to cast it
        return cls(
            *memv)  # Unpack the memoryview resulting from the cast into the pair of arguments needed for the constructor


a = Vector2d.frombytes(b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@')
print(a)


# ----------------------------------------------------------------------------------------------------------------------

# Classmethod Versus Staticmethod

# classmethod - to define a method that operates on the class and not on instances. classmethod changes the way the
# method is called, so it receives the class itself as the first argument, instead of an instance

# staticmethod - changes a method so that it receives no special first argument. In essence, a static method is just
# like a plain function that happens to live in a class body, instead of being defined at the module level

class Vector2d(Vector2d):
    @staticmethod
    def echo(word):
        print(word)


Vector2d.echo('Hello, world!')

print(1 / 4.82)
print(format(1 / 4.82, '0.4f'))

print(f'1BRL = {1 / 4.82:0.4f}')
print(format(2 / 3, '.1%'))

from datetime import datetime

now = datetime.now()
print(format(now, '%H:%M:%S'))
print('It\'s now {:%I:%M %p}'.format(now))

print(format(v1))


class Vector2d(Vector2d):
    def __format__(self, format_spec=''):
        components = (format(c, format_spec) for c in self)  # Use the format built-in to apply the format_spec to each
        # vector component, building an iterable of formatted strings
        return '({}, {})'.format(*components)  # Plug the formatted strings in the formula '(x, y)'


v2 = Vector2d(3, 4)
print(format(v2, '.2f'))


class Vector2d(Vector2d):
    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, format_spec=''):
        if format_spec.endswith('p'):  # Format ends with 'p': use polar coordinates
            format_spec = format_spec[:-1]  # Remove 'p' from format_spec
            coords = (abs(self), self.angle())  # (magnitude, angle)
            outer_fmt = '<{}, {}>'  # Configure outer format with angle brackets
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(*components)


v3 = Vector2d(3, 4)
print(format(v3, '.2fp'))


# ----------------------------------------------------------------------------------------------------------------------

# A Hashable Vector2d

class Vector2d(Vector2d):
    def __hash__(self):
        return hash((self.x, self.y))


v4 = Vector2d(3, 4)
print(hash(v4), Vector2d.__hash__(v3))


class Vector2d(Vector2d):
    def __float__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __int__(self):
        return int(float(self))

    def __complex__(self):
        return complex(self.x, self.y)


print(float(Vector2d(3, 2)))
print(complex(Vector2d(3, 1)))
print(int(Vector2d(4, 3)))

print(abs(Vector2d(3, 1)) == float(Vector2d(3, 1)))

class Vector2d(Vector2d):
    # Listing the instance attributes in the order they will be used for positional pattern matching
    __match_args__ = ('x', 'y')  #


def keyword_pattern_demo(v: Vector2d) -> None:
    match v:
        case Vector2d(0, 0):
            print(f'{v!r} is null')
        case Vector2d(0, _):
            print(f'{v!r} is vertical')
        case Vector2d(_, 0):
            print(f'{v!r} is horizontal')
        case Vector2d(x=c, y=cc) if c == cc:
            print(f'{v!r} is diagonal')
        case _:
            print(f'{v!r} is awesome!')


keyword_pattern_demo(Vector2d(0, 0))
keyword_pattern_demo(Vector2d(0, 1))
keyword_pattern_demo(Vector2d(1, 0))
keyword_pattern_demo(Vector2d(1, 1))
keyword_pattern_demo(Vector2d(2, 1))

print(Vector2d(0, 1).__dict__)

# ----------------------------------------------------------------------------------------------------------------------

# Private and "Protected" Attributes in Python

class Dog:
    def __init__(self, name, age):
        self._name = name  # This is a Protected attribute
        self.__age = age  # This is a Private attribute

dog1 = Dog('Bob', 18)
print(dog1._name)
# print(dog1.__age)  Will raise an error
dog1._name = 'Edik'
print(dog1.__dict__)

dog1._Dog__name = 'Hi'
print(dog1.__dict__)

"""
Never use two leading underscores. This is annoyingly private!
"""

# ----------------------------------------------------------------------------------------------------------------------

# Saving Memory with __slots__

# By default, Python stores the attributes of each instance in a dict named __dict__. The attributes named in __slots__
# are stored in a hidden array of references that use less memory than a dict.

class Pixel:
    __slots__ = ('x', 'y')

p = Pixel()
p.x = 1
p.y = 2
print(p.x, p.y)

class OpenPixel:
    pass

op = OpenPixel()
print(op.__dict__)
op.x = 8
print(op.__dict__)

print(op.x)
op.color = 'green'
print(op.__dict__)

class ColorPixel(Pixel):
    __slots__ = ('color', )

cp = ColorPixel()
cp.x = 2
cp.y = 4
cp.color = 'red'

# It's possible to save memory and "eat" it too. If you add the '__dict__' name to the __slots__ list, your instances
# will keep attributes named in __slots__ in the per-instance array of references, but will also support dynamically
# created attributes, which will be stored in the usual __dict__. This is necessary for the @cached_property operator

# ----------------------------------------------------------------------------------------------------------------------

# Overriding Class Attributes

# A distinctive feature of Python is how class attributes can be used as default values for instance attributes. We have
# typecode class attribute in Vector2d

v5 = Vector2d(1, 2)
dump_d = bytes(v5)
print(dump_d)

v5.typecode = 'f'
dump_f = bytes(v5)
print(dump_f)
