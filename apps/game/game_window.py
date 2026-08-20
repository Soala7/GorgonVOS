from __future__ import annotations

import math
import random

import pygame

from desktop.ui.core.event import KeyPressEvent
from desktop.ui.window.window import Window


class GameWindow(Window):
    TILE_SIZE = 25
    ROWS = 18
    COLS = 24
    BOARD_WIDTH = TILE_SIZE * COLS
    BOARD_HEIGHT = TILE_SIZE * ROWS

    BLACK = (5, 6, 16)
    BLUE = (36, 66, 190)
    BLUE_DARK = (13, 24, 82)
    BLUE_GLOW = (76, 122, 255)
    YELLOW = (255, 232, 24)
    RED = (242, 76, 76)
    WHITE = (236, 240, 255)
    GREEN = (88, 232, 126)
    GHOST_BLUE = (75, 125, 238)
    HUD = (16, 18, 38)
    HUD_LINE = (58, 76, 150)

    def __init__(self, window_manager=None):
        super().__init__(title="PAC-MAN PRO", width=660, height=540, name="PacMan")
        self.window_manager = window_manager
        self.transform.position.x = 190
        self.transform.position.y = 80
        self.font = pygame.font.SysFont("DejaVu Sans", 16, bold=True)
        self.small_font = pygame.font.SysFont("DejaVu Sans", 13)
        self.elapsed = 0.0
        self.move_timer = 0.0
        self.mouth_angle = 18
        self.mouth_opening = True
        self.score = 0
        self.level = 1
        self.game_over = False
        self.won = False
        self.frightened_until = 0.0
        self.maze = []
        self.player_x = 1
        self.player_y = 1
        self.player_dir = (0, 0)
        self.next_dir = (0, 0)
        self.ghosts = []
        self.ghost_dirs = []
        self.reset_level()

    def reset_level(self):
        self.maze = self.generate_maze()
        self.player_x, self.player_y = 1, 1
        self.player_dir = (0, 0)
        self.next_dir = (0, 0)
        spawn_points = [
            (self.COLS - 2, 1),
            (1, self.ROWS - 2),
            (self.COLS - 2, self.ROWS - 2),
            (self.COLS // 2, self.ROWS // 2),
        ]
        for x, y in [(1, 1), *spawn_points]:
            self.maze[y][x] = 0
        self.ghosts = [[x, y] for x, y in spawn_points]
        self.ghost_dirs = [(0, 0) for _ in self.ghosts]
        self.won = False

    def generate_maze(self):
        maze = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        for y in range(self.ROWS):
            for x in range(self.COLS):
                if x in (0, self.COLS - 1) or y in (0, self.ROWS - 1):
                    maze[y][x] = 1
        for y in range(2, self.ROWS - 2, 2):
            for x in range(2, self.COLS - 2, 2):
                if random.random() < 0.55:
                    maze[y][x] = 1
                    dx, dy = random.choice(((0, 1), (0, -1), (1, 0), (-1, 0)))
                    if 0 < x + dx < self.COLS - 1 and 0 < y + dy < self.ROWS - 1:
                        maze[y + dy][x + dx] = 1
        open_cells = [
            (x, y)
            for y in range(1, self.ROWS - 1)
            for x in range(1, self.COLS - 1)
            if maze[y][x] == 0 and (x, y) != (1, 1)
        ]
        for x, y in random.sample(open_cells, min(4, len(open_cells))):
            maze[y][x] = 3
        return maze

    def can_move(self, x, y):
        return 0 <= x < self.COLS and 0 <= y < self.ROWS and self.maze[y][x] != 1

    def restart(self):
        self.score = 0
        self.level = 1
        self.game_over = False
        self.frightened_until = 0.0
        self.reset_level()

    def set_direction(self, direction):
        self.next_dir = direction

    def update(self, dt):
        super().update(dt)
        if not self.active or self.minimized or self.game_over or self.won:
            return
        self.elapsed += dt
        self.move_timer += dt
        self.mouth_angle += (90 if self.mouth_opening else -90) * dt
        if self.mouth_angle >= 40:
            self.mouth_angle = 40
            self.mouth_opening = False
        elif self.mouth_angle <= 4:
            self.mouth_angle = 4
            self.mouth_opening = True
        if self.move_timer < 0.11:
            return
        self.move_timer = 0.0
        self.move_player()
        self.move_ghosts()

    def move_player(self):
        if self.can_move(self.player_x + self.next_dir[0], self.player_y + self.next_dir[1]):
            self.player_dir = self.next_dir
        if self.can_move(self.player_x + self.player_dir[0], self.player_y + self.player_dir[1]):
            self.player_x += self.player_dir[0]
            self.player_y += self.player_dir[1]
        tile = self.maze[self.player_y][self.player_x]
        if tile == 0:
            self.maze[self.player_y][self.player_x] = 2
            self.score += 10
        elif tile == 3:
            self.maze[self.player_y][self.player_x] = 2
            self.score += 50
            self.frightened_until = self.elapsed + 5.0
        pellets_left = sum(row.count(0) + row.count(3) for row in self.maze)
        if pellets_left == 0:
            self.level += 1
            self.reset_level()

    def move_ghosts(self):
        frightened = self.elapsed < self.frightened_until
        directions = ((0, -1), (0, 1), (-1, 0), (1, 0))
        for index, ghost in enumerate(self.ghosts):
            x, y = ghost
            current = self.ghost_dirs[index]
            valid = [direction for direction in directions if self.can_move(x + direction[0], y + direction[1])]
            if valid and (random.random() < 0.2 or not self.can_move(x + current[0], y + current[1])):
                if frightened:
                    self.ghost_dirs[index] = random.choice(valid)
                else:
                    self.ghost_dirs[index] = min(valid, key=lambda direction: abs(x + direction[0] - self.player_x) + abs(y + direction[1] - self.player_y))
            ghost[0] += self.ghost_dirs[index][0]
            ghost[1] += self.ghost_dirs[index][1]
            if ghost == [self.player_x, self.player_y]:
                if frightened:
                    self.score += 200
                    ghost[:] = [self.COLS // 2, self.ROWS // 2]
                else:
                    self.game_over = True

    def handle_event(self, event):
        super().handle_event(event)
        if getattr(event, "handled", False) or not self.active or self.minimized:
            return
        if not isinstance(event, KeyPressEvent):
            return
        directions = {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
        }
        if event.key in directions:
            self.set_direction(directions[event.key])
            event.handled = True
        elif event.key == pygame.K_r and (self.game_over or self.won):
            self.restart()
            event.handled = True

    def draw(self, renderer):
        if self.minimized:
            return
        super().draw(renderer)
        x = int(self.transform.position.x) + 2
        y = int(self.transform.position.y) + self.TITLEBAR_HEIGHT
        surface = renderer.surface
        board = pygame.Rect(x, y, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        pygame.draw.rect(surface, self.BLACK, board)
        pygame.draw.rect(surface, self.BLUE_DARK, board, 2)
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                center = (x + col * self.TILE_SIZE + self.TILE_SIZE // 2, y + row * self.TILE_SIZE + self.TILE_SIZE // 2)
                if tile == 1:
                    wall_rect = pygame.Rect(x + col * self.TILE_SIZE + 2, y + row * self.TILE_SIZE + 2, self.TILE_SIZE - 4, self.TILE_SIZE - 4)
                    pygame.draw.rect(surface, self.BLUE_DARK, wall_rect.inflate(2, 2), border_radius=5)
                    pygame.draw.rect(surface, self.BLUE, wall_rect, border_radius=5)
                    pygame.draw.rect(surface, self.BLUE_GLOW, wall_rect, 1, border_radius=5)
                elif tile == 0:
                    pygame.draw.circle(surface, (255, 255, 255, 80), center, 4)
                    pygame.draw.circle(surface, self.WHITE, center, 2)
                elif tile == 3:
                    pulse = 7 + int(2 * math.sin(self.elapsed * 7))
                    pygame.draw.circle(surface, (88, 232, 126, 45), center, pulse + 4)
                    pygame.draw.circle(surface, self.GREEN, center, pulse)
                    pygame.draw.circle(surface, (214, 255, 224), center, max(2, pulse // 3))
        self.draw_player(surface, x, y)
        frightened = self.elapsed < self.frightened_until
        for ghost in self.ghosts:
            self.draw_ghost(surface, x, y, ghost, frightened)
        hud = pygame.Rect(x, y + self.BOARD_HEIGHT, self.BOARD_WIDTH, 48)
        pygame.draw.rect(surface, self.HUD, hud)
        pygame.draw.line(surface, self.HUD_LINE, (hud.x, hud.y), (hud.right, hud.y), 2)
        pygame.draw.line(surface, self.BLUE_DARK, (hud.x, hud.bottom - 2), (hud.right, hud.bottom - 2), 2)
        self.draw_text(surface, f"SCORE {self.score}", x + 12, hud.y + 8, self.WHITE, self.font)
        self.draw_text(surface, f"LEVEL {self.level}", x + 220, hud.y + 8, self.YELLOW, self.font)
        if frightened:
            remaining = max(0, int(self.frightened_until - self.elapsed))
            self.draw_text(surface, f"POWER {remaining}", x + 420, hud.y + 8, self.GREEN, self.font)
            pygame.draw.rect(surface, self.GREEN, (x + 420, hud.y + 32, max(2, int(70 * (self.frightened_until - self.elapsed) / 5)), 3))
        if self.game_over or self.won:
            overlay = pygame.Surface((self.BOARD_WIDTH, self.BOARD_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            surface.blit(overlay, board.topleft)
            message = "YOU WIN!" if self.won else "GAME OVER"
            text = self.font.render(f"{message}  Press R to restart", True, self.YELLOW if self.won else self.RED)
            surface.blit(text, text.get_rect(center=board.center))

    def draw_player(self, surface, x, y):
        px = x + self.player_x * self.TILE_SIZE + self.TILE_SIZE // 2
        py = y + self.player_y * self.TILE_SIZE + self.TILE_SIZE // 2
        radius = self.TILE_SIZE // 2 - 2
        if self.player_dir == (0, 0):
            pygame.draw.circle(surface, self.YELLOW, (px, py), radius)
        else:
            angle = math.atan2(-self.player_dir[1], self.player_dir[0])
            mouth = math.radians(self.mouth_angle)
            points = [(px, py), (px + math.cos(angle + mouth) * radius, py - math.sin(angle + mouth) * radius), (px + math.cos(angle - mouth) * radius, py - math.sin(angle - mouth) * radius)]
            pygame.draw.polygon(surface, self.YELLOW, points)
            pygame.draw.arc(surface, (255, 246, 110), (px - radius, py - radius, radius * 2, radius * 2), -angle + mouth, -angle - mouth + math.tau, 2)
        eye_x = px + (4 if self.player_dir != (-1, 0) else -4)
        pygame.draw.circle(surface, (35, 35, 45), (eye_x, py - 6), 2)

    def draw_ghost(self, surface, x, y, ghost, frightened):
        gx = x + ghost[0] * self.TILE_SIZE + self.TILE_SIZE // 2
        gy = y + ghost[1] * self.TILE_SIZE + self.TILE_SIZE // 2
        color = self.GHOST_BLUE if frightened else self.RED
        radius = self.TILE_SIZE // 2 - 2
        pygame.draw.circle(surface, color, (gx, gy - 2), radius)
        pygame.draw.rect(surface, color, (gx - radius, gy - 2, radius * 2, radius + 5))
        foot_y = gy + radius + 1
        for foot_x in (gx - radius + 4, gx, gx + radius - 4):
            pygame.draw.circle(surface, color, (foot_x, foot_y), 4)
        eye_color = self.YELLOW if frightened else self.WHITE
        pygame.draw.circle(surface, eye_color, (gx - 4, gy - 3), 3)
        pygame.draw.circle(surface, eye_color, (gx + 4, gy - 3), 3)
        if not frightened:
            pygame.draw.circle(surface, self.BLUE_DARK, (gx - 4, gy - 3), 1)
            pygame.draw.circle(surface, self.BLUE_DARK, (gx + 4, gy - 3), 1)

    @staticmethod
    def draw_text(surface, text, x, y, color, font):
        surface.blit(font.render(text, True, color), (x, y))
