# gymnasium wrapper with
# - discrete inputs

from .gym import RetroGym
from ...utils.input import GamePadInput

import gymnasium as gym
from gymnasium import spaces, ActionWrapper

# https://gymnasium.farama.org/tutorials/gymnasium_basics/implementing_custom_wrappers/


class DiscreteInputs(ActionWrapper):
    """
    Map discrete actions into controller inputs.

    Example:
        >>> env = RetroGym(core, rom)
        >>> action_map = [["A"], ["B"], ["LEFT"], ["RIGHT", "A"], ["LEFT_X"]]
        >>> env = DiscreteInputs(env, action_map)
        >>> print(env.action_space) # -> Discrete(5)
    """

    def __init__(self, env: RetroGym, map: list[list[str]]):
        super().__init__(env)
        self.map = map
        self.action_space = spaces.Discrete(len(self.map))

    def action(self, action: int):
        inputs = self.map[action]

        action = [0] * len(GamePadInput)
        for i, input in enumerate(GamePadInput):
            if input in inputs:
                action[i] = 1

        print(action)

        return action
