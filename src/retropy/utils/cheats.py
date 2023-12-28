from typing import Callable, Iterator


class CheatManager:
    """
    Manages cheat code in accordance with the capabilities provided by libretro's cheat API.

    Upon inspection of common cores implementations, some don't fully utilize the parameters given to the `retro_cheat_set` function i.e. ignore `index` and `enabled`. Therefore, to provide the most universal solution, all added cheats are always enabled and removing a cheat resets all cheats and re-adds the remaining.

    Examples:
        >>> cheats = CheatManager(retro_cheat_set, retro_cheat_reset)
        >>> cheats['name'] = b'code'
        >>> cheats.pop('name')
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
        """Clears cheats after no longer needed."""
        self.store = {}
        self.__index = 0
        self.__reset_cheats()

    def __getitem__(self, name: str) -> bytes:
        """Return code of cheat by name.

        Args:
            name (str): Cheat name

        Returns:
            bytes: Cheat code
        """
        return self.store[name]

    def __setitem__(self, name: str, code: bytes):
        """Adds a new cheat to the core.

        Args:
            name (str): Cheat name. Acts as key.
            code (bytes): Cheat code.

        Raises:
            TypeError: 'code' is not bytes.
            KeyError: 'name' already exists.
        """

        # Check type since object is used with ctypes
        if not isinstance(code, bytes):
            return TypeError("'code' must be a bytes object")

        if self.store.get(name, None):
            raise KeyError(f"Cheat name '{name}' already exists.")

        self.store[name] = code
        self.__add_cheat(code)

    def __iter__(self) -> Iterator[tuple[str, bytes]]:
        """Iterate over all cheat codes.

        Returns:
            list[tuple[str, bytes]]: Iterator over all cheat codes.
        """
        return iter(self.store.items())

    def __repr__(self) -> str:
        return str(self.store)

    def __add_cheat(self, code: bytes):
        self.__index += 1
        self.__update_cheat(self.__index, True, code)

    def pop(self, name: str) -> bytes:
        """Remove cheat code.

        Args:
            name (str): Cheat name.

        Returns:
            bytes: Cheat code.
        """
        self.__reset_cheats()
        code = self.store.pop(name)

        self.__reset_cheats()
        self.__index = 0
        for code in self.store.values():
            self.__add_cheat(code)

        return code
