from ...core.device import Device, Joypad, Analog, AnalogIdx
from .base import InputDevice

from enum import StrEnum


class GamePadInput(StrEnum):
    """Based on the Nintendo© button layout"""

    LEFT_X = "LEFT_X"
    """Left Control Stick - Horizontal ↔"""
    LEFT_Y = "LEFT_Y"
    """Left Control Stick - Vertical ↕"""
    RIGHT_X = "RIGHT_X"
    """Right Control Stick - Horizontal ↔"""
    RIGHT_Y = "RIGHT_Y"
    """Right Control Stick - Vertical ↕"""
    B = "B"
    """B Button"""
    Y = "Y"
    """Y Button"""
    START = "START"
    """START Button"""
    SELECT = "SELECT"
    """SELECT Button"""
    UP = "UP"
    """Directional Pad - Up ↑"""
    DOWN = "DOWN"
    """Directional Pad - Down ↓"""
    LEFT = "LEFT"
    """Directional Pad - Left →"""
    RIGHT = "RIGHT"
    """Directional Pad - Right ←"""
    A = "A"
    """A Button"""
    X = "X"
    """X Button"""
    L1 = "L1"
    """Left Shoulder Button"""
    R1 = "R1"
    """Right Shoulder Button"""
    L2 = "L2"
    """Left Shoulder Trigger"""
    R2 = "R2"
    """Right Shoulder Trigger"""
    L3 = "L3"
    """Left Control Stick - Press"""
    R3 = "R3"
    """Right Control Stick - Press"""


class GamePad(InputDevice):
    threshold: float = 0.5

    def get_state(self, device: int, index: int, id: int) -> int:
        if device == Device.JOYPAD:
            # this is done as a hack to keep the dict smaller
            name = RETRO_INPUT_TO_STR[AnalogIdx.BUTTONS][id]

            # (-inf, threshold]: 0
            # ( threshold, inf): 1
            return int(self.state[name] > self.threshold)

        elif device == Device.ANALOG:
            name = RETRO_INPUT_TO_STR[index][id]

            # [-0x7FFF, 0x7FFF]
            return int(self.state[name] * 0x7FFF)
        else:
            raise ValueError(f"device ({device})")

    def reset(self):
        self.state = {
            GamePadInput.LEFT_X: 0.0,
            GamePadInput.LEFT_Y: 0.0,
            GamePadInput.RIGHT_X: 0.0,
            GamePadInput.RIGHT_Y: 0.0,
            GamePadInput.B: 0,
            GamePadInput.Y: 0,
            GamePadInput.START: 0,
            GamePadInput.SELECT: 0,
            GamePadInput.UP: 0,
            GamePadInput.DOWN: 0,
            GamePadInput.LEFT: 0,
            GamePadInput.RIGHT: 0,
            GamePadInput.A: 0,
            GamePadInput.X: 0,
            GamePadInput.L1: 0,
            GamePadInput.R1: 0,
            GamePadInput.L2: 0,
            GamePadInput.R2: 0,
            GamePadInput.L3: 0,
            GamePadInput.R3: 0,
        }

        # print(self.state)


RETRO_INPUT_TO_STR = {
    AnalogIdx.LEFT_STICK: {
        Analog.X: GamePadInput.LEFT_X,
        Analog.Y: GamePadInput.LEFT_Y,
    },
    AnalogIdx.RIGHT_STICK: {
        Analog.X: GamePadInput.RIGHT_X,
        Analog.Y: GamePadInput.RIGHT_Y,
    },
    AnalogIdx.BUTTONS: {
        Joypad.B: GamePadInput.B,
        Joypad.Y: GamePadInput.Y,
        Joypad.SELECT: GamePadInput.SELECT,
        Joypad.START: GamePadInput.START,
        Joypad.UP: GamePadInput.UP,
        Joypad.DOWN: GamePadInput.DOWN,
        Joypad.LEFT: GamePadInput.LEFT,
        Joypad.RIGHT: GamePadInput.RIGHT,
        Joypad.A: GamePadInput.A,
        Joypad.X: GamePadInput.X,
        Joypad.L: GamePadInput.L1,
        Joypad.R: GamePadInput.R1,
        Joypad.L2: GamePadInput.L2,
        Joypad.R2: GamePadInput.R2,
        Joypad.L3: GamePadInput.L3,
        Joypad.R3: GamePadInput.R3,
    },
}
