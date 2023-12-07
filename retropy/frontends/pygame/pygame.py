from ...core.retro import RetroPy
from ...core.device import Joypad

import pygame


class RetroPyGame(RetroPy):
    # options: PyGameOption
    running: bool = True

    keybindings: dict[int, tuple[int, int]] = {
        pygame.K_w: (0, 0, Joypad.UP),
        pygame.K_a: (0, 0, Joypad.LEFT),
        pygame.K_s: (0, 0, Joypad.DOWN),
        pygame.K_d: (0, 0, Joypad.RIGHT),
        pygame.K_l: (0, 0, Joypad.A),
        pygame.K_k: (0, 0, Joypad.B),
        pygame.K_i: (0, 0, Joypad.X),
        pygame.K_j: (0, 0, Joypad.Y),
        pygame.K_v: (0, 0, Joypad.SELECT),
        pygame.K_b: (0, 0, Joypad.START),
    }

    def __init__(
        self, dll_path: str, scaling: float = 1.0, fps: int = 30
    ):  # , options: PyGameOption = None
        super().__init__(dll_path, numpy=True)

        self.scaling = scaling
        self.fps = fps

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
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.running = False
                continue

            elif event.type == pygame.KEYDOWN and event.key in self.keybindings:
                port, index, button = self.keybindings[event.key]
                self.controllers[port].set_state(index, button, 1)
            elif event.type == pygame.KEYUP and event.key in self.keybindings:
                port, index, button = self.keybindings[event.key]
                self.controllers[port].set_state(index, button, 0)
