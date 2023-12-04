from ctypes import *
from typing import Callable
from enum import Enum, IntFlag


class FileAccess(IntFlag):
    """RETRO_VFS_FILE_ACCESS_"""

    READ = 1 << 0
    WRITE = 1 << 1
    UPDATE = 1 << 2


class AccessHint(Enum):
    """RETRO_VFS_FILE_ACCESS_HINT_"""

    NONE = 0
    FREQUENT_ACCESS = 1 << 0


class SeekPosition(Enum):
    """RETRO_VFS_SEEK_POSITION_"""

    START = 0
    CURRENT = 1
    END = 2


class StatResult(IntFlag):
    """RETRO_VFS_STAT_IS_"""

    VALID = 1 << 0
    DIRECTORY = 1 << 1
    CHARACTER_SPECIAL = 1 << 2


vfs_get_path_t = CFUNCTYPE(c_char_p, POINTER(VfsFileHandle))
"""retro_vfs_get_path_t"""

retro_vfs_file_handle = CFUNCTYPE(POINTER(VfsFileHandle), ...)


class VfsInterface(Structure):
    _fields_ = [
        ("get_path", c_char_p),
    ]

    get_path: bytes
