# Data classes are like children. They are okay as a starting point, but to participate as a grownup object,
# they need to take some responsibility
import dataclasses
import typing


# The Python suggests a few ways to build a simple class that is just a collection of fields, with little or no extra functionality:

# collections.namedtuple

# typing.NamedTuple

# @dataclasses.dataclass - a data class that allows more customization than previous alternatives, adding lots of options
# and potential complexity


class Coordinate:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


moscow = Coordinate(55.76, 37.62)
red_square = Coordinate(55.76, 37.62)
print(moscow)
print(moscow == red_square)
print((moscow.lat, moscow.lon) == (red_square.lat, red_square.lon))

# Ugly way, right?

from collections import namedtuple
Coordinate = namedtuple('Coordinate',
                        ['lat', 'lon'])

moscow = Coordinate(55.76, 37.62)
red_square = Coordinate(55.76, 37.62)
print(moscow)  # Useful __repr__
print(moscow == red_square)  # Inherited __eq__

# The newer typing.NamedTuple provides the same functionality, adding a type annotation to each field
from typing import NamedTuple
Coordinate = NamedTuple('Coordinate',
                        [('lat', float), ('lon', float)])

print(issubclass(Coordinate, tuple))

print(typing.get_type_hints(Coordinate))

# Since Python 3.6, typing.NamedTuple can also be used in a class statement, with type annotations written
class Coordinate(NamedTuple):
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        nt = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}° {ns}, {abs(self.lon):.1f}° {nt}'


moscow = Coordinate(55.76, 37.62)
print(moscow)

# Although, typing.NamedTuple appears as a superclass, it's actually not. NamedTuple uses the advanced functionality
# of a metaclass (is one of the subjects covered in Chapter 24, "class metaprogramming") to customize the creation of the
# user's class:

print(issubclass(Coordinate, NamedTuple('a')))
print(issubclass(Coordinate, tuple))

from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        nt = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}° {ns}, {abs(self.lon):.1f}° {nt}'

print(Coordinate)
'''
                          namedtuple               NamedTuple               dataclass
                          
mutable instances         No                       No                       Yes
^ 
A key difference between these class builders is that namedtuple and NamedTuple build tuple subclasses, therefore the 
instances are immutable. By default, the @dataclass produces mutable classes. But the decorator accepts a keyword argument
frozen. When frozen=True, the class will raise an exception if you try to assign a value to a field after the instance is initialized

class statement syntax    No                       Yes                      Yes
^
Only NamedTuple and dataclass support the regular class statement syntax, making it easier to add methods and docstrings
to the class you are creating

construct dict            x._asdict()              x._asdict()              dataclasses.asdict(x)
^
Both named tuple variants provide an instance method (._asdict) to construct a dict object from the fields in a data 
class instance. The dataclasses module provides a function to do it: dataclasses.asdict

get field names           x._fields                x._fields                [f.name for f in dataclasses.fields(x)]
get defaults              x._field_defaults        x._field_defaults        [f.default for f in dataclasses.fields(x)]
^
All three class builders let you get the field names and default values that may be configured for them. In named tuple
classes, that metadata is in the ._fields and ._fields_defaults class attributes. You can get the same metadata from a 
dataclass decorated class using the fields function from the dataclasses module. It returns a tuple of Field objects 
that have several attributes, including name and default

get field types           N/A                      x.__annotations__        x.__annotations__
^
Classes defined with the help of typing.NamedTuple and @dataclass have a mapping of field names to type the 
__annotations__ class attribute. As mentioned, use the typing.get_type_hints function instead of reading __annotations__
directly

new instance with changes x._replace(...)          x._replace(...)          dataclasses.replace(x, ...)
^
Given a named tuple instance x, the call x._replace(**kwargs) returns a new instance with some attribute values 
replaced according to the keyword arguments given. The dataclasses.replace(x, **kwargs) module-level function does the 
same foe an instance of a dataclass decorated class

new class at runtime      namedtuple(...)          NamedTuple(...)          dataclasses.make_dataclass(...)
^
Although the class statement syntax is more readable, it is hardcoded. A framework may need to build data classes on the
fly, at runtime. For that, you can use the default function call syntax of collections.namedtuple, which is likewise 
supported by typing.NamedTuple. The dataclasses module provides a make_dataclass function for the same purpose
'''

# ----------------------------------------------------------------------------------------------------------------------

# Classic Named Tuples

City = NamedTuple(
    'City',
    [('name', str), ('country', str), ('population', int), ('coordinates', tuple[float, float])]
)

tokyo = City('tokyo', 'JP', 34019502, (-123.456, -122.456))

print(tokyo)
print(tokyo.country)
print(tokyo[1])

Coordinate = namedtuple(
    'Coordinate',
    ['latitude', 'longitude'])

print(tokyo._fields)
delhi_data = ('Delhi NCR', 'IN', 21948, Coordinate(123.456, -122.456))
delhi = City._make(delhi_data)
print(delhi)
print(delhi._asdict())

import json
print(json.dumps(delhi._asdict()))


Coordinate = namedtuple(
    'Coordinate',
    ['lat', 'lon', 'reference'],
    defaults=['WGS84']
)

moscow = Coordinate(123.456, -122.456)
print(moscow)
print(moscow._field_defaults)

class Coordinate(NamedTuple):
    lat: float
    lon: float
    reference: str = 'WGS84'


print(Coordinate.__annotations__)
print(Coordinate.__doc__)

# ----------------------------------------------------------------------------------------------------------------------

# More about @dataclass

# The signature of @dataclass:
# @dataclasses.dataclass(*, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)

'''
Option            Meaning                     Default         Notes
init              Generate __init__           True            Ignored if __init__ is implemented by user
repr              Generate __repr__           True            Ignored if __repr__ is implemented by user
eq                Generate __eq__             True            Ignored if __eq__ is implemented by user
order             Generate lt, le, gt, ge     False           If True, raises exceptions if eq=False, or it any of the 
                                                              comparison methods that would be generated are defined or inherited
unsafe_hash       Generate __hash__           False           Complex semantics and several caveats (docs)
frozen            Make instances 'immutable'  False           Instances will be reasonably safe from accidental change, but nor really immutable
'''


# ----------------------------------------------------------------------------------------------------------------------

# Field Options

'''
@dataclass
class ClubMember:
    name: str
    guests: list = []

Will raise a Value error
ValueError: mutable default <class 'list'> for field guests is not allowed: use default_factory
'''

from dataclasses import field

# Keyword arguments accepted by the field function
'''
Option               Meaning                                 Default
default              Default value for field                 _MISSING_TYPE (a sentinel value indicating the option was not
                                                             provided . It exists so we can set None as an actual default
                                                             value, a common use case

default_factory      0-parameter function used to produce    _MISSING_TYPE
                     a default value                     
                     
init                 Include field in parameters to __init__ True
repr                 Include field in __repr__               True
compare              Use field in comparison methods         True
                     eq, lt, etc.
hash                 Include field in __hash__ calculation   None (The option hash=None means the field will be used as
                                                             __hash__ only if compare = True)
metadata             Mapping with the user-defined data;     None
                     ignored by the @dataclass
'''

@dataclass
class ClubMember:
    name: str
    guests: list[str] = field(default_factory=list)
    athlete: bool = field(default=False, repr=False)


guest = ClubMember('Alice')
print(guest.guests.append('str'))
print(guest)

# ----------------------------------------------------------------------------------------------------------------------

# Post-init Processing

# The __init__ method generated by @dataclass only takes the arguments passed and assigns them - or their default values
# if missing - to the instance attributes that are instance fields. But you may need to do more than that to initialize
# the instance. If that's the case, you can provide a __post_init__ method. When that method exists, @dataclass will add
# code to the generated __init__ to call __post_init__ as the last step

@dataclass
class HackerClubMember(ClubMember):
    all_handles = str()
    handle: str = ''

    












