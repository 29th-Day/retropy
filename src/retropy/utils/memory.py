from ctypes import c_ubyte, POINTER


class InternalMemory:
    def __init__(self, ptr: POINTER(c_ubyte), length: int):
        self.__ptr = ptr
        self.__length = length

    def __len__(self):
        return self.__length

    def __getitem__(self, index: int | slice):
        if isinstance(index, int):
            # Handle negative values
            if index < 0:
                index += self.__length

            # Check bounds
            if index < 0 or index >= self.__length:
                raise IndexError(
                    f"The index ({index}) is out of range for array of length {self.__length}."
                )
        elif isinstance(index, slice):
            # Handle negative/None values
            start = index.start or 0
            stop = index.stop or self.__length - 1
            step = index.step or 1

            start = start + self.__length if start < 0 else start
            stop = stop + self.__length if stop < 0 else stop
            step = abs(step)

            index = slice(start, stop, step)

            # Check bounds
            if (
                (index.start < 0 or index.start >= self.__length)
                or (index.stop >= self.__length or index.stop < index.start)
                or (index.step >= self.__length)
            ):
                raise IndexError(
                    f"The index ({index}) is out of range for array of length {self.__length}."
                )
        else:
            raise TypeError(f"Invalid index type: {type(index)}.")

        return self.__ptr[index]


class RAM:
    save: InternalMemory
    """Save RAM for persistent game data. Usually found on a game cartridge, backed up by a battery."""

    rtc: InternalMemory
    """Some games have a built-in clock to keep track of time."""

    system: InternalMemory
    """Game system's main RAM for actively used game data like characters, levels, and logic."""

    video: InternalMemory
    """Video RAM (VRAM) for displaying sprites, textures, and other graphics data."""

    def __init__(self) -> None:
        self._clear()

    def _clear(self):
        """Cleans memory pointer objects. Needs to be done after game unload."""
        self.save = None
        self.rtc = None
        self.system = None
        self.video = None

    def __repr__(self) -> str:
        return f"{self.save}, {self.rtc}, {self.system}, {self.video}"
