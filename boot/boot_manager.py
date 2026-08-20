"""
Gorgon OS (VOS)

Boot Manager
"""

from __future__ import annotations

import pygame

from boot.boot_screen import BootScreen
from boot.login_screen import LoginScreen
from desktop.shell.shell import Shell
from resources.cursor_manager import cursor_manager
from desktop.ui.core.event import (
    KeyPressEvent,
    KeyReleaseEvent,
    KeyModifier,
    MouseMoveEvent,
    MousePressEvent,
    MouseReleaseEvent,
    MouseWheelEvent,
    MouseButton,
)

class BootManager:

    BOOT = "boot"
    LOGIN = "login"
    DESKTOP = "desktop"

    def __init__(self, kernel) -> None:

        self.kernel = kernel

        self.boot_screen = BootScreen()

        self.login_screen = LoginScreen()

        self.shell = Shell(kernel.service_manager)

        self.cursor = cursor_manager

        self.state = self.BOOT

        self.boot_screen.finished = False
        self.login_screen.logged_in = False

        self.boot_screen.start()

        print("[BOOT] State:", self.state)

    def update(self, dt: float) -> None:

        if self.state == self.BOOT:

            self.boot_screen.update()

            if self.boot_screen.finished:

                self.state = self.LOGIN
                print("[BOOT] -> LOGIN")

        elif self.state == self.LOGIN:

            if self.login_screen.logged_in:

                self.state = self.DESKTOP
                print("[LOGIN] -> DESKTOP")

        elif self.state == self.DESKTOP:

            self.shell.update(dt)

    def restart_session(self, boot_again: bool = False) -> None:
        for window in list(self.shell.desktop.window_manager.windows):
            window.close()
        self.shell.desktop.window_manager.windows.clear()
        self.shell.desktop.window_manager.active_window = None
        pygame.mixer.music.stop()
        self.login_screen = LoginScreen()
        self.shell = Shell(self.kernel.service_manager)
        if boot_again:
            self.boot_screen = BootScreen()
            self.boot_screen.start()
            self.state = self.BOOT
        else:
            self.state = self.LOGIN

    def draw(self,renderer,) -> None:

        if self.state == self.BOOT:

            self.boot_screen.draw(renderer)

        elif self.state == self.LOGIN:

            self.login_screen.draw(renderer)

        elif self.state == self.DESKTOP:

            self.shell.draw(renderer)

        self.cursor.draw(renderer)

    def handle_event(self,event,) -> None:

        if self.state == self.LOGIN:

            import pygame

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_RETURN
            ):

                self.login_screen.select_user("Guest")

                self.login_screen.login()

        elif self.state == self.DESKTOP:

            ui_event = self._convert_pygame_event(event)

            if ui_event is not None:
                self.shell.handle_event(ui_event)

    def _convert_pygame_event(self, event):

        if event.type == pygame.MOUSEMOTION:
            return MouseMoveEvent(event.pos[0], event.pos[1])

        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self._map_button(event.button)
            return MousePressEvent(event.pos[0], event.pos[1], button)

        if event.type == pygame.MOUSEBUTTONUP:
            button = self._map_button(event.button)
            return MouseReleaseEvent(event.pos[0], event.pos[1], button)

        if event.type == pygame.MOUSEWHEEL:
            return MouseWheelEvent(event.pos[0], event.pos[1], event.y)

        if event.type == pygame.KEYDOWN:
            print("KEYDOWN:", event.key)
            modifier = self._map_modifiers(pygame.key.get_mods())
            return KeyPressEvent(
                event.key,
                event.unicode,
                modifier,
            )

        if event.type == pygame.KEYUP:
            modifier = self._map_modifiers(pygame.key.get_mods())
            return KeyReleaseEvent(event.key, modifier)

        return None

    def _map_button(self, button):

        match button:
            case 1: return MouseButton.LEFT
            case 2: return MouseButton.MIDDLE
            case 3: return MouseButton.RIGHT
            case 4: return MouseButton.X1
            case 5: return MouseButton.X2

        return MouseButton.NONE

    def _map_modifiers(self, mods):
        if mods & pygame.KMOD_CTRL:
            return KeyModifier.CTRL
        if mods & pygame.KMOD_SHIFT:
            return KeyModifier.SHIFT
        if mods & pygame.KMOD_ALT:
            return KeyModifier.ALT
        if mods & pygame.KMOD_GUI:
            return KeyModifier.SUPER

        return KeyModifier.NONE
