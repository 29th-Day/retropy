from ctypes import Array, c_ubyte, c_size_t
import os

class Savestate():
    data: Array[c_ubyte]
    size: c_size_t

    def __init__(self, size: int = None):
        if size:
            self.size = c_size_t(size)
            self.data = (c_ubyte * size)()
        else:
            self.size = None

    def save(self, path: str):
        with open(path, "wb") as f:
            f.write(self.data)

    def load(self, path: str):
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            self.size = f.tell()
            f.seek(0, os.SEEK_SET)
            self.data = (c_ubyte * self.size).from_buffer_copy(f.read())
            
        return self
