from enum import IntFlag
from typing import Any

from ..core.device import Device


class InputBitmask(IntFlag):
    B = 1 << 0
    Y = 1 << 1
    SELECT = 1 << 2
    START = 1 << 3
    UP = 1 << 4
    DOWN = 1 << 5
    LEFT = 1 << 6
    RIGHT = 1 << 7
    A = 1 << 8
    X = 1 << 9
    L = 1 << 10
    R = 1 << 11
    L2 = 1 << 12
    R2 = 1 << 13


class PlayerInput:
    joypad: list[int] = [0] * 17
    mouse: list[int] = [0] * 11

    def __getitem__(self, __device: Device) -> Any:
        if __device == Device.JOYPAD:
            return self.joypad
        elif __device == Device.MOUSE:
            return self.mouse
        else:
            raise NotImplementedError()
