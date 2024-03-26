import operator
from array import array
import reprlib
import math
import functools

class VectorMD:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return f'VectorMD({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(*self)

    def __bool__(self):
        return bool(abs(*self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, item):
        return self._components[item]

    @classmethod
    def from_bytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)


space1 = VectorMD([1, 2, 3, 4, 5])
print(space1.__repr__())
space2 = eval(space1.__repr__())

print(space2 == space1)


# How slicing works

class MySeq:
    def __getitem__(self, item):
        return item


s = MySeq()
print(s[1])
print(s[1:4:2, 7:9])

print(dir(slice))

an_arr = [i for i in range(0, 5)]
print(an_arr)

# S.indices(len) can convert the slicer for different iterable lengths
print(slice(None, 10, 2).indices(10))
print(an_arr[:10:2])
print(an_arr[0:5:2])

print(slice(-3, None, None).indices(10))
print(an_arr[-3:])
print(an_arr[2:5:1])


class VectorMD(VectorMD):
    def __len__(self):
        return len(self._components)

    def __getitem__(self, item):
        if isinstance(item, slice):  # If the argument is a slice
            cls = type(self)  # get the class of the instance (i.e., Vector...)
            return cls(self._components[
                           item])  # invoke the class to build another Vector instance from a slice of the _components array
        index = operator.index(item)  # If we can get an index from an item
        return self._components[index]  # return the specific item from _components


# The operator.index() function  calls the __index__ special method. The function and the special method were defined
# to be Used for Slicing to allow any of the numerous types of integers in NumPy to be Used.
# The key difference between .index and int() is that the former is intended for this specific purpose.

try:
    operator.index(0.5)
except TypeError as e:
    print(e)

v7 = VectorMD(range(7))
print(v7[-1].__repr__())  # An integer index retrieves just one component value as a float
print(v7[1:4].__repr__())  # A slice index creates a new Vector
print(v7[-1:].__repr__())  # A slice of length 1 also creates a Vector

v8 = VectorMD(range(10))


class VectorMD(VectorMD):
    __match_args__ = ('x', 'y', 'z', 't')

    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        msg = f'{cls.__name__!r} object has no attribute {name!r}'
        raise AttributeError(msg)


v9 = VectorMD(range(1, 10))
print(v9.__repr__())

# Let's make an experiment:
print(v9[0], v9.x, '=', v9[0] is v9.x)
# And so now out experiment is finished.
# Kidding
v9.x = 10
print(v9.__repr__())
print(v9.x)


class VectorMD(VectorMD):
    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:  # Special handling for single-character attribute names
            if name in cls.__match_args__:  # if name is one of __match_args__, set specific error message
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():  # if name is lowercase, set error message about all single-letter names
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:  # if there is a non-blank error, raise attribute error
                msg = error.format(attr_name=name, cls_name=cls.__name__)
                raise AttributeError(msg)
        super().__setattr__(name, value)  # Default case: call __setattr__ on superclass for standard behaviour


v10 = VectorMD(range(1, 10))
print(v10.__repr__())
print(v10[0], v10.x, '=', v10[0] is v10.x)
v10.X = 2
print(v10.__repr__())

# Hashing and a Faster ==

print(functools.reduce(lambda a, b: a * b, range(1, 6)))
# Will look like this: ((((1*2)*3)*4)*5)

class VectorMD(VectorMD):
    def __eq__(self, other):
        return tuple(self), other(self)

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

v11 = VectorMD(range(1, 6))
print(hash(v11))

# map is a lazy operator. It creates a generator that yields the result on demand, thus saving memory

hi = list(map(lambda x, y: (x, y), [1, 2, 3], list(map(lambda x: x*2, [1, 2, 3]))))
print(hi)

print(list(zip(range(1, 4), range(3, 6))))
b = [(1, 2),
     (3, 4),
     (5, 6)]

print(list(zip(*b)))