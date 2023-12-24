from ctypes import POINTER, c_int16
from ...core.retro import RetroPy
from ...utils.input import GamePadInput

import pyglet
import pyglet.window.key as key
from pyglet.media.codecs.base import Source, AudioFormat, AudioData

import numpy as np


class RetroPyGlet(RetroPy):
    keybindings = {
        key.W: GamePadInput.UP,
        key.A: GamePadInput.LEFT,
        key.S: GamePadInput.DOWN,
        key.D: GamePadInput.RIGHT,
        key.L: GamePadInput.A,
        key.K: GamePadInput.B,
        key.I: GamePadInput.X,
        key.J: GamePadInput.Y,
        key.V: GamePadInput.SELECT,
        key.B: GamePadInput.START,
    }

    def __init__(self, path: str, scaling: float = 1.0) -> None:
        super().__init__(path, True)
        self.scaling = scaling
        self.running = False

        # Nearest scaling
        pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
        pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

    def run(self):
        av_info = self.system_av_info()

        HEIGHT = av_info.geometry.base_height
        WIDTH = av_info.geometry.base_width
        FPS = int(av_info.timing.fps)
        SAMPLE_RATE = int(av_info.timing.sample_rate)

        window = pyglet.window.Window(
            height=HEIGHT * self.scaling,
            width=WIDTH * self.scaling,
            caption="Pyglet: Libretro",
        )

        self.audio = BufferSource(sample_rate=512 * FPS)
        self.audio.play()

        self.last_audio_frame = np.zeros((512, 2), dtype=np.int16)

        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        image = pyglet.image.ImageData(
            width=WIDTH, height=HEIGHT, fmt="RGB", data=frame.tobytes()
        )

        @window.event
        def on_key_press(symbol, _):
            action = self.keybindings.get(symbol, None)
            if action:
                self.controllers[0][action] = 1

        @window.event
        def on_key_release(symbol, _):
            action = self.keybindings.get(symbol, None)
            if action:
                self.controllers[0][action] = 0

        @window.event
        def on_draw():
            frame = self.frame_advance()

            image.set_data("RGB", -WIDTH * 3, frame.tobytes())

            window.clear()
            image.blit(0, 0, width=window.width, height=window.height)

            self.audio.set_audio_data(self.last_audio_frame)

        pyglet.app.run(1 / FPS)

    def audio_sample_batch(self, data: POINTER(c_int16), frames: int) -> int:
        data = np.ctypeslib.as_array(data, (frames * 2,)).reshape((frames, 2))
        self.last_audio_frame = data
        return 0


class BufferSource(pyglet.media.Source):
    def __init__(self, sample_rate: int) -> None:
        CHANNELS = 2
        BIT_SIZE = 16

        self.audio_format = AudioFormat(CHANNELS, BIT_SIZE, sample_rate)

        self._data = np.zeros((sample_rate, CHANNELS), dtype=np.int16)

    def set_audio_data(self, data: np.ndarray):
        size = len(data)

        buffer = np.roll(self._data, -size, axis=0)
        buffer[-size:] = data
        self._data = buffer

    def get_audio_data(self, num_bytes, compensation_time=0):
        data = self._data.tobytes()
        duration = float(len(data)) / self.audio_format.bytes_per_second
        return AudioData(data, len(data), 0, duration, [])
