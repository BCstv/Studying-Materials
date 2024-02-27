# Function decorators let us "mark" functions in the source code to enhance their behavior in some way.

# The most obscure reserved keyword in Python is nonlocal

# To implement your own decorator functions in Python you have must understand closures, and then the need for
# nonlocal
# becomes obvious!


# ----------------------------------------------------------------------------------------------------------------------

# Decorators 101
# A decorator is a callable that takes another function as an argument (the decorated function)
# it may perform some processing with the decorated function, and returns it or replaces it with another function or
# callable object

# In other words, assuming an existing decorator named decorate, this code:
"""
@decorate
def target():
    print('running target()')

has the same effect as writing this:

def target():
    print('running target()')
target = decorate(target)
"""


# The end result is the same: at the end of either of these snippets, the target name is bound to whatever function is
# returned by decorate(target) - which may be the function initially named target, or may be a different function

def deco(func):
    def inner():
        print('Running inner()')

    return inner  # deco returns its inner function object


@deco
def target():  # target is decorated by deco
    print('running target()')


target()  # Invoking the decorated target() actually runs inner
# Running inner()

print(target)  # Inspection reveals that target is a now a reference to inner
# <function deco.<locals>.inner at 0x000001D08E4122A0>

# Strictly speaking, decorators are just syntactic sugar. As we just saw, you can always simply call a decorator like any
# regular callable, passing another function. Sometimes that is actually convenient, especially when doing
# metaprogramming - changing program behaviour at runtime

'''
1 - A decorator is a function or another callable
2 - A decorator may replace the decorated function with a different one
3 - Decorators are executed immediately when a module is based
'''
# ----------------------------------------------------------------------------------------------------------------------
#                                       WHEN PYTHON EXECUTES DECORATORS
# ----------------------------------------------------------------------------------------------------------------------

registry = []  # It will hold references to functions decorated by @register


def register(func):  # register takes a function as an argument
    print(f'Running register ({func.__name__})')  # Display what function is being decorated, for demonstration
    registry.append(func)  # Include func in registry
    return func  # Return func: we must return a function; here we return the same received as argument


@register  # f1 and f2 are decorated by @register
def f1():
    print('running f1()')


@register
def f2():
    print('running f2()')


def f3():  # f3 is not decorated
    print('running f3()')


def main():  # main displays the registry, then calls f1(), f2(), and f3()
    print('running main()')
    print('registry -> ', registry)
    f1()
    f2()
    f3()


if __name__ == '__main__':
    main()  # main() is only invoked if registration.py runs as a script

'''
Note that register runs twice before any other function in the module. When register is called, it receives the decorated
function object as an argument - for example: Running register (f1)
'''


# So, at a runtime, decorators are being executed as soon as they are imported, and functions only when they are invoked

# ----------------------------------------------------------------------------------------------------------------------

# Registration Decorators

# The decorator function is defined in the same module as the decorated functions. A real decorator is usually defined in
# one module and applied to functions in other modules.

# The register decorator returns the same function passed as an argument. In practice, most decorators define an inner
# function and return it.

# Most decorators do change the decorated function. They usually do it by defining an inner function and returning it to
# replace the decorated function. Code that uses inner function almost always depends on closures to operate correctly.

# ----------------------------------------------------------------------------------------------------------------------

# Variable Scope Rules

def f1(a):
    print(a)
    print(b)


# Unresolved reference 'b'
a = 'I was here since the start'
b = 'I was here since the start too'
f1('I was given')


def f2(a):
    print(a)
    print('It used to be b variable here')  # Cannot access local variable 'b' where it is not associated with a value
    b = "I'm sitting in the function"


f2(1)

# Note that the output starts with 3, which proves that the print(a) statement was executed. But the second one, print(b)
# never runs! When I first saw this I was surprised, thinking that 6 should be printed, because there is a global variable
# b and the assignment to the local b is made after print(b)

'''
But the fact is, when Python compiles the body of the function, it decides that b is a local variable because it is 
assigned within the function. The generated bytecode reflects this decision and will try to fetch b from the local scope.
Later, when the call f2(3) is made, the body of f2 fetches and prints the value of the local variable a, but when trying
to fetch the value of local variable b, it discovers that b is unbound.
'''

# This is not a bug, but a design choice: Python does not require you to declare variables, but assumes that a variable
# assigned in the body of a function is a local. This is much better that the behaviour of JS, which does not require
# variable declarations either, but if you do forget to declare that a variable is local (with var), you may clobber a
# global variable without knowing

# If we want the interpreter to treat b as a global variable and still assign a new value to it within the function,
# we use the global declaration:
del b

print('New right function: ')
b = 'I was here since the start too'


def f3(a):
    global b
    print(a)
    print(b)
    _b = 'I was sitting in the function'
    print(_b)


f3('I was given')

print('And now b =', b)

from dis import dis  # The dis module provides an easy way to disassemble the bytecode of Python functions

print(dis(f1))

"""
112           0 RESUME                   0

113           2 LOAD_GLOBAL              1 (NULL + print)
             12 LOAD_FAST                0 (a)
             14 CALL                     1
             22 POP_TOP

114          24 LOAD_GLOBAL              1 (NULL + print)
             34 LOAD_GLOBAL              2 (b)
             44 CALL                     1
             52 POP_TOP
             54 RETURN_CONST             0 (None)
None
"""

print(dis(f2))
"""
121           0 RESUME                   0

122           2 LOAD_GLOBAL              1 (NULL + print)
             12 LOAD_FAST                0 (a)
             14 CALL                     1
             22 POP_TOP

123          24 LOAD_GLOBAL              1 (NULL + print)
             34 LOAD_CONST               1 ('It used to be b variable here')
             36 CALL                     1
             44 POP_TOP

124          46 LOAD_CONST               2 ("I'm sitting in the function")
             48 STORE_FAST               1 (b)
             50 RETURN_CONST             0 (None)
None
"""

print(dis(f3))
"""
150           0 RESUME                   0

152           2 LOAD_GLOBAL              1 (NULL + print)
             12 LOAD_FAST                0 (a)
             14 CALL                     1
             22 POP_TOP

153          24 LOAD_GLOBAL              1 (NULL + print)
             34 LOAD_GLOBAL              2 (b)
             44 CALL                     1
             52 POP_TOP

154          54 LOAD_CONST               1 ('I was sitting in the function')
             56 STORE_FAST               1 (_b)

155          58 LOAD_GLOBAL              1 (NULL + print)
             68 LOAD_FAST                1 (_b)
             70 CALL                     1
             78 POP_TOP
             80 RETURN_CONST             0 (None)
None
"""


# ----------------------------------------------------------------------------------------------------------------------

# Closures

# A closure is a function - let's call it f - with an extended scope that encompasses variables referenced in the body
# of f that are not global variables or local variables of f. Such variables must come from the local scope of an outer
# function that encompasses f

class Averager:
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        return sum(self.series) / len(self.series)


avg = Averager()
print(avg(10))
print(avg(11))
print(avg(12))


# It does not matter whether the function is anonymous or not; what matters is that it can access non-global variables
# that are defined outside its body

def make_averager():
    series = []                           # --
                                        #    |
    def averager(new_value):               # |
        series.append(new_value)           # |  <- Closure
        return sum(series) / len(series)   # |
                                        #    |
    return averager  #                      --
# series is a free variable

dosi = make_averager()
print(dosi(12))
print(dosi(15))

# The same function would not work with free variables of immutable types, because we can never reassign them. Only read
# Because f.e. counter += 1 is counter = counter + 1, what means that we are redeclaring a variable

# ----------------------------------------------------------------------------------------------------------------------

# The nonlocal Declaration

def make_averager():
    count = 0
    total = 0

    def avereger(new_value):
        count += 1
        total += new_value
        return total / count
    return avereger

del make_averager

def make_averager():
    count = 0
    total = 0

    def avereger(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    return avereger


# Variable Lookup Logic

# When a function is defined, the Python bytecode compiler determines how to fetch a variable x that appears in it,
# based on these rules
'''
* If there is a global x declaration, x comes from and is assigned to the x global variable module
* If there is a nonlocal x declaration, x comes from and is assigned to the x local variable of the nearest surrounding
function where x is defined
* If x is a parameter or is assigned a value in the function body, then x is the local variable
* If x is referenced but is not assigned and is not a parameter:
    - x will be looked up in the local scopes of the surrounding function bodies (nonlocal scopes)
    - If not found in surrounding scopes, it will be read from the module global scope
    - If not found in the global scope, it will be read from __builtins__.__dict__
'''

# ----------------------------------------------------------------------------------------------------------------------

# Implementing a Simple Decorator

import time
def clock(func):
    def clocked(*args):  # Define inner function clocked to accept any number of positional arguments
        t0 = time.perf_counter()
        result = func(*args)  # This line only works because the closure for clocked encompasses the func free variable
        elapsed = time.perf_counter() - t0
        arg_str = ', '.join(repr(arg) for arg in args)
        print(f'[{elapsed:0.8f}] {func.__name__}({arg_str}) -> {result!r}')
    return clocked  # Return the inner function to replace the decorated function

@clock
def snooze(seconds):
    time.sleep(seconds)


def factorial(n: int) -> int:
    return n if n <= 2 else n * factorial(n - 1)


print('*' * 40, 'Calling snooze(.123)')
snooze(.123)
print('*' * 40, 'Calling factorial(6)')
print('6! = ', clock(factorial(6)))

# ----------------------------------------------------------------------------------------------------------------------





