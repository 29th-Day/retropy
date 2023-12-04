from ctypes import *

from retropy import RetroPy
from env import CORE, GAMES


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


def main():
    core = RetroPy(CORE)

    success = core.load(GAMES[0])

    if not success:
        raise RuntimeError()

    # core.unload()

    for _ in range(100):
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

    core = RetroPyGame(CORE, 2, 1)

    success = core.load(GAMES[0])

    core.run()


if __name__ == "__main__":
    # test1()
    # test2()
    # main()
    pygame()
