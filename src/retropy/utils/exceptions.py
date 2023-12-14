# exceptions.py


class NoGameLoaded(RuntimeError):
    pass


class GameAlreadyLoaded(RuntimeError):
    pass


class UnknownColorFormat(RuntimeError):
    pass


class GameCannotBeLoaded(RuntimeError):
    pass


class UnkownEnvironmentCommand(RuntimeError):
    pass

class InvalidRomError(OSError):
    pass

class SavestateError(RuntimeError):
    pass