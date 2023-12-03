#

from ctypes import c_void_p, c_uint32, c_uint16, POINTER, cast
from typing import Tuple, List
from enum import Enum

import matplotlib.pyplot as plt

try:
    import numpy as np
    from numpy.typing import NDArray
except ImportError:
    pass

from ..core.framebuffer import PIXEL_FORMAT

i = 0


def buffer_to_frame(
    data: c_void_p,
    shape: Tuple[int, int, int],
    format: PIXEL_FORMAT,
    numpy: bool = True,
):
    """Convert void* array into usable python list / np array.

    Args:
        data (c_void_p): Data revieved by core
        shape (Tuple[int, int, int]): Shape of buffer (width, height, pitch)
        format (PIXEL_FORMAT): color format for raw buffer
        numpy (bool, optional): If numpy should be used. Defaults to True.
    """
    if format == PIXEL_FORMAT.XRGB8888:
        ptr = cast(data, POINTER(c_uint32))
    else:
        ptr = cast(data, POINTER(c_uint16))

    if numpy:
        frame: NDArray[np.uint8] = np.ctypeslib.as_array(int, shape=())
    else:
        frame: List[List[Tuple[int, int, int] | int]] = []
        for h in range(shape[1]):
            frame.append([])
            for w in range(shape[0]):
                pixel: int = ptr[h * w + w]
                frame[h].append(pixel_to_rgb(pixel, format))

    global i

    if i % 500 == 0:
        plt.imshow(frame)
        plt.title(f"{i}")
        plt.show()

    i += 1


def pixel_to_rgb(pixel: int, format: PIXEL_FORMAT):
    """_summary_

    Args:
        pixel (int): _description_
        format (PIXEL_FORMAT): _description_
    """

    # 0x1F = 0b00011111
    # 0x3F = 0b00111111
    # 0xFF = 0b11111111

    if format == PIXEL_FORMAT.RGB1555:
        red = ((pixel >> 10) & 0x1F) << 3
        green = ((pixel >> 5) & 0x1F) << 3
        blue = (pixel & 0x1F) << 3
    elif format == PIXEL_FORMAT.XRGB8888:
        red = (pixel >> 16) & 0xFF
        green = (pixel >> 8) & 0xFF
        blue = pixel & 0xFF
    elif format == PIXEL_FORMAT.RGB565:
        red = ((pixel >> 11) & 0x1F) << 3
        green = ((pixel >> 5) & 0x3F) << 2
        blue = (pixel & 0x1F) << 3
    else:
        raise NotImplementedError()

    return (red, green, blue)
