from ctypes import *

from retropy import RetroPy
from env import CORES, GAMES


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
    libc = cdll.msvcrt
    libc.printf(b"Okay")


def main():
    system = "N64"

    core = RetroPy(CORES[system])

    success = core.load(GAMES[system])

    if not success:
        raise RuntimeError()

    # core.unload()

    for _ in range(1):
        core.frame_advance()

    save = core.saveState()

    if not save:
        raise RuntimeError()

    core.reset()

    success = core.loadState(save)

    if not success:
        raise RuntimeError()


def pygame():
    from retropy.frontends import RetroPyGame

    core = RetroPyGame(CORES["GBA"], 1, 30)

    success = core.load(GAMES["GBA"])

    core.run()


if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    main()
    # pygame()
