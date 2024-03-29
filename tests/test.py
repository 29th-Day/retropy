# Resolve relative import
from pathlib import Path
import sys

sys.path.append(str((Path(__file__) / ".." / ".." / "src").resolve()))

from retropy import RetroPy
from env import SYSTEMS
from ctypes import *

import numpy as np


dll, game = SYSTEMS["NES"]


def main():
    core = RetroPy(dll)

    core.load(game)

    for _ in range(100):
        core.frame_advance()

    print(core.memory.system[0x7F0:0x7FF])
    print(core.memory.system[-16:])

    # save = core.save_state()

    # save.write("./savestate.svt")

    # core.reset()

    # core.load_state(save)


def pygame():
    from retropy.frontends.pygame import RetroPyGame

    core = RetroPyGame(dll, 3)

    core.load(game)

    core.cheats["9 Lives"] = b"AATOZE"
    core.cheats.pop("9 Lives")

    core.run()


def pyglet():
    from retropy.frontends.pyglet import RetroPyGlet

    core = RetroPyGlet(dll, 3)

    core.load(game)

    core.run()


def gym():
    from retropy.frontends.gym import RetroGym
    from retropy.frontends.gym.wrapper import DiscreteInputs

    env = RetroGym(dll, game)

    map = [["A"], ["B"], ["UP"], ["DOWN"], ["LEFT"], ["RIGHT"]]
    env = DiscreteInputs(env, map)
    print(env.observation_space)
    print(env.action_space)

    obs, info = env.reset()

    done = False

    while not done:
        action = env.action_space.sample()
        print(action)

        obs, reward, term, trunc, info = env.step(action)
        done = term or trunc

        break


def test():
    l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    list

    print(l[-2:])


if __name__ == "__main__":
    # test()
    # main()
    pygame()
    # pyglet()
    # gym()
