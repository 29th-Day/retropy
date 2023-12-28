# exceptions.py


class NoGameLoaded(RuntimeError):
    """An action is called which requires a loaded game."""

    pass


class GameAlreadyLoaded(RuntimeError):
    """Two games cannot be loaded at once."""

    pass


# class UnknownColorFormat(RuntimeError):
#     pass


class GameCannotBeLoaded(RuntimeError):
    """Core rejects provided game file."""

    pass


class UnkownEnvironmentCommand(RuntimeError):
    """Envrionment command used by core is not recognized."""

    pass


class InvalidRomError(OSError):
    """Core rejects provided game file."""

    pass


class SavestateError(RuntimeError):
    """Savestate could not be handled."""

    pass
