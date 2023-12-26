# Gym is made for single agents envs, therefore only one player is supported
# MAYBE a multi agent version (likly following PettingZoo's API) will be made eventually

# from gymnasium.envs.registration import register

# register(id="retropy/RetroGym-v0", entry_point="retropy.frontends.gym.gym:RetroGym")

from .gym import RetroGym
