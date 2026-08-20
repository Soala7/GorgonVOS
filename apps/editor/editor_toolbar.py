
import pygame
from bridge.vos_api import vos_api

class EditorToolbar:

    TARGET_DIRECTORIES = ["Documents", "Pictures", "Videos", "Downloads"]

    def __init__(self, x: int, y: int, width: int, height: int = 32):
        self.rect = pygame.Rect(x, y, width, height)
        self.selected_dir = "Documents"
        self.font = pygame.font.SysFont("Segoe UI", 13)

    def set_directory(self, dir_name: str) -> None:
        if dir_name in self.TARGET_DIRECTORIES:
            self.selected_dir = dir_name

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (225, 228, 232), self.rect)
        pygame.draw.line(
            surface,
            (190, 195, 205),
            (self.rect.x, self.rect.bottom),
            (self.rect.right, self.rect.bottom),
        )

        label = self.font.render(
            f"Target Dir: /{self.selected_dir}", True, (50, 50, 50)
        )
        surface.blit(label, (self.rect.x + 10, self.rect.y + 7))
