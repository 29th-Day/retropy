from ..libretro import LibRetro, LibRetroOption
from ..enums import RETRO_INPUT_JOYPAD

import numpy as np
import gymnasium as gym
from gymnasium import spaces

class RetroEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, core: str, settings: str, rom: str, actions: int) -> None:
        
        core: LibRetro = LibRetro(core, LibRetroOption(path=settings))
        core.load_game(path=rom)
        frames = core.get_system_av_info().geometry

        self.observation_space = spaces.Box(0, 255, (frames.base_height, frames.base_width), dtype=np.uint8)
        self.action_space = spaces.Discrete(actions)

    def reset(self, *, seed: int = None, options) -> np.ndarray:
        super().reset(seed=seed, options=options)

    