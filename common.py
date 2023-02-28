from ctypes import cast, POINTER, c_void_p, c_uint32, c_uint16

import numpy as np

from .enums import RETRO_COLOR_FORMAT
from .exceptions import UnknownColorFormat

def buffer_to_frame(data: c_void_p, width: int, height: int, pitch: int, format: RETRO_COLOR_FORMAT):
    """Convert the raw void* data into a useable numpy array.

    Args:
        data (c_void_p): Data given to the video callback.
        shape (tuple): Shape to cast buffer into.
        format (RETRO_COLOR_FORMAT): Different formats use different number of bytes per pixel.

    Returns:
        frame (np.ndarray): Frame into 2D shape.
    """

    if format == RETRO_COLOR_FORMAT.FORMAT_XRGB8888:
        _type = c_uint32
        cast_shape = (height, pitch // 4)
    else:
        _type = c_uint16
        cast_shape = (height, pitch // 2)


    int_ptr = cast(data, POINTER(_type))
    frame = np.ctypeslib.as_array(int_ptr, shape=cast_shape)[0:height, 0:width]
    return np.flip(frame, axis=1)

def frame_to_rgb(frame: np.ndarray, format: RETRO_COLOR_FORMAT):
    """Converts the frames from `cb_video_refresh` to standard `H x W x 3`-format

    Note: Color conversion may not be completely accurate.

    Args:
        frame (np.ndarray): Frame in 2D form.
        format (RETRO_COLOR_FORMAT): Color format used.

    Raises:
        UnknownColorFormat: Raised if RETRO_COLOR_FORMAT.FORMAT_UNKNOWN is given.

    Returns:
        image (np.ndarray): Frame with split color channels.
    """

    # 0x1F = 0b011111
    # 0x3F = 0b111111
    # 0xFF = 0b11111111 

    if format == RETRO_COLOR_FORMAT.FORMAT_0RGB1555:
        # extract and convert channels
        red = ((frame >> 10) & 0x1F) << 3
        green = ((frame >> 5) & 0x1F) << 3
        blue = (frame & 0x1F) << 3
    elif format == RETRO_COLOR_FORMAT.FORMAT_XRGB8888:
        # extract channels
        red = (frame >> 16) & 0xFF
        green = (frame >> 8) & 0xFF
        blue = frame & 0xFF
    elif format == RETRO_COLOR_FORMAT.FORMAT_RGB565:
        # extract and convert channels
        red = ((frame >> 11) & 0x1F) << 3     # = (red / 32)   * 256 = red   * 8 = red << 3
        green = ((frame >> 5) & 0x3F) << 2    # = (green / 64) * 256 = green * 4 = green << 2
        blue = (frame & 0x1F) << 3
    else:
        raise UnknownColorFormat("Unknown color format specified.")

    # Combine the red, green, and blue arrays into a single RGB888 array
    return np.dstack((red, green, blue)).astype(np.uint8)

def enable_bit(mask: int, bit: int) -> int:
    return mask | 1 << bit

def disable_bit(mask: int, bit: int) -> int:
    return mask & ~(1 << bit)
