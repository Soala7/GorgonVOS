from __future__ import annotations

import pygame
from desktop.ui.window.window import Window
from bridge.shell_bridge import ShellBridge
from resources.cursor_manager import cursor_manager

class TerminalWindow(Window):

    def __init__(self, service_manager):

        super().__init__(
            title="Terminal",
            width=900,
            height=600,
        )
        self.content_cursor = cursor_manager.TEXT
        self.minimized = False
        self.closed = False

        self.transform.position.x = 250
        self.transform.position.y = 120

        self.is_active = False

        self.font = pygame.font.SysFont("Consolas", 18)
        self.line_height = 24
        self.padding = 15
        self.prompt_prefix = "s7k11@vos:~$ "

        self.lines = [
            "Welcome to Gorgon OS Terminal",
            "Type 'help' to get started.",
            "",
        ]
        self.current_input = ""
        self.shell = ShellBridge(
            service_manager
        )

        self.cursor_visible = True
        self.cursor_timer = 0.0

    def activate(self):
        super().activate()
        self.is_active = True

    def deactivate(self):
        super().deactivate()
        self.is_active = False

    def update(self, dt):

        if self.is_active:
            self.cursor_timer += dt
            if self.cursor_timer >= 0.5:
                self.cursor_timer = 0.0
                self.cursor_visible = not self.cursor_visible
        else:
            self.cursor_visible = False

    def handle_event(self, event):

        super().handle_event(event)

        if not self.is_active or self.minimized:
            return

        if hasattr(event, "key"):
            if event.key == pygame.K_BACKSPACE:
                self.current_input = self.current_input[:-1]
            elif event.key == pygame.K_RETURN:
                self.execute_command()

        if hasattr(event, "unicode"):
            if event.unicode and event.unicode.isprintable():
                self.current_input += event.unicode

    def execute_command(self):

        command = self.current_input.strip()

        if command:

            self.lines.append(
                f"{self.prompt_prefix}{command}"
            )

            output = self.shell.execute(command)

            if output == "__VOS_CLEAR__":

                self.lines.clear()

            elif output == "__VOS_EXIT__":

                self.close()

            elif output:

                for line in output.splitlines():

                    if line.strip():

                        self.lines.append(line)

        self.current_input = ""

        self.cursor_timer = 0.0

        self.cursor_visible = True

    def draw(self, renderer):
        if self.minimized:
            return

        super().draw(renderer)
        surface = renderer.surface

        if hasattr(self, "transform"):
            wx, wy = self.transform.position.x, self.transform.position.y
            ww, wh = self.transform.size.width, self.transform.size.height
        else:
            wx, wy, ww, wh = self.rect.x, self.rect.y, self.rect.width, self.rect.height

        title_bar_height = 38
        border_thickness = 2

        client_rect = pygame.Rect(
            wx + border_thickness,
            wy + title_bar_height,
            ww - (border_thickness * 2),
            wh - title_bar_height - border_thickness,
        )

        is_maximized = getattr(self, "maximized", getattr(self, "is_maximized", False))
        corner_radius = 0 if is_maximized else 10

        canvas_surface = pygame.Surface((client_rect.width, client_rect.height), pygame.SRCALPHA)

        pygame.draw.rect(
            canvas_surface,
            (20, 20, 22, 10),
            canvas_surface.get_rect(),
            border_bottom_left_radius=corner_radius,
            border_bottom_right_radius=corner_radius,
        )

        surface.blit(canvas_surface, (client_rect.x, client_rect.y))

        max_visible_lines = (client_rect.height - (self.padding * 2)) // self.line_height

        max_history_lines = max_visible_lines - 1

        visible_history = self.lines[-max_history_lines:] if len(self.lines) > max_history_lines else self.lines

        text_y = client_rect.y + self.padding
        for line in visible_history:
            text_surface = self.font.render(line, True, (220, 220, 220))
            surface.blit(text_surface, (client_rect.x + self.padding, text_y))
            text_y += self.line_height

        full_prompt = f"{self.prompt_prefix}{self.current_input}"
        if self.cursor_visible:
            full_prompt += "_"

        input_surface = self.font.render(full_prompt, True, (120, 255, 120))
        surface.blit(input_surface, (client_rect.x + self.padding, text_y))
