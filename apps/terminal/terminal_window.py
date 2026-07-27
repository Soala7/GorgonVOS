from __future__ import annotations

import pygame
from desktop.ui.window.window import Window
from bridge.shell_bridge import ShellBridge

class TerminalWindow(Window):

    def __init__(self, service_manager):
        # 1. Initialize the base Window class first
        super().__init__(
            title="Terminal",
            width=900,
            height=600,
        )
        self.minimized = False  
        self.closed = False     

        # 2. Safely position the window. 
        self.transform.position.x = 250
        self.transform.position.y = 120

        # 3. Focus and state tracking
        self.is_active = False
        
        # Style Configuration
        self.font = pygame.font.SysFont("Consolas", 18)
        self.line_height = 24
        self.padding = 15
        self.prompt_prefix = "s7k11@vos:~$ "
        
        # Terminal Text Buffer
        self.lines = [
            "Welcome to Gorgon OS Terminal",
            "Type 'help' to get started.",
            "",
        ]
        self.current_input = ""
        self.shell = ShellBridge(
            service_manager
        )
        # Cursor blinking mechanics
        self.cursor_visible = True
        self.cursor_timer = 0.0

    # --------------------------------------------------
    # Window Manager Callbacks
    # --------------------------------------------------

    def activate(self):
        super().activate()
        self.is_active = True

    def deactivate(self):
        super().deactivate()
        self.is_active = False

    # --------------------------------------------------
    # Engine Loops
    # --------------------------------------------------

    def update(self, dt):
        # Only blink the cursor if the terminal is actually active
        if self.is_active:
            self.cursor_timer += dt
            if self.cursor_timer >= 0.5:
                self.cursor_timer = 0.0
                self.cursor_visible = not self.cursor_visible
        else:
            self.cursor_visible = False

    def handle_event(self, event):
        # 1. Allow the base Window class to handle window dragging/resizing first
        super().handle_event(event)
        
        # 2. Prevent typing into the terminal if the window isn't active/focused
        if not self.is_active or self.minimized:
            return

        # 3. Duck-type check: If it has a 'key' attribute, it's a keyboard event
        if hasattr(event, "key"):
            if event.key == pygame.K_BACKSPACE:
                self.current_input = self.current_input[:-1]
            elif event.key == pygame.K_RETURN:
                self.execute_command()
                
        # 4. Duck-type check: If it has 'unicode', check if we can print it
        if hasattr(event, "unicode"):
            if event.unicode and event.unicode.isprintable():
                self.current_input += event.unicode

    def execute_command(self):

        command = self.current_input.strip()

        if command:

            # Add command to terminal history
            self.lines.append(
                f"{self.prompt_prefix}{command}"
            )

            # Send command to C shell
            output = self.shell.execute(command)


            # Handle terminal control commands

            if output == "__VOS_CLEAR__":

                self.lines.clear()


            elif output == "__VOS_EXIT__":

                self.close()


            elif output:

                for line in output.splitlines():

                    if line.strip():

                        self.lines.append(line)


        # Reset input

        self.current_input = ""

        self.cursor_timer = 0.0

        self.cursor_visible = True

    # --------------------------------------------------
    # Rendering
    # --------------------------------------------------

    def draw(self, renderer):
        if self.minimized:
            return

        # 1. Draw base Window framework (borders, title bar, handles)
        super().draw(renderer)
        surface = renderer.surface

        # 2. Extract layout boundaries dynamically
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

        # 3. Paint dark canvas with transparency and dynamic corners
        # Safely check if the window is maximized (using standard property names)
        is_maximized = getattr(self, "maximized", getattr(self, "is_maximized", False))
        corner_radius = 0 if is_maximized else 10

        # Create an alpha-supported surface for transparency
        canvas_surface = pygame.Surface((client_rect.width, client_rect.height), pygame.SRCALPHA)
        
        pygame.draw.rect(
            canvas_surface,
            (20, 20, 22, 10),  # 215 is the alpha transparency level (0-255)
            canvas_surface.get_rect(),
            border_bottom_left_radius=corner_radius,
            border_bottom_right_radius=corner_radius,
        )
        
        # Blit the transparent surface onto the main screen
        surface.blit(canvas_surface, (client_rect.x, client_rect.y))


        # 4. Calculate bounded vertical layout limits
        # Determine maximum capacity of text rows inside window layout frame
        max_visible_lines = (client_rect.height - (self.padding * 2)) // self.line_height
        
        # Account for the active input row at the bottom
        max_history_lines = max_visible_lines - 1 
        
        # Slice history to only track what fits inside viewport (Automatic Vertical Scrolling)
        visible_history = self.lines[-max_history_lines:] if len(self.lines) > max_history_lines else self.lines

        # Draw History Buffer
        text_y = client_rect.y + self.padding
        for line in visible_history:
            text_surface = self.font.render(line, True, (220, 220, 220))
            surface.blit(text_surface, (client_rect.x + self.padding, text_y))
            text_y += self.line_height

        # Draw Active Interactive Command Input Row
        full_prompt = f"{self.prompt_prefix}{self.current_input}"
        if self.cursor_visible:
            full_prompt += "_"
            
        input_surface = self.font.render(full_prompt, True, (120, 255, 120))
        surface.blit(input_surface, (client_rect.x + self.padding, text_y))