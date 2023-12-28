from ctypes import Array, c_ubyte, c_size_t
import os


class Savestate:
    """Saves complete state of emulator to later return to."""

    data: Array[c_ubyte]
    """Emulator state in bytes as ctypes array"""
    size: c_size_t
    """Length of `data`"""

    def __init__(self, size: int = None):
        """Initialized a savestate.

        Args:
            size (int, optional): Number of bytes of buffer. Defaults to None.
        """
        if size:
            self.size = c_size_t(size)
            self.data = (c_ubyte * size)()
        else:
            self.size = None

    def write(self, path: str):
        """Write savestate to file

        Args:
            path (str): Path to file
        """
        with open(path, "wb") as f:
            f.write(self.data)

    def read(self, path: str) -> "Savestate":
        """Read savestate from file

        Args:
            path (str): Path to file

        Returns:
            Savestate: loaded state information
        """
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            self.size = f.tell()
            f.seek(0, os.SEEK_SET)
            self.data = (c_ubyte * self.size).from_buffer_copy(f.read())

        return self
