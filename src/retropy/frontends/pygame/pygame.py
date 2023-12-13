from ctypes import POINTER, c_int16
from ...core.retro import RetroPy
from ...core.device import Device, Joypad, Analog

import pygame

import numpy as np


class RetroPyGame(RetroPy):
    # options: PyGameOption
    running: bool = True

    keybindings: dict[int, tuple[int, int]] = {
        pygame.K_w: (Device.JOYPAD, 0, Joypad.UP),
        pygame.K_a: (Device.JOYPAD, 0, Joypad.LEFT),
        pygame.K_s: (Device.JOYPAD, 0, Joypad.DOWN),
        pygame.K_d: (Device.JOYPAD, 0, Joypad.RIGHT),
        pygame.K_l: (Device.JOYPAD, 0, Joypad.A),
        pygame.K_k: (Device.JOYPAD, 0, Joypad.B),
        pygame.K_i: (Device.JOYPAD, 0, Joypad.X),
        pygame.K_j: (Device.JOYPAD, 0, Joypad.Y),
        pygame.K_v: (Device.JOYPAD, 0, Joypad.SELECT),
        pygame.K_b: (Device.JOYPAD, 0, Joypad.START),
    }

    FPS: int = 30

    def __init__(
        self, dll_path: str, scaling: float = 1.0
    ):  # , options: PyGameOption = None
        super().__init__(dll_path, numpy=True)

        self.scaling = scaling

    def __del__(self):
        pygame.quit()
        return super().__del__()

    def run(self):
        av_info = self.system_av_info()

        self.FPS = int(max(self.FPS, av_info.timing.fps))
        # self.FREQUENCY = int(av_info.timing.sample_rate)

        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()

        while self.running:
            frame = self.frame_advance()

            if not hasattr(self, "display"):
                self.display = pygame.display.set_mode(
                    (
                        int(frame.shape[1] * self.scaling),
                        int(frame.shape[0] * self.scaling),
                    )
                )

            surf = pygame.surfarray.make_surface(frame)
            surf = pygame.transform.rotate(surf, -90)
            surf = pygame.transform.flip(surf, True, False)
            if self.scaling != 1.0:
                surf = pygame.transform.scale_by(surf, self.scaling)
            self.display.blit(surf, (0, 0))
            pygame.display.flip()

            self.clock.tick(self.FPS)

    def input_poll(self):
        port = 0  # only support one player

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.running = False
                continue

            elif event.type == pygame.KEYDOWN and event.key in self.keybindings:
                device, index, button = self.keybindings[event.key]
                self.controllers[port].set_state(device, index, button, 1)
            elif event.type == pygame.KEYUP and event.key in self.keybindings:
                device, index, button = self.keybindings[event.key]
                self.controllers[port].set_state(device, index, button, 0)

    def audio_sample(self, left: int, right: int) -> None:
        return super().audio_sample(left, right)

    def audio_sample_batch(self, data: POINTER(c_int16), frames: int) -> int:
        # manual = []

        # for i in range(frames):
        #     # print(f"left: {data[i]}, right: {data[i+1]}")
        #     manual.append((data[i], data[i + 1]))

        # manual = np.array(manual, dtype=np.int16)

        freq = 44100
        Hz = 440

        channel = np.sin(2 * np.pi * np.arange(freq) * Hz / freq).astype(np.float16)

        print(channel)

        manual = np.repeat(channel.reshape(-1, 1), 2, 1)

        print(manual.shape)

        sound = pygame.sndarray.make_sound(manual)

        print(sound.get_length())

        sound.play()

        wait = int(sound.get_length() * 1000)

        print(wait)

        # pygame.time.wait(int(sound.get_length() * 1000))

        return 0
