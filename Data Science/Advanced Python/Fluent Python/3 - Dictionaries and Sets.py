# Python is basically dicts wrapped in loads of syntactic sugar

# Hash tables are the engines behind Python's high-performance dicts

# Other built-in types based on hash tables are set and frozenset

# Python implement all fundamental operations from set theory, like union, intersection, subset tests, etc.
# With them, we can express algorithms in a more declarative way, avoiding lots of nested loops and conditionals

# We can build a dict instance by taking key:value pairs from any iterable
dial_codes = [
    (880, 'Bangladesh'),
    (55, 'Brazil'),
    (86, 'China'),
    (91, 'India'),
    (62, 'Indonesia'),
    (81, 'Japan'),
    (234, 'Nigeria'),
    (92, 'Pakistan'),
    (7, 'Russia'),
    (1, 'United States')
]

country_dial = {country: code for code, country in dial_codes}  # Looks weird, but it's basically
# for code, country in dial_codes:
#   {country: code}
print(country_dial)

country_dial = {code: country.upper() for country, code in sorted(country_dial.items()) if code > 70}
print(country_dial)


# ----------------------------------------------------------------------------------------------------------------------

# Mappings
# Unpacking mappings
def dump(**kwargs):
    return kwargs


print(dump(**{'x': 1}, y=2, **{'z': 3}))
print(dump(**{'a': 1, **{'x': 1}, 'y': 2, **{'z': 3, 'x': 4}}))

# Merging mappings using |
d1 = {'a': 1, 'b': 3}
d2 = {'a': 2, 'b': 4, 'c': 6}
print(d1 | d2)


# Pattern Matching with Mappings

def get_creators(record: dict) -> list:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:
            return names
        case {'type': 'book', 'api': 1, 'authors': name}:
            return [name]
        case {'type': 'book'}:
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {'type': 'movie', 'director': name}:
            return [name]
        case _:
            raise ValueError(f"Invalid record: {record!r}")


b1 = dict(type='book', api=2, authors='Stanislav Stas Stasyambo'.split())
print(get_creators(b1))
# print(get_creators(dict(type='book', pages=770)))

food = dict(category='ice cream', flavor='vanilla', cost=199)
match food:
    case {'category': 'ice cream', **details}:
        print(f"Ice cream details: {details}")

# Standard API of Mapping types

from collections import abc

# The main value of the ABCs is documenting and formalizing the standard interfaces for mappings, and serving as
# criteria for isinstance tests on code that needs to support mappings in a broad sense

print(isinstance({}, abc.Mapping))
print(isinstance({}, abc.MutableMapping))

# Using isinstance with an ABC is often better than checking whether a function argument is of the concrete dict type,
# because when alternative mapping types can be used.

# ----------------------------------------------------------------------------------------------------------------------

# Hashing
# An object is hashable if it has a hash code which never changed during its lifetime
# It needs a __hash__() method, and can be compared to other objects, so __eq__() method is necessary
# Hashable objects which compare equal must have the same hash code

tt = (1, 2, (30, 40))
print(hash(tt))

# tf = (1, 2, [30, 40])
# print(hash(tf))
# ! TypeError: unhashable type: 'list'

# User-defined types are hashable by default because their hash code is their id(), and the  __eq__() method inherited
# from the object class simply compares the object IDs


# Inserting or Updating Mutable Values

import re
import sys

RE = re.compile(r'\w+')
index = {}
print(sys.argv)

with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            # ^ This is ugly!
            occurences = index.get(word, [])  # Get the list of all occurences for word, or [] if not found
            occurences.append(location)  # Append new location to occurrences
            index[
                word] = occurences  # Put changed occurrences into index dict; this entails a second search through the index

with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index.setdefault(word, []).append(
                location)  # Get the list of occurrences for word, or set it to [] if not found
            # setdefault returns a value, so it can be updated without requiring a second search
            # In other words it looks like this:
            # if key not in my_dict:
            #   my_dict[key] = []
            # my_dict[key].append(new_value)

import collections

index = collections.defaultdict(list)  # Create a defaultdict with the list constructor as default_factory

with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index[word].append(location)  # If word is not initially in the index, the default_factory is called to
            # produce the missing value, which in this case is an empty list that is then assigned to index[word] and
            # returned, so the .append(location) operation always succeeds

# Display in alphabetical order
for word in sorted(index, key=str.upper):  # key=str.upper is used just to normalize the sorting
    print(word, index[word])


# Run it using $ python '3 - Dictionaries and Sets.py' 'aaaa'

# The mechanism that makes defaultdict work by calling default_factory is the __missing__ special method

# ----------------------------------------------------------------------------------------------------------------------

# The __missing__ Method

class StrKeyDict(dict):
    def __missing__(self, key):
        print('Running the missing method')
        if isinstance(key, str):  # Check whether key is already a str. If it is, and it's missing, raise an error
            raise KeyError(key)
        return self[str(key)]  # Build str from key and look it up

    # Why does if isinstance check is important here?
    # Without that test our __missing__ method would work OK for any key k--str or not str--whenever str(k) produced an
    # existing key

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()


d = StrKeyDict([('2', 'two'), ('3', 'three'), ('4', 'four')])
print(d)
print(d.get('2'))
print("Here the missing method wasn't called ^")
print(d.get(2))
print('Here the missing method was called 1 time ^')
print(d.get(1))
print('Here the missing method was called 2 times ^')

print('Checking if the key is an instance of str - ', isinstance('2', str))

# ----------------------------------------------------------------------------------------------------------------------

# Inconsistent usage of __missing__ in the Standard library

# If it is a dict subclass:
'''
A subclass of dict implementing only __missing__ and no other method. In this case, __missing__
may be called only on d[k], which will use the __getitem__ inherited from dict
'''
# if collections.UserDict subclass:
'''
Likewise, a subclass of UserDict implementing only __missing__ and no other method. The get method inherited from 
UserDict calls __getitem__. This means __missing__ may be called to handle lookups with d[k] and d.get(k)
'''
# If abc.Mapping subclass (with the simplest __getitem__):
'''
A minimal subclass of abc.Mapping implementing __missing__ and the required abstract methods, including an
implementation of __getitem__ that does not call __missing__. The __missing__ method is never triggered in this class
'''

# If abc.Mapping subclass with (__getitem__ calling __missing__):
'''
A minimal subclass of abc.Mapping implementing __missing__ and the required abstract methods, including an
implementation of _-getitem__ that calls __missing__. The __missing__ method is triggered in this class for missing key 
lookups made with d[k], d.get(k), and k in d
'''

# ----------------------------------------------------------------------------------------------------------------------

# Variations of dict

# collections.OrderedDict:
# The only reason to use OrderedDict is writing code that is backward compatible with earlier Python versions (<3.6)
# Because since then, the Python stores all it's dictionaries ordered right from the box

cod = collections.OrderedDict({'a': 1, 'b': 2, 'c': 3})

'''
* The equality operation for OrderedDict checks for matching order
* The popitem() method of OrderedDict has a different signature. It accepts an optional argument to specify which item
is popped 
* !!! OrderedDict has a move_to_end() method to efficiently reposition an element to an endpoint !!!
* The regular dict was designed to be very good at mapping operations. Tracking insertion order was secondary!
* OrderedDict was designed to be good at reordering operations. Space efficiency, iteration speed, and the performance
of update operations were secondary!
* Algorithmically, OrderedDict can handle frequent reordering operations better than dict. This makes it suitable for 
tracking recent accesses (for example, in an LRU cache) 
'''
print(cod)
cod.move_to_end('a')
print(cod)

# collections.ChainMap:
fir_d = {'a': 1, 'b': 2}
sec_d = {'a': 2, 'b': 4, 'c': 3}
thi_d = {'g': 5}
ccm = collections.ChainMap(fir_d, sec_d, thi_d)

print(ccm['a'])
ccm.__delitem__('a')
print(ccm['a'])

print(ccm['g'])
thi_d.__delitem__('g')
# print(ccm['g']) Will raise an error. It's not possible to call the only removed variable

print(fir_d)
print(ccm)

# The ChainMap instance does not copy the input mappings, but holds references to them. Updated or insertions to a
# ChaiMap only affect the first input mapping.

'''
ChainMap is useful to implement interpreters for languages with nested scopes, where each mapping represents a scope
context, from the innermost enclosing scope to the outermost scope. The 'ChainMap objects' section of the collections
docs has several examples of ChainMap usage, including

# import builtins
# pylookup = ChainMap(locals(), globals(), vars(builtins))

inspired by the basic rules of variable lookup in Python
'''

# collections.Counter
ct = collections.Counter('abracadabra')
print(ct)
print(ct.most_common(2))

ca = collections.Counter(['a', 'b', 'c'])
ca = ca + ct
print(ca)


# A mapping that holds an integer count for each key. Updating an existing key adds to its count.

# This can be used to count instances of hashable object or as a multiset

# shelve.Shelf
# https://docs.python.org/3/library/shelve.html#
# https://nedbatchelder.com/blog/202006/pickles_nine_flaws.html

def adder(a, b):
    return a + b


a = list(map(adder, [1, 2, 3], [2, 1, 0]))
print(a)


# ----------------------------------------------------------------------------------------------------------------------

# Why it is better to use UserDict rather than dict for an inheriting in user-defined classes

# Because it has some implementation shortcuts

class StrKeyDict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.keys()

    def __setitem__(self, key, value):
        self.data[str(key)] = value  # __setitem__ converts any key to a str. This method is easier to overwrite when we
        # can delegate to the self.data attribute

    def __repr__(self):
        return f'{self.data}'


asa = StrKeyDict({2: 1})
print(asa)

values_class = type({}.values())
print(values_class)

# ----------------------------------------------------------------------------------------------------------------------

# Set Theory
# A set is a collection of unique objects. A basic use case is removing duplication
ll = ['spam', 'eggs', 'bacon', 'eggs', 'spam', 'eggs', 'bacon']
print(set(ll))
print(dict.fromkeys(ll).keys())

fkd = dict.fromkeys(ll)
fkd['spam'] = 'aaaaa'
print(fkd)

haystack = {'spam', 'eggs', 'bacon', 'aboba'}
needles = {'spam', 'eggs', 'sword'}

print(haystack & needles)  # {'spam', 'eggs'}
print(set(needles).intersection(haystack))  # Basically the same thing

print(haystack - needles)

ffs = frozenset({'spam', 'eggs', 'bacon', 'milk', 'oil', 'chicken', 'rice'})
# The set type is mutable, meaning it can be changed, and the frozenset type is immutable, meaning it can't be changed
ffs -= haystack
print(ffs)

from unicodedata import name  # To obtain character names
print({chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i), '')})

# Practical Consequences of How Sets Work
'''
* Set elements must be hashable objects. They must implement proper __hash__ and __eq__ methods

* Membership testing os very efficient. A set may have millions of elements, but an element can be located directly by
computing its hash code and deriving an index offset, with the possible overhead of a small number of tries to find a
matching element or exhaust the search

* Sets have a significant memory overhead, compared to a low-level array pointers to its elements - which would be 
more compact but also much slower to search beyond a handful of elements

* Element ordering depends on insertion order, but not in a useful or reliable way. If two elements are different but
have the same hash code, their position depends on which element is added first

* Adding elements to a set may change the order of existing elements. That's because the algorithm becomes less 
efficient if the hash table is more than two-thirds full, so Python may need to move and resize the table as it grows, 
When this happens, elements are reinserted and their relative ordering may change
'''

# The whole set theory in Python:
r'''
Math symbol    Python operator        Method                                  Description
S ∩ Z         s & z                  s.__and__(z)                            Intersection of s and z
              z & s                  s.__rand__(z)                           Reversed & operator
                                     s.intersection(it, ...)                 Intersection of s and all sets built from 
                                                                             iterables it, etc
              s &= z                 s.__iand__(z)                           s updated with intersection of s and z
                                     s.intersection_update(it, ...)          s updated with intersection of s and all 
                                                                             sets built from iterabled it, etc
S ∪ Z         s | z                  s.__or__(z)                             Union of s and z
              z | s                  s.__ror__(z)                            Reversed | operator
                                     s.union(it, ...)                        Union of s and all sets built from 
                                                                             iterables it, etc
              s |= z                 s.__ior__(z)                            s updated with union of s and z
                                     s.update(it, ...)                       s updated with union of s and all sets 
                                                                             built from iterables it, etc
S \ Z         s - z                  s.__sub__(z)                            Relative complement or difference between 
                                                                             s and z
              z - s                  s.__rsub__(z)                           Reversed - operator
                                     s.difference(it, ...)                   Difference between s and all sets built 
                                                                             from iterables it, etc
              s -= z                 s.__isub__(z)                           s updated with difference of s and z
                                     s.difference_update(it, ...)            s updated with the difference of s and all 
                                                                             sets built from iterables it, etc
S Δ Z         s ^ z                  s.__xor__(z)                            Symmetric difference (the complement of the
                                                                             intersections s & z)
              z ^ s                  s.__rxor__(z)                           Reversed ^ operator
                                     s.symmetric_difference(it)              Complement of s & set(it)
              s ^= z                 s.__ixor__(z)                           s updated with symmetric difference of s and z
                                     s.symmetric_difference_update(it)       s updated with symmetric difference of s 
                                                                             and all sets built from iterables it, etc
S ∩ Z = ∅                            s.isdisjoint(z)                         s and z are disjoint (no elements in common)
e ∈ S         e in s                 s.__contains__(e)                       Element is a meneber of s
S ⊆ Z         s <= z                 s.__le__(z)                             s is a subset of the z set
                                     s.issubset(it)                          s is a subset of the set built from the iterable it
S ⊂ Z         s < z                  s.__lt__(z)                             s is a proper sunset of the z set
S ⊇ Z         s >= z                 s.__ge__(z)                             s is a superset of the z set
                                     s.issuperset(it)                        s is a superset of the set built from the iterable it
S ⊃ Z         s > z                  s.__gt__(z)                             s is a proper sunset of the z set
'''

d1 = dict(a=1, b=2, c=3)
d2 = dict(a=10, b=20, g=30)

print(list(f'{d2[i]}, {d1[i]}' for i in set(d1) & set(d2)))


# ----------------------------------------------------------------------------------------------------------------------

# CHAPTER SUMMARY

''' 
1. Dictionaries are a keystone of Python. Over the years, the familiar {k1: v1, k2: v2} literal syntax was enhanced to
support unpacking with **, pattern matching, as well as dict comprehensions

2. Beyond the basic dict, the standard library offers handy, ready-to-use specialized mappings like defaultdict, 
ChainMap, and Counter, all defined in the collections module. With the new dict implementation, OrderedDict is not as 
useful as before, but should remain in the standard library for backward compatibility -- and has specific characteristics
that dict doesn't have, such as taking into account key ordering on == comparisons. Also in the collections module is 
the UserDict, an easy to use base class to create custom mappings

3. Two powerful methods available in most mappings are setdefault and update. The setdefault method can update items
holding mutable values -- for example, in a dict of list values -- avoiding a second search for the same key. The update
method allows bulk insertion or overwriting of items from any other mapping, from iterables providing (key, value) pairs,
and from keyword arguments. Mapping constructors also use update internally, allowing instances to be initialized from
mappings, iterables, or keyword arguments. Since Python 3.9, we can also use the |= operator to update a mapping, and 
the | operator to create a new one from the union of two mappings

4. A clever hook in the mapping API is the __missing__ method, which lets you customize what happens when a key is not
found when using the d[k] syntax that invokes __getitem__

5. The collections.abc module provides the Mapping and MutableMapping abstract base classes as standard interfaces, 
useful for runtime type checking. The Mapping ProxyType from the types module creates an immutable facade for a mapping 
you want to protect from accidental change. There are also ABCs for Set and MutableSet
'''

true, false, null = True, False, None

fruit = dict(
    type='banana',
    avg_weight=123.2,
    edible_peel=false,
    species=["acuminata", "balbisiana", "paradisiaca"],
    issues=null
)

fruits = {
    'type': 'banana',
    'avg_weight': 123.2,
    'edible_peel': false,
    'species': ['acuminata', 'balbisiana', 'paradisiaca'],
    'issues': null}


print(fruit == fruits, fruit)

# The syntax everybody now uses for exchanging data is Python's dict and list syntax. Now we have the nice syntax with
# the convenience of preserved insertion order.








