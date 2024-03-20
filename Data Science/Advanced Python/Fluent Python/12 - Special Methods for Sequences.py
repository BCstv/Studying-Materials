import operator
from array import array
import reprlib
import math

class VectorMD:

    typecode = 'd'

    def __init__(self, *args):
        self._components = array(self.typecode, [*args])

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        return f'VectorMD{str(tuple(self))}'

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


space1 = VectorMD(1, 2, 3, 4, 5)
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
        if isinstance(type(item), slice):  # If the argument is a slice
            cls = type(self)  # get the class of the instance (i.e., Vector...)
            return cls(*self._components[item])  # invoke the class to build another Vector instance from a slice of the _components array
        index = operator.index(item)  # If we can get an index from an item
        return self._components[index]  # return the specific item from _components

# The operator.index() function  calls the __index__ special method. The function and the special method were defined
# to be Used for Slicing to allow any of the numerous types of integers in NumPy to be Used






