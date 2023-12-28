from typing import Callable
from ctypes import c_uint, c_bool, c_char_p


class Cheat:
    __index: int
    """Apperently intended to be used as an identifier. Many cores just dont use this. No significance for the user."""
    __enabled: bool
    """Whether cheat is enabled."""
    __code: bytes
    """Cheat code content."""

    __update_cheat: Callable = None

    def __init__(
        self, index: int, enabled: bool, code: bytes, update: Callable
    ) -> None:
        self.__index = index
        self.__enabled = enabled
        self.__code = code
        self.__update_cheat = update

        self.__update()

    def __repr__(self) -> str:
        return f"Cheat: {{ {self.__enabled}, {self.__code.decode()} }}"

    def __update(self):
        self.__update_cheat(
            c_uint(self.__index), c_bool(self.__enabled), c_char_p(self.__code)
        )

    @property
    def code(self):
        return self.__code

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, val: bool):
        self.__enabled = val
        print(self.__enabled)
        self.__update()


class _CheatManager:
    """Manages cheat code in accordance with the capabilities provided by libretro's cheat API."""

    store: dict[str, Cheat]

    __update_cheat: Callable[[int, bool, bytes], None] = None
    __reset_cheat: Callable[[None], None] = None

    def __init__(self, update: Callable, reset: Callable) -> None:
        self.__update_cheat = update
        self.__reset_cheat = reset
        self._clear()

    def __iter__(self):
        return self.store.items()

    def add(self, name: str, code: str | bytes, enabled: bool = True):
        """Add a cheat code.

        Args:
            name (str): Name of cheat code. Used as unique key.
            code (str | bytes): Cheat code.
            enabled (bool, optional): Whether cheat is enabled. Defaults to True.
        """

        self.__index += 1
        self.store[name] = Cheat(
            self.__index,
            enabled,
            code if isinstance(code, bytes) else code.decode(),
            self.__update_cheat,
        )

        print(self.store[name])

    def __getitem__(self, name: str):
        return self.store[name]

    def _clear(self):
        self.store = {}
        self.__index = 0
        self.__reset_cheat()


class CheatManager:
    """
    Manages cheat code in accordance with the capabilities provided by libretro's cheat API.

    Upon inspection of common cores implementations, some don't fully utilize the parameters given to the `retro_cheat_set` function i.e. ignore `index` and `enabled`. Therefore, to provide the most universal solution, all added cheats are always enabled and removing a cheat resets all cheats and re-adds the remaining.
    """

    store: dict[str, bytes]
    __index: int
    __update_cheat: Callable[[int, bool, bytes], None]
    __reset_cheats: Callable[[None], None]

    def __init__(self, update: Callable, reset: Callable) -> None:
        self.__update_cheat = update
        self.__reset_cheats = reset
        self._clear()

    def _clear(self):
        self.store = {}
        self.__index = 0
        self.__reset_cheats()

    def __getitem__(self, name: str):
        return self.store[name]

    def __setitem__(self, name: str, code: bytes):
        # Check type since object is used with ctypes
        if not isinstance(code, bytes):
            return TypeError("'code' must be a bytes object")

        self.store[name] = code
        self.__add_cheat(code)

    def __iter__(self):
        return self.store.items()

    def __repr__(self) -> str:
        return str(self.store)

    def __add_cheat(self, code: bytes):
        self.__index += 1
        self.__update_cheat(self.__index, True, code)

    def pop(self, name: str):
        self.__reset_cheats()
        code = self.store.pop(name)

        self.__reset_cheats()
        self.__index = 0
        for code in self.store.values():
            self.__add_cheat(code)

        return code
