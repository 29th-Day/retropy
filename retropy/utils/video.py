# 

from ctypes import c_void_p, c_uint32, c_uint16, POINTER, cast
from typing import Tuple

try:
    import numpy as np
except ImportError:
    pass

from ..core.framebuffer import PIXEL_FORMAT

def buffer_to_frame(data: c_void_p, shape: Tuple[int, int, int], format: PIXEL_FORMAT, numpy: bool = True):
    """Convert void* into usable list/array.

    Args:
        data (c_void_p): Data revieved by core
        shape (Tuple[int, int, int]): Shape of buffer (width, height, pitch)
        format (PIXEL_FORMAT): color format
        numpy (bool, optional): If numpy should be used. Defaults to True.
    """
    if format == PIXEL_FORMAT.XRGB8888:
        ptr = cast(data, POINTER(c_uint32))
    else:
        ptr = cast(data, POINTER(c_uint16))
        
    if numpy:
        ...
    else:
        frame = []
        for h in shape[1]:
            frame.append([])
            for w in shape[0]:
                frame[h].append(ptr[h * w + w])
