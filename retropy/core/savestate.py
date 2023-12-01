# libretro.h

from ctypes import *
from enum import IntEnum
from typing import Callable

# region 3213 - 3240

class SAVESTATE_CONTEXT(IntEnum):
    NORMAL = 0
    RUNAHEAD_SAME_INSTANCE = 1
    RUNAHEAD_SAME_BINARY   = 2
    ROLLBACK_NETPLAY       = 3
    
# endregion
