# Variables Are Not Boxes

# Python variables are like reference variables, labels with names attached to objects.
a = [1, 2, 3]
b = a
a.append(4)
print(b)


# Therefore, the b = a statement does not copy the contents of box a into box b. It attaches the label b to the object
# that already has the label a

# The object has to be created before the assignment

class Gizmo:
    def __init__(self):
        print(f'Gizmo id: {id(self)}')


x = Gizmo()
# y = Gizmo() * 10
'''
    y = Gizmo() * 10
        ~~~~~~~~^~~~
TypeError: unsupported operand type(s) for *: 'Gizmo' and 'int'
'''

print(dir())  # [..., '__package__', '__spec__', 'a', 'b', 'x']
# The variable y was never created, because the exception happened while the right hand side of the assignment was being evaluated

# ----------------------------------------------------------------------------------------------------------------------

# Identity, Equality, and Aliases

charles = {'name': 'Charles L. Dodgson', 'born': 1832}
lewis = charles

print(lewis is charles)
print(id(charles), id(lewis))

lewis['balance'] = 950
print(charles)

alex = dict(charles)
print(alex)

print(alex == charles)
print(alex is charles)

# Syntactic sugar is f.e., a == b, while the method itself is a.__eq__(b)

# ----------------------------------------------------------------------------------------------------------------------

# Deep and Shallow Copies of Arbitrary Objects

import copy

print("Bus' class")


class Bus:
    def __init__(self, passengers: list = None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers

    def pick(self, name):
        return self.passengers.append(name)

    def drop(self, name):
        if name in self.passengers:
            self.passengers.remove(name)
        else:
            raise ValueError(f'{name[0].upper()} is not in {self.passengers}')


bus_149 = Bus(['Alice', 'Bob', 'Charlie'])

bus_221 = copy.copy(bus_149)
'''
A shallow copy creates a new object, but does not create new objects for the elements within the original object. 
In this case, it copies references to the same passenger objects.
'''
print(f'bus_221 == bus_149: {bus_221 is bus_149}')
print(f'bus_221.passengers == bus_149.passengers: {bus_221.passengers is bus_149.passengers}')
print(f'bus_221.passengers[0] == bus_149.passengers[0]: {bus_221.passengers[0] is bus_149.passengers[0]}\n')

bus_148 = copy.deepcopy(bus_149)
'''
A deep copy creates a completely new object and recursively copies all the objects referenced by the original object.
In this case, it creates new passenger objects for each passenger in bus_149.
'''
print(f'bus_148 == bus_149: {bus_148 is bus_149}')
print(f'bus_148.passengers == bus_149.passengers: {bus_148.passengers is bus_149.passengers}')
print(f'bus_148.passengers[0] == bus_149.passengers[0]: {bus_148.passengers[0] is bus_149.passengers[0]}\n')

bus_149.drop('Alice')
print(f'bus_149.passengers = {bus_149.passengers}')
print(f'bus_221.passengers = {bus_221.passengers}')
print(f'bus_148.passengers = {bus_148.passengers}\n')

bus_149.passengers[-1] += ' Ive just added it'
print(f'bus_149.passengers = {bus_149.passengers}')
print(f'bus_221.passengers = {bus_221.passengers}')
print(f'bus_148.passengers = {bus_148.passengers}\n')

bus_149.pick('Alesha')
print(f'bus_149.passengers = {bus_149.passengers}')
print(f'bus_221.passengers = {bus_221.passengers}')
print(f'bus_148.passengers = {bus_148.passengers}\n')

a = [10, 20]
b = [a, 30]
a.append(b)
print(a)


# ----------------------------------------------------------------------------------------------------------------------

# Functions Parameters as References

def foo(g, j):
    g += j
    return g


# A function may change any mutable object passed as a parameter, but it cannot change the identity of those objects
f, s = 1, 2
print(foo(f, s))
print(f, s)
print('Integer is unchanged!')

# It means that it cannot altogether replace an object with another!
lst_1, lst_2 = [1, 2], [3, 4]
print(foo(lst_1, lst_2))
print(lst_1, lst_2)
print('List is changed!')

tpl_1, tpl_2 = (1, 2), (3, 4)
print(foo(tpl_1, tpl_2))
print(tpl_1, tpl_2)
print('Tuple is unchanged!')


# ----------------------------------------------------------------------------------------------------------------------

# Mutable Types as Parameter Defaults: BAD IDEA
class HauntedBus:
    def __init__(self, passengers=[]):
        self.passengers = passengers
        # ^ A bad code.
        # The reason is - all variables created by this class will reference to the list object
        # A proper way for declaring mutable objects is below:


"""   def __init__(self, passengers=None):
        if passengers is None:
            passengers = list()
        self.passengers = list(passengers)"""  # = list(passengers) called as a defensive programming with mutable parameters

bus_1 = HauntedBus()
bus_2 = HauntedBus()

print(bus_1.passengers is bus_2.passengers)

bus_1.passengers.append(1)
print(bus_2.passengers)

# Even if we will pass different values to the self.passenger, they will share the same passenger list among themselves

# ----------------------------------------------------------------------------------------------------------------------
# THE MOST MISUNDERSTOOD PYTHON'S STATEMENT: del

# del and Garbage Collection

# Del deletes references, not objects!
"""
 Python's garbage collector may discard an object from memory as an indirect result of del, if the deleted variable was
 the last reference to the object. Rebinding a variable may also cause the number of references to an object to reach 
 zero, causing its destruction
"""

a = [1, 2]  # Create object [1, 2] and blind a to it
b = a  # Bind b to the same [1, 2] object
del a  # Delete reference a
print(b)  # [1, 2] was not affected, because b still points to it
b = [3]  # Rebinding b to a different object removes the last remaining reference to [1, 2]. So now the garbage
# collector discards an object

# Basically, the Python's garbage collector works, counting the reference to each object, and if it's 0 - discard it from the memory

import weakref
s1 = {1, 2, 3}
s2 = s1
def bye():
    print('...like tears in the rain.')

ender = weakref.finalize(s1, bye)  # weak references don't increment a reference counter to objects.
print(ender.alive)
s2 = 'something'

print(ender.alive)

# ----------------------------------------------------------------------------------------------------------------------
# P.E
# Tricks Python Plays with Immutables

t1 = (1, 2, 3)
t2 = tuple(t1)
print(t1 is t2)

t3 = t1[:]
print(t1 is t3)

# We can see such behavior with str, bytes, and frozenset

s1 = 'ABC'
s2 = 'ABC'
print(s2 is s1)

i1 = 19824
i2 = 19824

print(i1 is i2)

# The sharing of string literals is an optimization technique called interning.

# CPython uses a similar technique with small integers to avoid unnecessary duplication of numbers that appear
# frequently in programs like 0, 1, -1, etc.

# So object identity becomes important only when objects are mutable
