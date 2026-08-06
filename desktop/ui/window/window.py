"""
Gorgon OS (VOS)

Window widget.
"""

from __future__ import annotations

import pygame
from desktop.ui.widgets.panel import Panel
from desktop.cursor.cursor_manager import cursor_manager
class Window(Panel):

    TITLEBAR_HEIGHT = 38
    BORDER_RADIUS = 18
    BUTTON_SIZE = 24
    BUTTON_SPACING = 12  # Unified spacing for both drawing and clicking

    def __init__(
        self,
        title: str = "Window",
        width: int = 800,
        height: int = 600,
        name: str = "Window",
        ) -> None:
        self.previous_position = None
        self.previous_size = None

        super().__init__(name)

        self.title = title
        self.transform.resize(width, height)
        self.widgets = []

        self.minimized = False
        self.maximized = False
        self.closed = False

        self.draggable = True
        self.resizable = True
        self.active = True

        self.dragging = False
        self.resizing = False
        self.resize_edge = None
        self.resize_margin = 6  # Slightly wider for better accessibility

        self.min_width = 400
        self.min_height = 300

        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.target_x = self.transform.position.x
        self.target_y = self.transform.position.y
        self.titlebar_height = 38
        self.font = pygame.font.SysFont("DejaVu Sans Mono", 18, bold=True)

    # In your Desktop / OS main update loop:
    def update(self, dt):
        # Reset cursor to default each frame so widgets must actively claim hover states
        cursor_manager.set(cursor_manager.DEFAULT)

        for widget in self.widgets:
            widget.update(dt)

    def _get_button_rects(self, x, y, w):
        """Helper to guarantee matching layout hitboxes for draw and events."""
        close_rect = pygame.Rect(
            x + w - self.BUTTON_SIZE - 10,
            y + 7,
            self.BUTTON_SIZE,
            self.BUTTON_SIZE,
        )
        maximize_rect = pygame.Rect(
            close_rect.x - self.BUTTON_SIZE - self.BUTTON_SPACING,
            y + 7,
            self.BUTTON_SIZE,
            self.BUTTON_SIZE,
        )
        minimize_rect = pygame.Rect(
            maximize_rect.x - self.BUTTON_SIZE - self.BUTTON_SPACING,
            y + 7,
            self.BUTTON_SIZE,
            self.BUTTON_SIZE,
        )
        return close_rect, maximize_rect, minimize_rect

    def draw(self, renderer):
        if self.minimized:
            return

        surface = renderer.surface

        x, y = int(self.transform.position.x), int(self.transform.position.y)
        w, h = int(self.transform.size.width), int(self.transform.size.height)
        
        # Dynamically determine corner radius
        current_radius = 0 if self.maximized else self.BORDER_RADIUS

        # Shadow Effect (only draw if not maximized so it doesn't bleed off screen)
        if not self.maximized:
            shadow = pygame.Surface((w + 16, h + 16), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (0, 0, 0, 45), shadow.get_rect(), border_radius=current_radius + 6)
            surface.blit(shadow, (x - 8, y - 4))

        # Create an alpha-supported surface for window transparency
        window_surface = pygame.Surface((w, h), pygame.SRCALPHA)

        # Set transparent colors
        border = (20, 20, 22, 215) if self.active else (70, 70, 80, 215)
        titlebar_color = (42, 42, 48, 230)

        # Window Frame Background (drawn locally at 0,0 on the temporary surface)
        pygame.draw.rect(window_surface, border, window_surface.get_rect(), border_radius=current_radius)
        pygame.draw.rect(window_surface, border, window_surface.get_rect(), 1, border_radius=current_radius)

        # Title bar background
        titlebar = pygame.Rect(0, 0, w, self.TITLEBAR_HEIGHT)
        pygame.draw.rect(window_surface, titlebar_color, titlebar, border_top_left_radius=current_radius, border_top_right_radius=current_radius)

        # Blit the transparent window surface to the main renderer
        surface.blit(window_surface, (x, y))

        # Text and Buttons can be drawn normally over the main surface
        renderer.draw_text(self.title, self.font, (235, 235, 235), pygame.Vector2(x + 16, y + 9))

        # Buttons Rendering Layout
        close_rect, maximize_rect, minimize_rect = self._get_button_rects(x, y, w)

        pygame.draw.rect(surface, (70, 70, 78), minimize_rect, border_radius=6)
        pygame.draw.rect(surface, (70, 70, 78), maximize_rect, border_radius=6)
        pygame.draw.rect(surface, (150, 60, 60), close_rect, border_radius=6)

        # Icons markup code...
        pygame.draw.line(surface, (230, 230, 230), (minimize_rect.x + 6, minimize_rect.centery), (minimize_rect.right - 6, minimize_rect.centery), 2)
        if self.maximized:
            pygame.draw.rect(surface, (230, 230, 230), pygame.Rect(maximize_rect.x + 7, maximize_rect.y + 9, 8, 8), 2)
        else:
            pygame.draw.rect(surface, (230, 230, 230), pygame.Rect(maximize_rect.x + 6, maximize_rect.y + 6, 12, 12), 2)
        pygame.draw.line(surface, (255, 255, 255), (close_rect.x + 7, close_rect.y + 7), (close_rect.right - 7, close_rect.bottom - 7), 2)
        pygame.draw.line(surface, (255, 255, 255), (close_rect.right - 7, close_rect.y + 7), (close_rect.x + 7, close_rect.bottom - 7), 2)

    def minimize(self):
        self.minimized = True

    def maximize(self):
        if self.maximized: return
        self.previous_position = (self.transform.position.x, self.transform.position.y)
        self.previous_size = (self.transform.size.width, self.transform.size.height)
        surface = pygame.display.get_surface()
        self.transform.position.x = 0
        self.transform.position.y = 0
        self.transform.resize(surface.get_width(), surface.get_height())
        self.maximized = True

    def restore(self):
        self.minimized = False
        if self.maximized and self.previous_position:
            self.transform.position.x = self.previous_position[0]
            self.transform.position.y = self.previous_position[1]
            self.transform.resize(self.previous_size[0], self.previous_size[1])
        self.maximized = False

    def close(self):
        cursor_manager.set(cursor_manager.DEFAULT)
        self.closed = True
        self.destroy()

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def get_resize_edge(self, mx, my):
        if self.maximized:
            return None  # Can't resize maximized window
            
        x, y = self.transform.position.x, self.transform.position.y
        w, h = self.transform.size.width, self.transform.size.height
        m = self.resize_margin

        left = abs(mx - x) <= m
        right = abs(mx - (x + w)) <= m
        top = abs(my - y) <= m
        bottom = abs(my - (y + h)) <= m

        if left and top: return "top_left"
        if right and top: return "top_right"
        if left and bottom: return "bottom_left"
        if right and bottom: return "bottom_right"
        if left: return "left"
        if right: return "right"
        if top: return "top"
        if bottom: return "bottom"
        return None

    def handle_event(self, event):
        from desktop.ui.core.event import MousePressEvent, MouseReleaseEvent, MouseMoveEvent, MouseButton

        x, y = self.transform.position.x, self.transform.position.y
        w, h = self.transform.size.width, self.transform.size.height

        if isinstance(event, MousePressEvent) and event.button == MouseButton.LEFT:
            close_rect, maximize_rect, minimize_rect = self._get_button_rects(x, y, w)

            # 1. UI Window Control Hits (Priority #1)
            if close_rect.collidepoint(event.x, event.y):
                self.close()
                event.handled = True
                return
            if maximize_rect.collidepoint(event.x, event.y):
                if self.maximized: self.restore()
                else: self.maximize()
                event.handled = True
                return
            if minimize_rect.collidepoint(event.x, event.y):
                self.minimize()
                event.handled = True
                return

            # 2. Resize Border Checking (Priority #2)
            edge = self.get_resize_edge(event.x, event.y)
            if edge and self.resizable:
                self.resizing = True
                self.resize_edge = edge
                event.handled = True
                return

            # 3. Titlebar Drag Checking (Priority #3)
            titlebar_rect = pygame.Rect(x, y, w - 120, self.TITLEBAR_HEIGHT)
            if titlebar_rect.collidepoint(event.x, event.y) and self.draggable and not self.maximized:
                self.dragging = True
                self.drag_offset_x = event.x - x
                self.drag_offset_y = event.y - y
                event.handled = True
                return

        elif isinstance(event, MouseReleaseEvent) and event.button == MouseButton.LEFT:
            self.dragging = False
            self.resizing = False
            self.resize_edge = None

        elif isinstance(event, MouseMoveEvent):
            # Check if mouse is inside this window's bounds
            in_window = x <= event.x <= x + w and y <= event.y <= y + h

            # Only track systemic cursor icons if not actively dragging or resizing
            if not self.dragging and not self.resizing:
                if not in_window:
                    cursor_manager.set(cursor_manager.DEFAULT)
                else:
                    edge = self.get_resize_edge(event.x, event.y)
                    close_rect, maximize_rect, minimize_rect = self._get_button_rects(x, y, w)
                    
                    # Strictly limit titlebar move region to the draggable bar area (excluding buttons)
                    titlebar_rect = pygame.Rect(x, y, minimize_rect.x - x, self.TITLEBAR_HEIGHT)

                    if edge in ("left", "right"):
                        cursor_manager.set(cursor_manager.RESIZE_H)
                    elif edge in ("top", "bottom"):
                        cursor_manager.set(cursor_manager.RESIZE_V)
                    elif edge in ("top_left", "bottom_right"):
                        cursor_manager.set(cursor_manager.RESIZE_L)
                    elif edge in ("top_right", "bottom_left"):
                        cursor_manager.set(cursor_manager.RESIZE_R)
                    elif close_rect.collidepoint(event.x, event.y) or maximize_rect.collidepoint(event.x, event.y) or minimize_rect.collidepoint(event.x, event.y):
                        cursor_manager.set(cursor_manager.POINTER)
                    elif titlebar_rect.collidepoint(event.x, event.y) and self.draggable and not self.maximized:
                        cursor_manager.set(cursor_manager.MOVE)
                    else:
                        cursor_manager.set(cursor_manager.DEFAULT)

            # Process window resizing transformations
            if self.resizing:
                if "right" in self.resize_edge:
                    w = max(self.min_width, event.x - x)
                if "bottom" in self.resize_edge:
                    h = max(self.min_height, event.y - y)
                if "left" in self.resize_edge:
                    new_x = min(event.x, x + w - self.min_width)
                    w += x - new_x
                    x = new_x
                if "top" in self.resize_edge:
                    new_y = min(event.y, y + h - self.min_height)
                    h += y - new_y
                    y = new_y

                self.transform.position.x = x
                self.transform.position.y = y
                self.transform.resize(w, h)
                event.handled = True
                return

            # Process window dragging movement
            if self.dragging:
                self.transform.position.x = event.x - self.drag_offset_x
                self.transform.position.y = event.y - self.drag_offset_y
                event.handled = True
                return




















                