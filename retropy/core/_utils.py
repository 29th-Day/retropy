from ctypes import Array, c_ubyte, c_size_t
from typing import Dict
import os

from ._enums import RETRO_DEVICE

class Savestate():
    data: Array[c_ubyte]
    size: c_size_t

    def __init__(self, size: int = None, path: str = None):
        if not size is None:
            self.size = c_size_t(size)
            self.data = (c_ubyte * size)()
        elif not path is None:
            self.load(path)
        else:
            raise ValueError("Either `size` or `path` must not be None")

    def save(self, path: str):
        with open(path, "wb") as f:
            f.write(self.data)

    def load(self, path: str):
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            self.size = f.tell()
            f.seek(0, os.SEEK_SET)
            self.data = (c_ubyte * self.size).from_buffer_copy(f.read())

class PlayerInput():
    port: int
    device: RETRO_DEVICE
    actions: Dict[int, int]

    def __init__(self, port: int = 0, device: RETRO_DEVICE = RETRO_DEVICE.JOYPAD) -> None:
        self.port = port
        self.device = device
        self.actions = {}
