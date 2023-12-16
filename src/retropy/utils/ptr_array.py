from __future__ import annotations

from ctypes import *
from ctypes import _Pointer
from typing import TypeVar, Callable

try:
    import numpy as np
except ImportError:
    # np = None
    pass

T = TypeVar("T")


def foreach(array: _Pointer[T], cond: Callable[[T], bool]):
    i = 0
    v: T = array[i]
    while cond(v):
        yield v
        i += 1
        v = array[i]
