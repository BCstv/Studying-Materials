"""
For large programs you need more disciplined approach. And it helps if the language gives you that discipline rather
than telling you "Well, you can do whatever you want"
"""
from typing import overload, TypeVar, Union
import functools
import operator
from collections.abc import Iterable

T = TypeVar('T')
S = TypeVar('S')  # We need this second TypeVar in the second overload
@overload
def sum(it: Iterable[T]) -> Union[T, int]: ...  # This signature is for the simple case: sum(my_iterable). The result
# type may be T

@overload
def sum(it:Iterable[T], /, start: S) -> Union[T, S]: ...

print(help(TypeVar))

# Page 521

