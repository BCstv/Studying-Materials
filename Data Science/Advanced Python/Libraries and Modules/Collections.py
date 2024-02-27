# ----------------------------------------------------------------------------------------------------------------------
#                                                Collections
# ----------------------------------------------------------------------------------------------------------------------
"""
Python has 4 built-in data structures:
    * Lists [1, 2, 3, 4]
    * Tuples (1, 2, 3, 4)
    * Dictionaries {1: 'one', 2: 'two', 3: 'three'}
    * Sets {1, 2, 3, 4}
"""

# ----------------------------------------------------------------------------------------------------------------------

from collections import namedtuple  # (typename, field_names, *, rename=False, defaults=None, module=None)

"""
Factory function for creating tuple subclasses with named fields

Returns a new tuple subclass named typename. The new subclass is used to create tuple-like objects that have fields 
accessible by attribute lookup as well as being indexable and iterable. Instances of the subclass also have a helpful 
docstring (with typename and field_names) and a helpful __repr__() method which lists the tuple contents in a name=value
format.
"""

# Pre-defined dunder methods:
'''
['__annotations__', '__builtins__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', 
'__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__getstate__', 
'__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', 
'__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
 '__sizeof__', '__str__', '__subclasshook__', '__type_params__']
'''

humaninfo = namedtuple('HumanInfo', ['age', 'name', 'sex'])
stas = humaninfo(20, 'Stas', 'M')
katya = humaninfo(18, sex='W', name='Katya')
print(stas, katya)

# If rename is True - invalid fieldnames are automatically replaced with positional names
lildataset = namedtuple('Data', ['age', 'age', 'age', 'likes()', 'def', 'class', 'pets'], rename=True)
data_1 = lildataset(19, 10, 15, 'MJ', _4='Loves anime', _5='Middle', pets='Dogs')
# Data(age=19, _1=10, _2=15, _3='MJ', _4='Loves anime', _5='Middle', pets='Dogs')
print(data_1)

# If rename=False, then:
# ValueError: Type names and field names cannot be a keyword: 'def'
# Because you can't use class, for, return, global, pass, or raise. Also you can't put brackets after the field name

# ValueError: Encountered duplicate field name: 'age'
print(data_1._1, data_1._2, data_1.pets)

# If Default=some_iter
coordinates = namedtuple('Coordinates', ['x', 'y', 'z', 'd'], defaults=(0, 0))
# The last 2 values (in this case) will be equal to defaults iterable
circle_center = coordinates(y=1, x=1)
rectangle_center = coordinates(2, 3, d=4)

print(circle_center)
print(rectangle_center)

print(circle_center + rectangle_center)  # Eh \;

# If module = string
# the __module__ attribute of the named tuple is set to that value

coordinates = namedtuple('Coordinates', ['x', 'y', 'z', 'd'], module='geometry')
print(coordinates(x=1, y=2, z=3, d=4).__module__)

# NamedTuples are light weighted and don't require a lot of memory

# Use cases

coordinates = namedtuple('Coordinates', ['x', 'y', 'z', 'd'], rename=True, defaults=(1, 2, 3, 4),
                         module='4D calculations')

object_1 = coordinates(1, 3)
print(object_1)
print(object_1.x + object_1.y)

# object_1[0] += object_1[1] is impossible, because named tuples are immutable

object_2 = coordinates(5, 12)
first, second = object_2[:2]
print(first, second)

first, second, third, fourth = object_2
print(first, second, third, fourth)

EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade', defaults=(0,))

book = EmployeeRecord._make(['Stas', '18', 'War', 'UNE', '20$'])
print(book)

print(book._asdict())

book = book._replace(age='19')
print(book)

print(book._fields)
print(book._field_defaults)
print(getattr(book, 'age'))

new_arrival = {'name': 'Katya', 'age': '16', 'title': 'Peace', 'department': book.department, 'paygrade': '21.99$'}
book_1 = EmployeeRecord(**new_arrival)
print(book_1)


# Since a named tuple is a regular Python class, it is easy to add or change functionality with a subclass. Here is how
# to add a calculated field and a fixed-width print format:

class Point(namedtuple('Point', ['x', 'y'])):
    __slots__ = ()

    @property
    def hypot(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self):
        return f'Point: {self.x:.3f}  {self.y:.3f}  {self.hypot:.3f}'


for p in (Point(3, 4), Point(14, 5 / 7)):
    print(p)

Point3D = namedtuple('Point3D', [*Point._fields, 'z'])

print(Point3D._fields)

Point3D.__doc__ += ': Allows to store points in 3D space'
Point3D.x.__doc__ = 'x coordinate'
Point3D.y.__doc__ = 'y coordinate'
Point3D.z.__doc__ = 'z coordinate'

print(Point3D.__doc__)
print(Point3D.x.__doc__)

# ----------------------------------------------------------------------------------------------------------------------

from collections import deque

# | <-> ||||| <-> |

# Methods:

names = deque(['John', 'Stas', 'Katya', 'Jacob'])

# 1. append(x) -> Add x to the right side of the deque
names.append('Jessica')

# 2. appendleft(x) -> Add x to the left side of the deque
names.appendleft('Igor')
print(names)
print(list(names))

# 3. copy() -> create a shallow copy of the deque
names_1 = names.copy()

# 4. clear() -> Clear the deque => length = 0
names.clear()
print(names)
print(list(names_1))

# 5. count(x) -> Count the number of deque elements equal to x
print(names_1.count('Stas'))

# 6. extend(iterable) -> Extend the right side of the deque by appending elements from the iterable argument
names_1.extend((['Stas']))
print(names_1)

# 7. extendleft(iterable) -> Extend the left side of the deque by appending elements from the iterable
names_1.extendleft(['Lewis', 'Hello', 'I was third'])  # It also reverses the given iterable
print(names_1)

# 8. index[x[, start[, stop]]) - Return the position of x in the deque (at or after index start and before index stop).
#    Returns the first match or raises ValueError if not found
print(names_1.index('Lewis'))
print(names_1.index('Lewis', 0, 4))

# 9. insert(i, x) -> Insert x into the deque at position i
print(names_1, end=' -> ')
names_1.insert(1, 'I was entered')
print(names_1)

# 10. pop() -> Remove and return an element from the right side of deque
names_1.pop()
print(names_1)


# 11. popleft() -> Remove and return an element from the left side of deque
names_1.popleft()
print(names_1)

# 12. remove(x) -> Remove the first occurrence of value
names_1.remove('Stas')
print(names_1)

# 13. reverse() -> Reverse the elements of the deque in-place and then return None
names_1.reverse()
print(names_1)

# 14. rotate(n=1) -> Rotate the deque n steps to the right. If n = negative - rotate to the left
names_1.rotate(2)
print(names_1)

# An only-read attribute - maxlen
# For fast random access, use lists instead.

def tail(filename, n=10):
    """Return the last n lines of a file"""
    with open(filename) as f:
        return deque(f, n)

# ----------------------------------------------------------------------------------------------------------------------

from collections import ChainMap

# A ChainMap groups multiple dicts or their mappings together to create a single, updatable view. If no maps are
# specified, a single empty dictionary is provided so that a new chain always has at least on mapping

# Define multiple dictionaries
default_settings = {'debug': False, 'logging_level': 'INFO'}
user_settings = {'debug': True, 'username': 'user123'}

# Create a ChainMap combining the dictionaries
settings: ChainMap = ChainMap(user_settings, default_settings)

# Access values in the ChainMap
print(settings['debug'])  # Output: True (user_settings overrides default_settings)
print(settings['logging_level'])  # Output: INFO (default_settings value)

# Update values in the ChainMap
settings['logging_level'] = 'DEBUG'
print(settings['logging_level'])  # Output: DEBUG (updated value)

# Add a new key-value pair
settings['timeout'] = 30
print(settings)  # Output: 30 (new key-value pair)
print(user_settings)


print(settings.maps)

print(settings['debug'])
settings = ChainMap(settings.maps[1], settings.maps[0])
print(settings['debug'])

print(ChainMap(locals(), globals(), vars()))

# ----------------------------------------------------------------------------------------------------------------------

from collections import Counter

print(Counter(['red', 'blue', 'red', 'green', 'blue', 'blue']).most_common(3))

# Counter objects have a dictionary interface except that they return a zero count for missing items instead of raising
# a KeyError

c = Counter(['eggs', 'ham'])
print(c['bacon'])  # count of a missing element is zero


c = Counter(a=4, b=2, c=0, d=-2)
print(sorted(c.elements()))

c = Counter(a=4, b=2, c=0, d=-2, e=1)
d = Counter(a=1, b=2, c=3, d=4)
c.subtract(d)
print(c)
print(c.total())

print(+c)  # WOW, + in the beginning of objects with __pos__ or __neg__ methods returns only positive values. So sweet!

# ----------------------------------------------------------------------------------------------------------------------

from collections import OrderedDict

o_d: OrderedDict = OrderedDict.fromkeys('abcde')
print(o_d)
o_d.move_to_end('b')
print(' -> '.join(o_d))
o_d.move_to_end('b', last=False)  # Moves 'b' to the head
print(' -> '.join(o_d))

# ----------------------------------------------------------------------------------------------------------------------

from collections import defaultdict

# Basically, rewrites the __missing__ method, using the default_factory attribute, passed while an assignation

dfd = defaultdict(list)
storage = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
for k, v in storage:
    dfd[k].append(v)

print(dfd)

dfd = defaultdict(int)
for k, v in storage:
    dfd[k] += v
print(dfd)

dfd = defaultdict(lambda: 1)
dfd['a']
print(dfd)

# ----------------------------------------------------------------------------------------------------------------------

from collections import UserList

# Class that simulates a list. The instance’s contents are kept in a regular list, which is accessible via the data
# attribute of UserList instances. The instance’s contents are initially set to a copy of list, defaulting to the empty
# list []. list can be any iterable, for example a real Python list or a UserList object

ul = UserList([1, 2, 3, 4])
print(ul)
print(ul.data)

# Basically it's just a wrapper to be inherited for User Classes. It' better than list because:
'''
Custom Behavior: If you need to customize the behavior of list-like objects by adding additional methods, overriding 
                 existing methods, or providing custom behavior for certain operations, subclassing UserList allows you 
                 to do so while still maintaining compatibility with the built-in list interface.

Encapsulation: Subclassing UserList can help encapsulate the implementation details of your list-like objects, making 
               your code more modular and easier to maintain. By defining a subclass of UserList, you can hide the 
               underlying implementation and expose only the methods and properties that are relevant to the users of your class.

Type Checking and Validation: If you need to perform type checking or validation on the elements of your list-like 
                              objects, subclassing UserList allows you to override methods like append() or extend() to 
                              perform type checking and validation before adding elements to the list.

Integration with               Some frameworks or libraries may expect or require objects to be instances of
Frameworks and Libraries:      UserList or its subclasses. By subclassing UserList, you can ensure 
                               compatibility with such frameworks and libraries by providing list-like 
                               objects that adhere to their expected interface or behavior.
'''

# ----------------------------------------------------------------------------------------------------------------------

from collections import UserString

ustr = UserString("Hello, world!")
print(ustr)
print(ustr.data)

# Basically the same purpose as of UserList

# ----------------------------------------------------------------------------------------------------------------------

from collections import UserDict

usdct = UserDict.fromkeys("Hello, world!")
print(usdct)
print(usdct.data)

# The same thingy
