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
    buffer = np.zeros((8, 2), dtype=np.int16)

    len = 2
    for i in range(0, len * 10, len):
        data = np.stack([np.arange(i, i + len)] * 2).transpose()

        buffer = np.roll(buffer, -len, axis=0)
        buffer[-len:] = data

        print(buffer)


if __name__ == "__main__":
    # test()
    # main()
    # pygame()
    pyglet()
    # gym()
