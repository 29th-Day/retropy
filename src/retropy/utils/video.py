# video utilities

from ctypes import c_void_p, c_uint32, c_uint16, POINTER, cast
from typing import Tuple, List

try:
    import numpy as np
except ImportError:
    # np = None
    pass

from ..core.renderer.framebuffer import PixelFormat

Frame = np.ndarray | List[List[Tuple[int, int, int]]]
"""Type alias for video frame"""


def buffer_to_frame(
    data: c_void_p,
    shape: Tuple[int, int, int],
    format: PixelFormat,
    numpy: bool = True,
) -> Frame:
    """Convert void* array into usable python list / np array.

    Uses `Height x Width x Channels` convention.

    Args:
        data (c_void_p): Data received by core
        shape (Tuple[int, int, int]): Shape of buffer (height, width, pitch)
        format (PixelFormat): color format for raw buffer
        numpy (bool, optional): If numpy should be used. Defaults to True.

    Returns:
        Frame: Converted video frame
    """
    if format == PixelFormat.XRGB8888:
        ptr = cast(data, POINTER(c_uint32))
        width_p = shape[2] // 4
    else:
        ptr = cast(data, POINTER(c_uint16))
        width_p = shape[2] // 2

    if numpy:
        frame = np.ctypeslib.as_array(ptr, shape=(shape[0], width_p))[
            0 : shape[0], 0 : shape[1]
        ]
        frame = np.dstack(pixel_to_rgb(frame, format)).astype(np.uint8)
    else:
        frame = []
        for h in range(shape[0]):
            frame.append([])
            for w in range(shape[1]):
                pixel: int = ptr[h * width_p + w]
                frame[h].append(pixel_to_rgb(pixel, format))

    return frame


def pixel_to_rgb(
    pixel: int | np.ndarray, format: PixelFormat
) -> np.ndarray | Tuple[int, int, int]:
    """Splits single pixel value into RGB channels

    Args:
        pixel (int | np.ndarray): single pixel value or whole np frame
        format (PixelFormat): color format for raw buffer

    Returns:
        np.ndarray | Tuple[int, int, int]: RGB values of single pixel or whole frame if numpy
    """

    # 0x1F = 0b00011111
    # 0x3F = 0b00111111
    # 0xFF = 0b11111111

    if format == PixelFormat.RGB1555:
        red = ((pixel >> 10) & 0x1F) << 3
        green = ((pixel >> 5) & 0x1F) << 3
        blue = (pixel & 0x1F) << 3
    elif format == PixelFormat.RGB565:
        red = ((pixel >> 11) & 0x1F) << 3
        green = ((pixel >> 5) & 0x3F) << 2
        blue = (pixel & 0x1F) << 3
    else:  # format == PixelFormat.XRGB8888:
        red = (pixel >> 16) & 0xFF
        green = (pixel >> 8) & 0xFF
        blue = pixel & 0xFF

    return (red, green, blue)
