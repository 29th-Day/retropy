from ctypes import *
from enum import Enum


class SavestateContext(Enum):
    """retro_savestate_context"""

    NORMAL = 0
    RUNAHEAD_SAME_INSTANCE = 1
    RUNAHEAD_SAME_BINARY = 2
    ROLLBACK_NETPLAY = 3
