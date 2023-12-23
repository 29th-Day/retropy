from ...core.retro import RetroPy
from ...utils.input import GamePadInput

import gymnasium as gym
from gymnasium import spaces

import numpy as np
from typing import Sequence

# gymnasium environment with continuous inputs

# https://gymnasium.farama.org/api/spaces/fundamental/#gymnasium.spaces.MultiDiscrete


class RetroGym(gym.Env):
    def __init__(self, core: str, rom: str):
        self.core = RetroPy(core, True)
        self.core.load(rom)

        geometry = self.core.system_av_info().geometry

        obs_shape = (geometry.base_height, geometry.base_width, 3)

        self.observation_space = spaces.Box(0, 255, obs_shape, dtype=np.uint8)
        self.action_space = spaces.Box(0, 1, (len(GamePadInput),))

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.core.reset()

        observation = self.core.frame_advance()
        info = {}

        return observation, info

    def step(
        self, action: Sequence[float]
    ) -> tuple[np.ndarray, float, bool, bool, dict]:
        self.__set_controller_input(action)

        observation = self.core.frame_advance()
        reward = self._reward_function(observation)
        terminated, truncated = self._stopping_criterion()
        info = {}

        return observation, reward, terminated, truncated, info

    # Helper function

    def __set_controller_input(self, action):
        for input, value in zip(GamePadInput, action):
            self.core.controllers[0][input] = value

    # RL functions

    def _reward_function(self, observation: np.ndarray) -> float:
        raise NotImplementedError()

    def _stopping_criterion(self) -> tuple[bool, bool]:
        raise NotImplementedError()
