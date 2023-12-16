# Tutorials

## Gettings started

``` py
from retropy import RetroPy

dll_path = "..."            # path to libretro core
rom_path = "..."            # path to valid rom

core = RetroPy(dll)         # load core

core.load(rom_path)         # load game

for _ in range(1):
    core.frame_advance()    # run emulator for one frame

save = core.save_state()    # create a savestate

save.write("./save.svt")    # write savestate to binary object

core.reset()                # reset core

core.load_state(save)       # load previous savestate

```
