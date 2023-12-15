# Resolve relative import
from pathlib import Path
import sys

sys.path.append(str((Path(__file__) / ".." / ".." / "src").resolve()))

from retropy import RetroPy
from env import SYSTEMS
from ctypes import *

import numpy as np


def test1():
    from retropy.core.environment import CoreVariable

    def func(data: c_void_p):
        data = cast(data, POINTER(CoreVariable)).contents
        data.value = b"456"

    v = CoreVariable(key=b"okay", value=b"123")
    print(v.value)

    func(byref(v))

    print(v.value)


def test2():
    def func(data: c_void_p):
        data = cast(data, POINTER(c_bool)).contents
        data.value = True

    v = c_bool(False)
    print(v)

    func(byref(v))

    print(v)


def test3():
    from enum import Enum

    class DefaultEnum(Enum):
        UNKNOWN = 0
        A = 1
        B = 2
        C = 3

        @classmethod
        def _missing_(cls, _):
            return cls.UNKNOWN

    print(DefaultEnum(1))
    print(DefaultEnum(123123))


def test4():
    from retropy.core.environment import EnvironmentCommand

    for cmd in EnvironmentCommand:
        print(f"EnvironmentCommand.{cmd.name}: self.env_{cmd.name},")


class Test5:
    def __init__(self) -> None:
        self.funcs = {0: self.func}

    def func(self):
        print("Test5")


class Super(Test5):
    def __init__(self) -> None:
        super().__init__()
        # self.funcs[0] =

    def func(self):
        print("Super")


def test5():
    s = Super()
    s.funcs[0]()


def test6():
    import io

    bytes = io.BytesIO()

    bytes.write(b"1234")
    bytes.seek(0)
    bytes.write(b"5678")

    len = bytes.seek(0, 2)
    print(len, bytes.getvalue().decode("utf-8"))

    bytes.truncate(4)

    len = bytes.seek(0, 2)
    print(len, bytes.getvalue().decode("utf-8"))


dll, game = SYSTEMS["GBA"]


def main():
    core = RetroPy(dll)

    core.load(game)

    for _ in range(1):
        core.frame_advance()

    save = core.save_state()

    save.write("./savestate.svt")

    core.reset()

    core.load_state(save)


def pygame():
    from retropy.frontends import RetroPyGame

    core = RetroPyGame(dll, 3)

    core.load(game)

    core.run()


def pyglet():
    from retropy.frontends import RetroPyGlet

    core = RetroPyGlet(dll, 3)

    core.load(game)

    core.run()


if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # test6()
    # main()
    # pygame()
    pyglet()
