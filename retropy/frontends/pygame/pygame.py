from ctypes import POINTER, c_void_p, c_uint32, c_size_t, c_int16, c_uint16

from ...core.retro import RetroPy
from ...core.device import Device, Joypad

from ...utils.input import PlayerInput

import pygame


class RetroPyGame(RetroPy):
    # options: PyGameOption
    running: bool = True

    keybindings = {
        pygame.K_w: (0, Joypad.UP),
        pygame.K_a: (0, Joypad.LEFT),
        pygame.K_s: (0, Joypad.DOWN),
        pygame.K_d: (0, Joypad.RIGHT),
        pygame.K_i: (0, Joypad.A),
        pygame.K_l: (0, Joypad.B),
        pygame.K_j: (0, Joypad.SELECT),
        pygame.K_k: (0, Joypad.START),
    }

    def __init__(
        self, dll_path: str, scaling: float = 1.0, fps: int = 30
    ):  # , options: PyGameOption = None
        super().__init__(dll_path, numpy=True)

        self.scaling = scaling
        self.fps = fps

        self.players = [PlayerInput()]

        pygame.init()
        self.clock = pygame.time.Clock()

    def run(self):
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

            self.clock.tick(self.fps)

    def input_poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key in self.keybindings:
                port, button = self.keybindings[event.key]
                self.players[port].actions[Device.JOYPAD][button] = 1
            elif event.type == pygame.KEYUP and event.key in self.keybindings:
                port, button = self.keybindings[event.key]
                self.players[port].actions[Device.JOYPAD][button] = 0
                # self.inputs.pop(button, None) # None = safety check (most possibly useless)

    def input_state(self, port: int, device: int, index: int, id: int) -> int:
        # return self.players[port].actions[Device(device)][id]

        print(self.players[port].actions[Device(device)])

        return 0
