# Overview of a Built-In Sequences:

# Container Sequences:
#   Can hold items of different types, including nested containers(list, tuple, collections.deque)

# Flat Sequences:
#   Hold items of one simple type(str, bytes, array.array)

# A container sequence holds references to the objects it contains, which may be of any type, while a flat sequence
# stores the value of its contents in its own memory space, not as distinct Python objects

# Every python object in memory has a header with metadata. F.e. a float:
# * ob_refcnt: the object's reference count
# * ob_type: a pointer to object's count
# * ob_fval: a C double holding the value of the float

# In 64- bit python, each of those headers takes 8 bytes

# ----------------------------------------------------------------------------------------------------------------------

# A list comprehensions and readability

print([ord(x) for x in '#$(*%#'])
codes = [last := ord(c) for c in 'ABC']
print(codes, last)

# Listcomps vs map and filter

symbols = ')@~#¥*!'
beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
print(beyond_ascii)

beyond_ascii = [ord(c) for c in symbols if ord(c) > 127]
print(beyond_ascii)

# Listcomps do everything the map and filter functions do, without the contortions of the functionally challenged lambda

# ----------------------------------------------------------------------------------------------------------------------

# Cartesian Products

colors = ['red', 'green', 'blue']
sizes = ['small', 'medium', 'large']

print([(color, size) for color in colors
       for size in sizes])  # It generates a list of tuples arranged by color, then size
print([(color, size) for size in sizes
       for color in colors])  # Does the opposite thing

# ----------------------------------------------------------------------------------------------------------------------

# Generator Expressions (genexp)
print(tuple(ord(symbol) for symbol in symbols))
# Genexps use the same syntax as listcomps, but are enclosed in parentheses rather than brackets
for tshirt in (f'{c}, {s}' for c in colors for s in sizes):
    print(tshirt)
# The generator expression yields items one by one;
# a list with all six T-shirts variations is never produced in this example

# ----------------------------------------------------------------------------------------------------------------------

# Tuples are not just Immutable Lists

# Tuples do double duty: they can be used as immutable lists and also as records with no field names

# Tuples as records:
a = ('Tokyo', 2003, 32_450, 0.66, 8014)
print(a + (4,))
city, year, pop, chg, area = a
print(city, area)

traveler_ids = [('USA', '129842945'), ('BRA', '745234964'), ('ESP', '239233469')]

for passport in sorted(traveler_ids, key=lambda x: x[1]):
    print('%s (%s)' % passport)  # The % formatting understands tuples and treats each item as a separate field

for country, _ in traveler_ids:
    print(country)

# Tuples as immutable lists:
# Clarity - When you see a tuple in code, you know its length will never change
# Performance - A tuple uses less memory than a list of the same length, and it allows Python to do some optimizations

# ----------------------------------------------------------------------------------------------------------------------

# Comparing Tuple and List Methods

'''
Method                            list   tuple           Clarifications

s.__add__(s2)                       *      *             s + s2 - concatenation
s.__iadd__(s2)                      *                    s += 2 - in-place concatenation
s.append(e)                         *                    Append one element after last
s.clear()                           *                    Clear all elements
s.__contains__(e)                   *      *             Check if e in s
s.copy()                            *                    Shallow copy of the list
s.count(e)                          *      *             Count occurrences of an e
s.__delitem__(i)                    *                    Remove item at index i
s.extend(it)                        *                    Append items from iterable it
s.__getitem__(p)                    *      *             Get item at index p
s.__getnewargs__()                         *             Support for optimized serialization with pickle
s.index(e)                          *      *             Find position of first occurrence of e
s.insert(p, e)                      *                    Insert element e before the item at position p
s.__iter__()                        *      *             Get iterator
s.__len__()                         *      *             len(s) - number of items
s.__mul__(n)                        *      *             s * n - repeated concatenation
s.__imul__(n)                       *                    s *= n - in-place repeated concatenation
s.pop([p])                          *                    Remove and return last item or item at optional position p
s.remove(e)                         *                    Remove first occurrence of element e by value
s.reverse()                         *                    Reverse the order of the items in place
s.__reversed__()                    *                    Get iterator to scan items from last to first
s.__setitem__(p, e)                 *                    s[p] = e - put e in position p, overwriting existing element
s.sort([key], [reverse])            *                    Sort items in place with optional keyword arguments key and reverse
'''

# ----------------------------------------------------------------------------------------------------------------------

# Unpacking Sequences and Iterables

x = (1, 2)
a, b = x
b, a = a, b  # An elegant application of unpacking is swapping the values of variables without using a temporary variable
print(b)

t = (20, 8)
quotient, remainder = divmod(*t)
print(quotient, remainder)
# Another example of unpacking is prefixing an argument with * when calling a function

# Using * to Grab Excess Items
f, s, *rest = range(1, 6)
print(f, s, rest)
f, s, *rest = range(1, 4)
print(f, s, rest)
f, s, *rest = range(1, 3)
print(f, s, rest)
f, *body, l = range(1, 6)
print(f, body, l)


# Unpacking with * in function calls and sequence literals
def fun(a, b, c, d, *rest):
    return a, b, c, d, rest


print(fun(*[1, 2], 3, *range(4, 7)))
print(*range(4), 4, *(5, 6, 7))

# Nested Unpacking
metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.1242, 139.182459)),
    ('Delhi NCR', 'IN', 21.395, (28.681392, 77.289354)),
    ('Mexico City', 'MX', 20.142, (19.293757, -99.139282))
]


def unpacker(metro):
    print(f'{"-"*16}| {"latitude":>9} | {"longitude":>9} |')
    for name, _, _, (lat, lon) in metro:
        print(f'{name:15} | {lat:9.4f} | {lon:9.4f} |')


unpacker(metro_areas)

# Slicing
s = 'bicycle'
print(s[::3])
b = slice(5, 6)
print(s[b])

z = slice(0, 7, 2)
print(s[z])

# Assigning to Slices
l = list(range(1, 11))
print(l)

l[2:4] = (1,3)
print(l)

del l[-3:-1]
print(l)

l[2::4] = (11, 22)
print(l)

# ----------------------------------------------------------------------------------------------------------------------

# Building lists of lists

board = [['_'] * 3 for i in range(3)]
board[1][1] = 'X'
print(board)

weird_board = [['_']*3]*3  # The outer list is made of three references to the same inner list
weird_board[2][1] = '0'
print(weird_board)

# ----------------------------------------------------------------------------------------------------------------------

# Deques and Other Queues

from collections import deque
dq = deque(range(1, 11), maxlen=10)
dq += [1, 4, 3, 2]
print(dq)

dq.rotate(2)
print(dq)

# maxlen is an optional value
# deque can do appendleft(), __copy__()(shallow copy), extendleft(), popleft(), rotate(n)
