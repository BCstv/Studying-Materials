# A design pattern is a general recipe for solving a common design problems

# ----------------------------------------------------------------------------------------------------------------------

# Refactoring Strategy (leverage functions as first-class objects)

# Strategy pattern - define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets
# the algorithm vary independently of clients that use it

"""
Consider an online store with these discount rules:
* Customers with 1,000 or more fidelity points get a global 5% discount
* A 10% discount is applied to each line item with 20 or more units in the same order
* Orders with at least 10 distinct items get a 7% global discount

For brevity, let's assume that only one discount may be applied to an order
"""
import functools
import time


def clock(func):
    @functools.wraps(func)
    # functools.wraps, a helper for building well-behaved decorators
    # It prohibits to the original function lose some of its metadata (__module__, __name__, __doc__, etc.) in the
    # decorator function
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0

        arg_lst = [repr(arg) for arg in args]
        arg_lst.extend(f'{k}={v!r}' for k, v in kwargs.items())
        arg_str = ', '.join(arg_lst)

        print(f'[{elapsed:0.8f}] {func.__name__}({arg_str}) -> {result}')
        return result
    return clocked

from abc import ABC, abstractmethod
from collections.abc import Sequence
from decimal import Decimal
from typing import NamedTuple

class Customer(NamedTuple):
    name: str
    fidelity: int

class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal()

    def total(self) -> Decimal:
        return self.price * self.quantity



class Order(NamedTuple):
    customer: Customer
    cart: Sequence[LineItem]
    promotion: 'Promotion' = None

    def total(self) -> Decimal:
        totals = (map(lambda item: item.total(), self.cart))
        return sum(totals, start=Decimal(0))

    def __repr__(self):
        return f'Order({self.customer.name}, {self.total()})'

class Promotion(ABC):
    # It's an interface which allows us to get access to the concrete strategies
    @abstractmethod  # means that doesn't have an implementation, but must be implemented in subclasses
    def discount(self, order: Order) -> Decimal:
        """
        :parameter order: Order to discount
        :return: Returns discount as a positive dollar amount
        """
class FidelityPromo(Promotion):  # First Concrete Strategy
    """5% discount for customers with 1000 or more fidelity points"""
    @clock
    def discount(self, order: Order) -> Decimal:
        rate = Decimal('0.05')
        if order.customer.fidelity >= 1000:
            return order.total() * rate
        return Decimal(0)

class BulkItemPromo(Promotion):  # Second Concrete Strategy
    """10% discount for each LineItem with 20 or more units"""
    def discount(self, order: Order) -> Decimal:
        discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * Decimal('0.1')
        return discount

class LargeOrderPromo(Promotion):  # Third concrete strategy
    """7% discount for orders with 10 or more distinct items"""
    def discount(self, order: Order) -> Decimal:
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * Decimal('0.07')
        return Decimal(0)


stas = Customer('Stas', 1010)

cart = (LineItem('Banana', 100, Decimal('20.1')),
        LineItem('Apple', 150, Decimal('10.5')),
        LineItem('Pineapple', 120, Decimal('50.99')))


order = Order(stas, cart)
total = order.total()
for prom in Promotion.__subclasses__():
    discount = prom().discount(order)
    total -= discount
    print(f'{prom.__name__} gives {discount} discount, therefore total is: {total}')


# ----------------------------------------------------------------------------------------------------------------------

# Function-Oriented Strategy

'''
Each concrete strategy is implemented using a single class with an inheritance from the strategy class, what makes them
looking like plain functions! So let's replace concrete strategies with simple functions.
'''

from collections import Counter
from typing import Sequence, Optional, Callable, Any
# from decimal import Decimal
# from typing import NamedTuple

class Customer(NamedTuple):
    name: str
    fidelity: int

class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self):
        return self.quantity * self.price

class Order(NamedTuple):
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Callable[['Order'], Decimal] | None = None  # promotion takes an Order and returns Decimal

    def total(self):
        return sum([i.total() for i in self.cart], start=Decimal(0))

    def due(self):
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        return f'Total: {self.total()}, Due: {self.due()}'

# Without an abstract class, implement all functions
def fidelity_promo(order: Order) -> Decimal:
    """5% discount for customers with 1000+ fidelity points"""
    if order.customer.fidelity >= 1000:
        return order.total()*Decimal('0.05')
    return Decimal(0)

def bulk_item_promo(order: Order) -> Decimal:
    """10% discount for each LineItem with 20+ units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total()*Decimal('0.1')
    return discount

def large_order_promo(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items"""
    if Counter(order.cart).__len__() >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)

print(Order(stas, cart, fidelity_promo))
print(Order(stas, cart))
print(Order(Customer('Katya', 10000), [LineItem('Jam', 20, Decimal(100))], bulk_item_promo))

# ----------------------------------------------------------------------------------------------------------------------

# Choosing the Best Strategy: Simple Approach

def best_promo(order: Order) -> Decimal:
    """Choosing the best promo for an order"""
    return max(discount(order) for discount in [bulk_item_promo, large_order_promo, fidelity_promo])

print(best_promo(order))

# Although it works and is easy to read, there is some duplication that could lead to a subtle bug: to add a new
# promotion strategy, we need to code the function and remember to add it to the promos list, or else the new promotion
# will work when explicitly passed as an argument to Order, but will not be considered by best_promotion

# ----------------------------------------------------------------------------------------------------------------------

# Finding strategies in a module

# A module in Python is also a first-class object, and the standard library provides several function to handle them.
# The built-in 'globals()' is described as:
"""
globals()
    Return a dictionary representing the current global symbol table. This is always the dictionary of the current 
    module (inside a function or method, this is the module where it is defined, not the module from which it is called)
"""

promos = [promo for name, promo in globals().items()
          if name.endswith('_promo') and
          name != 'best_promo']

print(promos)
print(globals().items())
print(globals())
print(globals()['stas'])
del large_order_promo

# ----------------------------------------------------------------------------------------------------------------------

# Decorator-Enhanced Strategy Pattern
del promos
promos: list[Callable[[Order], Decimal]] = []

def promotion(promo: Callable[[Order], Decimal]) -> Callable[[Order], Decimal]:
    promos.append(promo)
    return promo

def best_promo(order: Order) -> Decimal:
    """Choosing the best promo for an order"""
    return max(promo(order) for promo in promos)

@promotion
def fidelity_promo(order: Order) -> Decimal:
    """5% discount for customers with 1000+ fidelity points"""
    if order.customer.fidelity >= 1000:
        return order.total()*Decimal('0.05')
    return Decimal(0)

@promotion
def bulk_item_promo(order: Order) -> Decimal:
    """10% discount for each LineItem with 20+ units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total()*Decimal('0.1')
    return discount

@promotion
def large_order_promo(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items"""
    if Counter(order.cart).__len__() >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)

print(promos)

# ----------------------------------------------------------------------------------------------------------------------

# The Command Pattern

# Command is another design pattern that can be simplified by the use of functions passed as arguments
# The goal of Command is to decouple an object that invokes an operation from the provider object that implements it.

class MacroCommand:
    """A command that executes a list of commands"""
    def __init__(self, commands: Sequence[Callable]):
        self.commands = list(commands)

    def __call__(self, *args, **kwargs):
        for command in self.commands:
            print(command(*args, **kwargs))

a = MacroCommand([large_order_promo, bulk_item_promo])
a(order)

# More advanced uses of the Command pattern - to support undo, for example - may require more than a simple callback
# function. Even then, Python provides a couple of alternatives that deserve consideration:

# * A callable instance like MarcoCommand can keep whatever state is necessary, and provide extra methods in addition to
# __call__
# * A closure can be used to hold the internal state of a function between calls

def turtle():
    return 'eggs'

print(turtle())
print(turtle.__call__())
print(turtle.__call__.__call__.__call__.__call__())

