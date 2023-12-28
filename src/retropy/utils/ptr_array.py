from __future__ import annotations

from ctypes import _Pointer
from typing import TypeVar, Callable

T = TypeVar("T")


# -> T (adding this destroys type inference (VSCODE 12-23), so it is dropped)
def foreach(array: _Pointer[T], cond: Callable[[T], bool]):
    """Loop of arbitrary terminated C array.

    Args:
        array (_Pointer[T]): C array
        cond (Callable[[T], bool]): terminate condition

    Yields:
        T: element of array

    Examples:
        >>> # Iterate over NULL terminated array
        >>> for e in foreach(c_array, lambda e: e):
        >>>     print(e)
    """
    i = 0
    v: T = array[i]
    while cond(v):
        yield v
        i += 1
        v = array[i]
