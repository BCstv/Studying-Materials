# Subclassing Built-In Types
class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)

dd = DoppelDict(one=1)  # The __init__ completely ignores the overwritten __setitem__ method

dd['two'] = 2  # Works properly

dd.update(three=3)  # The .update doesn't use our __setitem__ too((

print(dd)

class AnswerDict(dict):
    def __getitem__(self, item):
        return 42

ad = AnswerDict(a='foo')
print(ad)
print(ad['a'])

# But if we were using collections.UserDict, both those issues would have been fixed

import collections
class DoubleDict(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value]*2)

dd = DoubleDict(one=1)
dd['two'] = 2
dd.update(three=3)

print(dd)

# ----------------------------------------------------------------------------------------------------------------------

# Multiple Inheritance and Method Resolution Order

class Root:
    def ping(self):
        print(f'{self}.ping() in Root')

    def pong(self):
        print(f'{self}.pong() in Root')

    def __repr__(self):
        return f'<instance of {type(self).__name__}>'

class A(Root):
    def ping(self):
        print(f'{self}.ping() in A')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in A')
        super().pong()
        
class B(Root):
    def ping(self):
        print(f'{self}.ping() in B')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in B')
        
class Leaf(A, B):
    def ping(self):
        print(f'{self}.ping() in Leaf')
        super().ping()

leaf1 = Leaf()
leaf1.ping()
print('-----')
leaf1.pong()

print(Leaf.__mro__)
# Leaf.ping() activates the implementation in the next class of Leaf.__mro__: the A class.
# Method A.pong() calls super().pong(). The B class is next in __mro__, therefore B.pong is activated

def _upper(key):
    try:
        return key.upper()
    except AttributeError:
        return key

# ----------------------------------------------------------------------------------------------------------------------

# Mixin Classes

class UpperCaseMixin:  # The mixin implements four essential methods of mappings, always calling super(), with the key unchanged
    def __setitem__(self, key, value):
        super().__setitem__(_upper(key), value)

    def __getitem__(self, item):
        return super().__getitem__(_upper(item))

    def get(self, key, default=None):
        return super().get(_upper(key), default)

    def __contains__(self, item):
        return super().__contains__(_upper(item))

class UpperDict(UpperCaseMixin, collections.UserDict):  # UpperDict needs no implementation of its own, but
    # UpperCaseMixin must be the first base class, otherwise the methods from UserDict would be called instead
    pass

class UpperCounter(UpperCaseMixin, collections.Counter):  # UpperCaseMixin also works with Counter
    """Specialized 'Counter' that uppercases string keys"""  # Instead of pass, it's better to implement a docstring
    # to satisfy the need for a body in the class statement syntax

d = UpperDict([('aAa', 'letters A'), (2, 'digit two')])
print(d)
print(d['aAa'])
print('aAa' in d, 'AAA' in d)
print(d.keys())

c = UpperCounter('BaNanA')
print(c)

# ----------------------------------------------------------------------------------------------------------------------

# Subclass Only Classes Designed for Subclassing

'''
Subclassing any complex class and overriding its methods is error-prone because the superclass methods may ignore the 
subclass overrides in unexpected ways. As much as possible,avoid overriding methods, or at least restrain yourself to 
subclassing classes which are designed to be easily extended, and only in the ways in which they were designed to be 
extended
'''