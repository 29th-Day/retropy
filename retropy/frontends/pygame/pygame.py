from ctypes import POINTER, c_void_p, c_uint32, c_size_t, c_int16, c_uint16

from ..libretro import LibRetro
from ..config import PyGameOption
from ..common import buffer_to_frame, frame_to_rgb
from ..enums import RETRO_INPUT, RETRO_INPUT_JOYPAD

import pygame


class Retro_pyGame(LibRetro):
    options: PyGameOption
    running: bool = True

    keybindings = {
        pygame.K_w: (0, RETRO_INPUT_JOYPAD.UP),
        pygame.K_a: (0, RETRO_INPUT_JOYPAD.LEFT),
        pygame.K_s: (0, RETRO_INPUT_JOYPAD.DOWN),
        pygame.K_d: (0, RETRO_INPUT_JOYPAD.RIGHT),
        pygame.K_i: (0, RETRO_INPUT_JOYPAD.A),
        pygame.K_l: (0, RETRO_INPUT_JOYPAD.B),
        pygame.K_j: (0, RETRO_INPUT_JOYPAD.SELECT),
        pygame.K_k: (0, RETRO_INPUT_JOYPAD.START),
    }

    def __init__(self, dll_path: str, options: PyGameOption = None):
        super().__init__(dll_path, options)
        pygame.init()
        self.clock = pygame.time.Clock()

    def run(self):
        super().run()
        self.clock.tick(self.options.fps)

    def cb_video_refresh(
        self, data: c_void_p, width: c_uint32, height: c_uint32, pitch: c_size_t
    ):
        if not hasattr(self, "display"):
            self.display = pygame.display.set_mode(
                (int(width * self.options.scaling), int(height * self.options.scaling))
            )

        frame = buffer_to_frame(data, width, height, pitch, self.color_format)
        frame = frame_to_rgb(frame, self.color_format)

        surf = pygame.surfarray.make_surface(frame)
        surf = pygame.transform.rotate(surf, -90)
        if self.options.scaling != 1.0:
            surf = pygame.transform.scale_by(surf, self.options.scaling)
        self.display.blit(surf, (0, 0))
        pygame.display.flip()

    def cb_audio_sample(self, left: int, right: int):
        pass

    def cb_audio_sample_batch(
        self, data: POINTER(c_int16), frames: c_size_t
    ) -> c_size_t:
        return 0

    def cb_input_poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key in self.keybindings:
                port, button = self.keybindings[event.key]
                self.player_inputs[port].actions[button] = 1
            elif event.type == pygame.KEYUP and event.key in self.keybindings:
                port, button = self.keybindings[event.key]
                self.player_inputs[port].actions[button] = 0
                # self.inputs.pop(button, None) # None = safety check (most possibly useless)
