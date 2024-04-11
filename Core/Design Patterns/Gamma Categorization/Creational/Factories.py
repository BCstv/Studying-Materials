"""
When object creation logic becomes too convoluted, Initializer is not descriptive (
    Name is always __init__,
    Cannot overload with same sets of arguments with different names,
    Can turn into 'optional parameter hell'
), and Wholesale object creation (non-piecewise, unlike Builder) can be outsourced to (
    A separate method (Factory Method),
    That may exist in a separate class (Factory),
    Can create hierarchy of factories (Abstract Factory)
)
"""

# Factory - A component responsible solely for the wholesale (not piecewise) creation of objects.

# ----------------------------------------------------------------------------------------------------------------------

# Factory Method - It's an any method which creates an object!

"""
"Define an interface for creating an object,but let subclasses decide which class to instantiate. Factory Method lets a 
class defer instantiation to subclasses."
                                                @GoF
"""


from enum import Enum, auto
from math import sin, cos


class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2

class Point:
    # def __init__(self, a, b, system=CoordinateSystem.CARTESIAN):
    #     if system == CoordinateSystem.CARTESIAN:
    #         self.x = a
    #         self.y = b
    #     elif system == CoordinateSystem.POLAR:  # THIS IS PAINFUL!!!!!!!!!!
    #         self.x = a * sin(b)
    #         self.y = a * cos(b)

    # """ def __init__(self, rho, theta):
    #   it's impossible"""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    @staticmethod
    def new_cartesian_coordinates(x, y):
        return Point(x, y)

    @staticmethod
    def new_polar_coordinates(rho, theta):
        return Point(rho * cos(theta), rho * sin(theta))

p = Point(2, 3)
p2 = Point.new_polar_coordinates(2, 3)
print(p, p2)

# ----------------------------------------------------------------------------------------------------------------------

# Factory
# Once you get too many factory methods inside a class, it might make sense to move them out of the class, or at least
# to try and group them somehow into a separate entity

class PointFactory:
    @staticmethod
    def new_cartesian_coordinates(x, y):
        p = Point()
        p.x = x
        p.y = y
        return p

    @staticmethod
    def new_polar_coordinates(rho, theta):
        return Point(rho * cos(theta), rho * sin(theta))


# ----------------------------------------------------------------------------------------------------------------------

# Abstract Factory

"""
"Provide an interface for creating families of related or dependent
objects without specifying their concrete classes"
                             @GoF
"""

from abc import ABC

class HotDrink(ABC):
    def consume(self):
        pass

class Tea(HotDrink):
    def consume(self):
        print('This tea is delicious')

class Coffee(HotDrink):
    def consume(self):
        print('This coffee is delicious')

class HotDrinkFactory(ABC):
    def prepare(self, amount):
        pass

class TeaFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f'Put in tea bag, boil water, '
              f'pour {amount} ml. Enjoy!')
        return Tea()

class CoffeeFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f'Grind some beans, boil water,'
              f' pour {amount} ml. Enjoy!')
        return Coffee()

def make_drink(type):
    if type == 'coffee':
        return CoffeeFactory().prepare(200)
    elif type == 'tea':
        return TeaFactory().prepare(200)
    else:
        return None

class HotDrinkMachine:
    class AvailableDrink(Enum):
        Coffee = auto()
        TEA = auto()

    factories = []
    initialized = False

    def __init__(self):
        if not self.initialized:
            self.initialized = True
            for d in self.AvailableDrink:
                name = d.name[0] + d.name[1:].lower()
                factory_name = name + 'Factory'
                factory_instance = eval(factory_name)()
                self.factories.append((name, factory_instance))

    def make_drink(self):
        print('Available drinks: ')
        for f in self.factories:
            print(f[0])

        s = input("Pick a drink: ")
        idx = int(s)
        s = input('Specify amount: ')
        amount = int(s)
        return self.factories[idx][1].prepare(amount)


entry = input("What kind of drink would you like? ")
drink = make_drink(entry)
drink.consume()

hdm = HotDrinkMachine()
hdm.make_drink()

# TEST
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class PersonFactory:
    id = -1
    def create_person(self, name):
        self.id += 1
        return Person(self.id, name)
# SUCCESS

# Summary
'''
- A factory method is a static method that creates objects
- A factory is any entity that can take care of object creation
- A factory can be external or reside inside the object as an inner class
- Hierarchies of factories can be used to create related objects
'''







