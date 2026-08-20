from __future__ import annotations

import pygame

class CursorManager:

    DEFAULT = "default"
    POINTER = "pointer"
    TEXT = "text"
    BUSY = "busy"
    MOVE = "move"
    RESIZE_H = "resize_h"
    RESIZE_V = "resize_v"
    RESIZE_L = "resize_l"
    RESIZE_R = "resize_r"

    CURSOR_SIZE = 28

    def __init__(self):

        self.cursors = {
            self.DEFAULT: self._load("assets/cursor/cursor_default.png"),
            self.POINTER: self._load("assets/cursor/cursor_pointer.png"),
            self.TEXT: self._load("assets/cursor/cursor_text.png"),
            self.BUSY: self._load("assets/cursor/cursor_busy.png"),
            self.MOVE: self._load("assets/cursor/cursor_move.png"),
            self.RESIZE_H: self._load("assets/cursor/cursor_resize_h.png"),
            self.RESIZE_V: self._load("assets/cursor/cursor_resize_v.png"),
            self.RESIZE_L: self._load("assets/cursor/cursor_resize_l.png"),
            self.RESIZE_R: self._load("assets/cursor/cursor_resize_r.png"),
        }

        self.current = self.DEFAULT

    def _load(self, path):

        image = pygame.image.load(path)

        image = pygame.transform.smoothscale(
            image,
            (
                self.CURSOR_SIZE,
                self.CURSOR_SIZE,
            ),
        )

        return image

    def set(self, cursor):

        if cursor in self.cursors:
            self.current = cursor
        else:
            self.current = self.DEFAULT

    def draw(self, renderer):

        mx, my = pygame.mouse.get_pos()

        image = self.cursors[self.current]

        renderer.surface.blit(
            image,
            (
                mx - 2,
                my - 2,
            ),
        )

cursor_manager = CursorManager()
