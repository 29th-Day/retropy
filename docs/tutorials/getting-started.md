# Getting started

<!--
## Basics

``` py
from retropy import RetroPy

core = RetroPy(dll_path)         # load core

core.load(rom_path)              # load game

for _ in range(1):
    frame = core.frame_advance() # run emulator for one frame
```
-->

## Load core

``` py
from retropy import RetroPy
```

## Load game

...

## Run core

## Input

``` py

from retropy import Device, Joypad, Analog

...

player = 0
core.controller[player].set_state(Device.JOYPAD, 0, Joypad.A, 1)
core.controller[player].set_state(Device.ANALOG, Analog.LEFT_STICK, Analog.X, 0x9FFF)

```

## Savestates

``` py
from retropy.utils.savestate import Savestate

...

save = core.save_state()            # create a savestate

save.write("./save.svt")            # write savestate to file

core.reset()                        # reset core

del save                            # delete savestate for demonstrational purposes

save = Savestate().load("save.svt") # load savestate from file

core.load_state(save)               # load previous savestate

```
## Complete code

``` py
from retropy import RetroPy

core = RetroPy(dll_path)

core_info = core.system_info()

core.load(rom_path)

game_info = core.system_av_info()

for _ in range(1):
    frame = core.frame_advance()


```
