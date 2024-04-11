"""
For some components it makes sense to have one in the system (database repository, object factory)
The initializer call is expensive
Want to prevent anyone creating additional copies
Need to take cary of lazy instantiation
"""

"""
"Ensure a class only has one instance, and provide a global point of
access to it"
                            @GoF
"""

# ----------------------------------------------------------------------------------------------------------------------

# Singleton Allocator

class Database(object):
    _instance = None

    def __init__(self, x):
        print('Loading a database from file')
        self.x = x
        print(x)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(Database)
        return cls._instance

d1 = Database(2)
d2 = Database(3)

# The problem with a singleton allocator is that it calls __init__() method

print(d1 is d2)
print(d1.x, d2.x)

# ----------------------------------------------------------------------------------------------------------------------

# Singleton Decorator

def singleton(class_):
    instances = {}
    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance
@singleton
class Database:
    def __init__(self, x):
        print('Creating a database')
        self.x = x
        print(x)

d1 = Database(2)
d2 = Database(3)
print(d1.x, d2.x)
print(d1 is d2)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = type.__call__(cls, *args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self, x):
        print('Creating a database')
        self.x = x
        print(x)

d1 = Database(2)
d2 = Database(3)
print(d1.x, d2.x)
print(d1 is d2)

# ----------------------------------------------------------------------------------------------------------------------

# Monostate

class CEO:
    _shared_state = {
        'name': 'Steve',
        'age': 36
    }

    def __init__(self):
        self.__dict__ = self._shared_state

    def __str__(self):
        return f'{self.name} is {self.age} years old!'

ceo1 = CEO()
print(ceo1)

ceo2 = CEO()
ceo2.age = ceo2.age + 1
print(ceo1)
print(ceo2)


class Monostate:
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj.__dict__ = cls._shared_state
        print(cls._shared_state)
        return obj

class CFO(Monostate):
    def __init__(self):
        self.income = 0
        self.name = ''

    def __str__(self):
        return f'{self.name} is {self.income}$'

cfo1 = CFO()
cfo1.name = 'John'
print(cfo1)
cfo2 = CFO()
cfo2.income = 29
print(cfo1, cfo2, sep='\n')

# Summary
"""
- Different realizations of Singleton: custom allocator, decorator, metaclass
- Laziness is eazy, just init on first request
- Monostate variation
"""



