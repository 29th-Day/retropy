# Resolve relative import
from pathlib import Path
import sys

sys.path.append(str((Path(__file__) / ".." / ".." / "src").resolve()))

from retropy import RetroPy
from env import SYSTEMS
from ctypes import *

import numpy as np


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


def gym():
    from retropy.frontends import RetroGym

    env = RetroGym(dll, game)


def test():
    ...


if __name__ == "__main__":
    # test()
    # main()
    # pygame()
    # pyglet()
    gym()
