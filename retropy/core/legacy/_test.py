# from enum import IntFlag, auto

# class InputMask(IntFlag):
#     B = auto()
#     Y = auto()
#     SELECT = auto()
#     START = auto()
#     UP = auto()
#     DOWN = auto()
#     LEFT = auto()
#     RIGHT = auto()
#     A = auto()
#     X = auto()
#     L = auto()
#     R = auto()
#     L2 = auto()
#     R2 = auto()

# mask = InputMask(0)

# mask |= InputMask.A
# mask |= InputMask.B

# print(f"{mask:016b}")

# mask &= ~InputMask.A

# print(f"{mask:016b}")

# -------------------

from ctypes import *

def compare_function(a, b):
    print("cmp", a[0], b[0])
    return 0

callback_t = CFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int))

class Test:
    def __init__(self) -> None:
        self.libc = cdll.msvcrt
        
        self.a = (c_int * 5)(5, 1, 7, 33, 99)
        
        self.qsort = self.libc.qsort
        self.qsort.restype = None
        
        self.callback = callback_t(self.compare_function)
    
    def compare_function(self, a, b):
        print("cmp", a[0], b[0])
        # return 0
        return a[0] - b[0]
    
    def sort(self):
        a = self.a
        self.qsort(a, len(a), sizeof(c_int), self.callback)
        
        for i in a: print(i, end=" ")

t = Test()
t.sort()
