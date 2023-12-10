from ..core.device import Device, Joypad, Analog

class Gamepad:
    state: dict
    
    def __init__(self) -> None:
        self.reset()
    
    def get_state(self, device: Device, index: int, id: int):
        return self.state[device][index][id]
    
    def set_state(self, device: Device, index: int, id: int, value: int):
        self.state[device][index][id] = value
    
    def reset(self):
        self.state = {
            Device.JOYPAD: ([0] * len(Joypad),), # wrap in tuple to account for index
            Device.ANALOG: {
                Analog.LEFT_STICK: [0, 0],
                Analog.RIGHT_STICK: [0, 0],
                Analog.BUTTONS: [0] * len(Joypad)
            }
        }
        
        # print(self.state)
