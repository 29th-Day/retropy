from ctypes import *
from typing import Callable
from enum import Enum, IntFlag

raise NotImplementedError(
    "VFS is not implemented. Only structure is ported, no functionability."
)


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


class VfsFileHandle(Structure):
    _fields_ = [
        # ('name', c_char_p),
    ]

    # name: bytes


class VfsDirHandle(Structure):
    _fields_ = [
        # ('name', c_char_p),
    ]

    # name: bytes


vfs_get_path_t = CFUNCTYPE(c_char_p, POINTER(VfsFileHandle))
"""retro_vfs_get_path_t"""

vfs_open_t = CFUNCTYPE(POINTER(VfsFileHandle), c_char_p, c_uint, c_uint)
"""retro_vfs_open_t"""

vfs_close_t = CFUNCTYPE(c_int, POINTER(VfsFileHandle))
"""retro_vfs_close_t"""

vfs_size_t = CFUNCTYPE(c_int64, POINTER(VfsFileHandle))
"""retro_vfs_size_t"""

vfs_truncate_t = CFUNCTYPE(c_int64, POINTER(VfsFileHandle), c_int64)
"""retro_vfs_truncate_t"""

vfs_tell_t = CFUNCTYPE(c_int64, POINTER(VfsFileHandle))
"""retro_vfs_tell_t"""

vfs_seek_t = CFUNCTYPE(c_int64, POINTER(VfsFileHandle), c_int64, c_int)
"""retro_vfs_seek_t"""

vfs_read_t = CFUNCTYPE(c_int64, POINTER(VfsFileHandle), c_void_p, c_uint64)
"""retro_vfs_read_t"""

vfs_write_t = CFUNCTYPE(c_int64, POINTER(VfsFileHandle), c_void_p, c_uint64)
"""retro_vfs_write_t"""

vfs_flush_t = CFUNCTYPE(c_int, POINTER(VfsFileHandle))
"""retro_vfs_flush_t"""

vfs_remove_t = CFUNCTYPE(c_int, c_void_p)
"""retro_vfs_remove_t"""

vfs_rename_t = CFUNCTYPE(c_int, c_char_p, c_char_p)
"""retro_vfs_rename_t"""

vfs_stat_t = CFUNCTYPE(c_int, c_char_p, POINTER(c_int32))
"""retro_vfs_stat_t"""

vfs_mkdir_t = CFUNCTYPE(c_int, c_char_p)
"""retro_vfs_mkdir_t"""

vfs_opendir_t = CFUNCTYPE(POINTER(VfsDirHandle), c_char_p, c_bool)
"""retro_vfs_opendir_t"""

vfs_readdir_t = CFUNCTYPE(c_bool, POINTER(VfsDirHandle))
"""retro_vfs_readdir_t"""

vfs_dirent_get_name_t = CFUNCTYPE(c_char_p, POINTER(VfsDirHandle))
"""retro_vfs_dirent_get_name_t"""

vfs_dirent_is_dir_t = CFUNCTYPE(c_bool, POINTER(VfsDirHandle))
"""retro_vfs_dirent_is_dir_t"""

vfs_closedir_t = CFUNCTYPE(c_int, POINTER(VfsDirHandle))
"""retro_vfs_closedir_t"""


class VfsInterface(Structure):
    """retro_vfs_interface"""

    _fields_ = [
        ("get_path", vfs_get_path_t),
        ("open", vfs_open_t),
        ("close", vfs_close_t),
        ("size", vfs_size_t),
        ("tell", vfs_tell_t),
        ("seek", vfs_seek_t),
        ("read", vfs_read_t),
        ("write", vfs_write_t),
        ("flush", vfs_flush_t),
        ("remove", vfs_remove_t),
        ("rename", vfs_rename_t),
        ("truncate", vfs_truncate_t),
        ("stat", vfs_stat_t),
        ("mkdir", vfs_mkdir_t),
        ("opendir", vfs_opendir_t),
        ("readdir", vfs_readdir_t),
        ("dirent_get_name", vfs_dirent_get_name_t),
        ("dirent_is_dir", vfs_dirent_is_dir_t),
        ("closedir", vfs_closedir_t),
    ]

    get_path: Callable
    open: Callable
    close: Callable
    size: Callable
    tell: Callable
    seek: Callable
    read: Callable
    write: Callable
    flush: Callable
    remove: Callable
    rename: Callable
    # API v2
    truncate: Callable
    # API v3
    stat: Callable
    mkdir: Callable
    opendir: Callable
    readdir: Callable
    dirent_get_name: Callable
    dirent_is_dir: Callable
    closedir: Callable
