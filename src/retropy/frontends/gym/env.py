from ...core.retro import RetroPy
from ...utils.input import GamePadInput

import gymnasium as gym
from gymnasium import spaces

import numpy as np
from typing import Sequence

# gymnasium environment with continuous inputs


class RetroGym(gym.Env):
    def __init__(self, core: str, rom: str, player: int = 1):
        self.player = player

        self.core = RetroPy(core, True)
        self.core.load(rom)

        geometry = self.core.system_av_info().geometry

        obs_shape = (geometry.base_height, geometry.base_width, 3)

        self.observation_space = spaces.Box(0, 255, obs_shape, dtype=np.uint8)
        self.action_space = spaces.Box(0, 1, (self.player, len(GamePadInput)))

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.core.reset()

        observation = self.core.frame_advance()
        info = {}

        return observation, info

    def step(
        self, action: Sequence[Sequence[float]]
    ) -> tuple[np.ndarray, float, bool, bool, dict]:
        # Set input in core
        for player, action in enumerate(action):
            for i, name in enumerate(GamePadInput):
                player[name] = action[i]
        # gym API
        observation = self.core.frame_advance()
        reward = self._reward_function(observation)
        terminated, truncated = self._stopping_criterion()
        info = {}

        return observation, reward, terminated, truncated, info

    # Helper functions

    def _reward_function(self, obs: np.ndarray) -> float:
        reward = 0.0

        return reward

    def _stopping_criterion(self) -> tuple[bool, bool]:
        terminated = False  # Goal reached
        truncated = False  # Timesteps elapsed

        return terminated, truncated
