from enum import IntFlag
from typing import Any

from ..core.device import Device, Joypad, Analog

class Controller:
    state: dict
    
    def get_state(self, index: int, id: int):
        raise NotImplementedError()
    
    def set_state(self, index: int, id: int, value: int):
        raise NotImplementedError()

class ButtonController(Controller):
    state = [0] * len(Joypad)
    
    def get_state(self, index: int, id: int):
        return self.state[id]
    
    def set_state(self, index: int, id: int, value: int):
        self.state[id] = value
    
class AxesController(Controller):
    state = {
        Analog.IDX_LEFT: [0, 0],
        Analog.IDX_RIGHT: [0, 0],
        Analog.IDX_BUTTON: [0] * len(Joypad)
    }
    
    def get_state(self, index: int, id: int):
        return self.state[index][id]
    
    def set_state(self, index: int, id: int, value: int):
        self.state[index][id] = value

def device_to_controller(device: Device) -> Controller:
    if device == Device.NONE:
        raise ValueError(f"{device} is not supported")
    elif device == Device.JOYPAD:
        return ButtonController()
    elif device == Device.ANALOG:
        return AxesController()
