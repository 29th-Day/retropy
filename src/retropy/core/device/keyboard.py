from ctypes import *
from enum import Enum
from typing import Callable

keyboard_event_t = CFUNCTYPE(None, c_bool, c_uint, c_uint32, c_uint16)
"""retro_keyboard_event_t"""


class KeyboardCallback(Structure):
    """retro_keyboard_callback"""

    _fields_ = [
        ("callback", keyboard_event_t),
    ]

    callback: Callable[[bool, int, int, int], None]


class Key(Enum):
    """retro_key"""

    UNKNOWN = 0
    FIRST = 0
    BACKSPACE = 8
    TAB = 9
    CLEAR = 12
    RETURN = 13
    PAUSE = 19
    ESCAPE = 27
    SPACE = 32
    EXCLAIM = 33
    QUOTEDBL = 34
    HASH = 35
    DOLLAR = 36
    AMPERSAND = 38
    QUOTE = 39
    LEFTPAREN = 40
    RIGHTPAREN = 41
    ASTERISK = 42
    PLUS = 43
    COMMA = 44
    MINUS = 45
    PERIOD = 46
    SLASH = 47
    K0 = 48
    K1 = 49
    K2 = 50
    K3 = 51
    K4 = 52
    K5 = 53
    K6 = 54
    K7 = 55
    K8 = 56
    K9 = 57
    COLON = 58
    SEMICOLON = 59
    LESS = 60
    EQUALS = 61
    GREATER = 62
    QUESTION = 63
    AT = 64
    LEFTBRACKET = 91
    BACKSLASH = 92
    RIGHTBRACKET = 93
    CARET = 94
    UNDERSCORE = 95
    BACKQUOTE = 96
    a = 97
    b = 98
    c = 99
    d = 100
    e = 101
    f = 102
    g = 103
    h = 104
    i = 105
    j = 106
    k = 107
    l = 108
    m = 109
    n = 110
    o = 111
    p = 112
    q = 113
    r = 114
    s = 115
    t = 116
    u = 117
    v = 118
    w = 119
    x = 120
    y = 121
    z = 122
    LEFTBRACE = 123
    BAR = 124
    RIGHTBRACE = 125
    TILDE = 126
    DELETE = 127

    KP0 = 256
    KP1 = 257
    KP2 = 258
    KP3 = 259
    KP4 = 260
    KP5 = 261
    KP6 = 262
    KP7 = 263
    KP8 = 264
    KP9 = 265
    KP_PERIOD = 266
    KP_DIVIDE = 267
    KP_MULTIPLY = 268
    KP_MINUS = 269
    KP_PLUS = 270
    KP_ENTER = 271
    KP_EQUALS = 272

    UP = 273
    DOWN = 274
    RIGHT = 275
    LEFT = 276
    INSERT = 277
    HOME = 278
    END = 279
    PAGEUP = 280
    PAGEDOWN = 281

    F1 = 282
    F2 = 283
    F3 = 284
    F4 = 285
    F5 = 286
    F6 = 287
    F7 = 288
    F8 = 289
    F9 = 290
    F10 = 291
    F11 = 292
    F12 = 293
    F13 = 294
    F14 = 295
    F15 = 296

    NUMLOCK = 300
    CAPSLOCK = 301
    SCROLLOCK = 302
    RSHIFT = 303
    LSHIFT = 304
    RCTRL = 305
    LCTRL = 306
    RALT = 307
    LALT = 308
    RMETA = 309
    LMETA = 310
    LSUPER = 311
    RSUPER = 312
    MODE = 313
    COMPOSE = 314

    HELP = 315
    PRINT = 316
    SYSREQ = 317
    BREAK = 318
    MENU = 319
    POWER = 320
    EURO = 321
    UNDO = 322
    OEM_102 = 323


class Mod(Enum):
    """retro_mod"""

    NONE = 0x00
    SHIFT = 0x01
    CTRL = 0x02
    ALT = 0x04
    META = 0x08
    NUMLOCK = 0x10
    CAPSLOCK = 0x20
    SCROLLOCK = 0x40
