"""
Gorgon OS (VOS)
Text Editor File Menu
"""

from __future__ import annotations

import pygame

from desktop.ui.core.event import MousePressEvent

class EditorMenu:
    def __init__(self, editor) -> None:
        self.editor = editor
        self.font = pygame.font.SysFont("Segoe UI", 14)
        self.menu_font = pygame.font.SysFont("Segoe UI", 14)
        self.open = False
        self.items = []
        self.menu_rect = pygame.Rect(0, 0, 0, 0)
        self._build_menu()

    def _build_menu(self) -> None:
        self.items = [
            {"label": "New", "action": getattr(self.editor, "new_document", self.editor.new_file)},
            {"label": "Open", "action": getattr(self.editor, "open_document_dialog", lambda: print("Open dialog coming next"))},
            {"label": "Save", "action": self.editor.save_file},
            {"label": "Save As", "action": getattr(self.editor, "save_as_document", lambda: self.editor.save_to_directory("document.txt"))},
        ]

    def handle_event(self, event) -> bool:
        if not isinstance(event, MousePressEvent):
            return False

        if getattr(event, "button", 1) != 1:
            return False

        pos = getattr(event, "pos", pygame.mouse.get_pos())

        if self.open:
            if self.menu_rect.collidepoint(pos):
                for item in self.items:
                    rect = item.get("rect")

                    if rect and rect.collidepoint(pos):
                        action = item.get("action")

                        if callable(action):
                            action()

                        self.open = False
                        return True

                return True

            self.open = False
            return False

        file_button = pygame.Rect(
            self.menu_rect.x,
            self.menu_rect.y - 32,
            55,
            32
        )

        if file_button.collidepoint(pos):
            self.open = True
            return True

        return False

    def draw(self, surface: pygame.Surface) -> None:
        x = self.editor.transform.position.x + 8
        y = self.editor.transform.position.y + self.editor.TITLEBAR_HEIGHT + 2

        file_button = pygame.Rect(x, y, 55, 30)
        mouse_pos = pygame.mouse.get_pos()
        hovered = file_button.collidepoint(mouse_pos)

        pygame.draw.rect(
            surface,
            (220, 226, 234) if hovered or self.open else (242, 244, 247),
            file_button,
            border_radius=4
        )

        pygame.draw.rect(
            surface,
            (190, 195, 203),
            file_button,
            1,
            border_radius=4
        )

        text = self.font.render("File", True, (40, 43, 50))
        surface.blit(text, text.get_rect(center=file_button.center))

        if not self.open:
            self.menu_rect = pygame.Rect(
                x,
                y + file_button.height,
                180,
                0
            )
            return

        item_height = 32
        menu_height = len(self.items) * item_height

        self.menu_rect = pygame.Rect(
            x,
            y + file_button.height,
            180,
            menu_height
        )

        pygame.draw.rect(
            surface,
            (250, 250, 252),
            self.menu_rect
        )

        pygame.draw.rect(
            surface,
            (175, 180, 190),
            self.menu_rect,
            1
        )

        for index, item in enumerate(self.items):
            rect = pygame.Rect(
                self.menu_rect.x,
                self.menu_rect.y + index * item_height,
                self.menu_rect.width,
                item_height
            )

            item["rect"] = rect

            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(
                    surface,
                    (225, 232, 240),
                    rect
                )

            text = self.menu_font.render(
                item["label"],
                True,
                (35, 38, 45)
            )

            surface.blit(
                text,
                (rect.x + 12, rect.y + 7)
            )
