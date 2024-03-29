from ..core.retro import RetroPy
from ..utils.input import GamePadInput
import pygame


class RetroPyGame(RetroPy):
    running: bool = True

    keybindings: dict[int, tuple[int, int]] = {
        pygame.K_w: GamePadInput.UP,
        pygame.K_a: GamePadInput.LEFT,
        pygame.K_s: GamePadInput.DOWN,
        pygame.K_d: GamePadInput.RIGHT,
        pygame.K_l: GamePadInput.A,
        pygame.K_k: GamePadInput.B,
        pygame.K_i: GamePadInput.X,
        pygame.K_j: GamePadInput.Y,
        pygame.K_v: GamePadInput.SELECT,
        pygame.K_b: GamePadInput.START,
    }

    FPS: int = 30

    def __init__(
        self, dll_path: str, scaling: float = 1.0
    ):  # , options: PyGameOption = None
        super().__init__(dll_path, numpy=True)

        self.scaling = scaling

    def run(self):
        av_info = self.system_av_info()

        self.FPS = int(max(self.FPS, av_info.timing.fps))
        pygame.init()
        self.display = pygame.display.set_mode(
            (
                int(av_info.geometry.base_width * self.scaling),
                int(av_info.geometry.base_height * self.scaling),
            )
        )

        self.clock = pygame.time.Clock()

        self.sound = None
        self.pos = 0

        while self.running:
            frame = self.frame_advance()

            surf = pygame.surfarray.make_surface(frame)
            surf = pygame.transform.rotate(surf, -90)
            surf = pygame.transform.flip(surf, True, False)
            if self.scaling != 1.0:
                surf = pygame.transform.scale_by(surf, self.scaling)
            self.display.blit(surf, (0, 0))
            pygame.display.flip()

            self.clock.tick(self.FPS)

        pygame.quit()

    def input_poll(self):
        port = 0  # only support one player

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.running = False
                continue

            elif event.type == pygame.KEYDOWN and event.key in self.keybindings:
                # device, index, button = self.keybindings[event.key]
                self.controllers[port][self.keybindings[event.key]] = 1
            elif event.type == pygame.KEYUP and event.key in self.keybindings:
                # device, index, button = self.keybindings[event.key]
                self.controllers[port][self.keybindings[event.key]] = 0
