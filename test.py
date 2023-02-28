from enum import IntFlag, auto

class InputMask(IntFlag):
    B = auto()
    Y = auto()
    SELECT = auto()
    START = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    A = auto()
    X = auto()
    L = auto()
    R = auto()
    L2 = auto()
    R2 = auto()

mask = InputMask(0)

mask |= InputMask.A
mask |= InputMask.B

print(f"{mask:016b}")

mask &= ~InputMask.A

print(f"{mask:016b}")
