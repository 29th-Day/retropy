# Frontends


## Gymnasium

Frontend implementing `gymnasium`'s API (formerly `gym`).

Particularly useful for AI applications, especially in reinforcement learning. Additional details can be found in the [documentation](https://gymnasium.farama.org/ "Gymnasium Documentation").

``` py

from retropy.frontends import RetroPyGym

env = RetroPyGym(dll_path)

terminated, truncated = False, False
obs, info = env.reset()

while not terminated and not truncated:
    action = ...

    obs, reward, terminated, truncated, info = env.step(action)

env.close()

```

## Interactive

If your primary goal is to play retro games, I strongly recommend using player-focused frontends like [RetroArch](https://www.retroarch.com/). Interactive frontends within retropy are implemented to showcase its capabilities and for debugging purposes.

### Pygame

Frontend using pygame. No audio support due to the way pygame handles audio.

``` py
from retropy.frontends import RetroPyGame

core = RetroPyGame(dll_path)

core.load(rom_path)

core.run()

```

### Pyglet

Frontend using pygame. Maybe audio support?

``` py
from retropy.frontends import RetroPyGlet

core = RetroPyGlet(dll_path)

core.load(rom_path)

core.run()

```
