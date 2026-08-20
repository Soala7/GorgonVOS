from __future__ import annotations

from pathlib import Path

import pygame

from desktop.ui.core.event import KeyPressEvent, MouseButton, MousePressEvent
from desktop.ui.window.window import Window


class MusicWindow(Window):
    AUDIO_EXTENSIONS = {".mp3", ".ogg", ".wav", ".flac"}

    def __init__(self, window_manager=None):
        super().__init__(title="Music Player", width=720, height=520, name="MusicPlayer")
        self.window_manager = window_manager
        self.transform.position.x = 240
        self.transform.position.y = 110
        self.font = pygame.font.SysFont("DejaVu Sans", 18, bold=True)
        self.small_font = pygame.font.SysFont("DejaVu Sans", 14)
        self.tracks = self.find_tracks()
        self.selected = 0
        self.scroll_offset = 0
        self.volume = 0.8
        self.playing = False
        self.paused = False
        self.status = "Choose a track"
        self._load_selected()
        pygame.mixer.music.set_volume(self.volume)

    @classmethod
    def find_tracks(cls):
        roots = [Path("assets/music"), Path("assets/sounds")]
        tracks = []
        for root in roots:
            if root.exists():
                tracks.extend(path for path in sorted(root.iterdir()) if path.suffix.lower() in cls.AUDIO_EXTENSIONS)
        return tracks

    def _load_selected(self):
        if not self.tracks:
            self.status = "Add audio files to assets/music"
            return
        try:
            pygame.mixer.music.load(str(self.tracks[self.selected]))
            self.status = self.tracks[self.selected].stem
        except pygame.error as exc:
            self.status = f"Cannot play track: {exc}"

    def open(self):
        self.restore()
        self.tracks = self.find_tracks()
        if self.tracks:
            self.selected = min(self.selected, len(self.tracks) - 1)
            self._load_selected()
        if self.window_manager and self not in self.window_manager.windows:
            self.window_manager.add_window(self)
        elif self.window_manager:
            self.window_manager.focus_window(self)

    def update(self, dt):
        super().update(dt)
        if self.playing and not pygame.mixer.music.get_busy() and not self.paused:
            self.playing = False
            self.next_track(auto_play=True)

    def next_track(self, auto_play=False):
        if not self.tracks:
            return
        self.select_track((self.selected + 1) % len(self.tracks))
        if auto_play:
            self.toggle_play()

    def previous_track(self):
        if self.tracks:
            self.select_track((self.selected - 1) % len(self.tracks))

    def set_volume(self, value):
        self.volume = max(0.0, min(1.0, value))
        pygame.mixer.music.set_volume(self.volume)

    def select_track(self, index):
        if not self.tracks:
            return
        self.selected = max(0, min(index, len(self.tracks) - 1))
        self.scroll_offset = max(0, min(self.scroll_offset, self.selected))
        self._load_selected()
        self.playing = False
        self.paused = False

    def toggle_play(self):
        if not self.tracks:
            return
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.playing = True
            return
        if self.playing:
            pygame.mixer.music.pause()
            self.paused = True
            self.status = "Paused"
            return
        pygame.mixer.music.play()
        self.playing = True
        self.status = f"Playing {self.tracks[self.selected].stem}"

    def handle_event(self, event):
        super().handle_event(event)
        if getattr(event, "handled", False) or not self.active or self.minimized:
            return
        if isinstance(event, KeyPressEvent):
            if event.key == pygame.K_SPACE:
                self.toggle_play()
                event.handled = True
            elif event.key in (pygame.K_UP, pygame.K_DOWN) and self.tracks:
                self.select_track(self.selected + (-1 if event.key == pygame.K_UP else 1))
                event.handled = True
            elif event.key == pygame.K_LEFT:
                self.previous_track()
                event.handled = True
            elif event.key == pygame.K_RIGHT:
                self.next_track()
                event.handled = True
        elif isinstance(event, MousePressEvent) and event.button == MouseButton.LEFT:
            x = int(self.transform.position.x)
            y = int(self.transform.position.y) + self.TITLEBAR_HEIGHT
            width = int(self.transform.size.width) - 4
            height = int(self.transform.size.height) - self.TITLEBAR_HEIGHT - 2
            content_x = x + 30
            content_right = x + width - 30
            if pygame.Rect(x + 30, y + height - 64, 54, 44).collidepoint(event.x, event.y):
                self.previous_track()
                event.handled = True
            elif pygame.Rect(x + width - 84, y + height - 64, 54, 44).collidepoint(event.x, event.y):
                self.next_track()
                event.handled = True
            elif pygame.Rect(x + 100, y + height - 64, 180, 44).collidepoint(event.x, event.y):
                self.toggle_play()
                event.handled = True
            elif pygame.Rect(content_x, y + height - 110, content_right - content_x, 12).collidepoint(event.x, event.y):
                self.set_volume((event.x - content_x) / max(1, content_right - content_x))
                event.handled = True
            else:
                visible_rows = max(1, (height - 250) // 32)
                for row_index in range(visible_rows):
                    index = self.scroll_offset + row_index
                    if index >= len(self.tracks):
                        break
                    row = pygame.Rect(content_x, y + 205 + row_index * 32, content_right - content_x, 28)
                    if row.collidepoint(event.x, event.y):
                        self.select_track(index)
                        event.handled = True
                        break

    def draw(self, renderer):
        if self.minimized:
            return
        super().draw(renderer)
        surface = renderer.surface
        x = int(self.transform.position.x) + 2
        y = int(self.transform.position.y) + self.TITLEBAR_HEIGHT
        width = int(self.transform.size.width) - 4
        height = int(self.transform.size.height) - self.TITLEBAR_HEIGHT - 2
        pygame.draw.rect(surface, (13, 16, 32), (x, y, width, height))
        pygame.draw.rect(surface, (28, 35, 70), (x + 24, y + 24, width - 48, 120), border_radius=16)
        title = self.tracks[self.selected].stem if self.tracks else "No music found"
        renderer.draw_text(title, self.font, (242, 245, 255), pygame.Vector2(x + 44, y + 52))
        renderer.draw_text(self.status, self.small_font, (145, 165, 215), pygame.Vector2(x + 44, y + 84))
        renderer.draw_text("UP/DOWN select   SPACE play/pause", self.small_font, (120, 135, 180), pygame.Vector2(x + 44, y + 112))
        renderer.draw_text("PLAYLIST  assets/music + assets/sounds", self.font, (120, 210, 255), pygame.Vector2(x + 30, y + 166))
        if not self.tracks:
            renderer.draw_text("Place .mp3, .ogg, .wav, or .flac files in assets/music", self.small_font, (210, 215, 230), pygame.Vector2(x + 30, y + 215))
        list_top = y + 205
        list_bottom = y + height - 130
        visible_rows = max(1, (list_bottom - list_top) // 32)
        self.scroll_offset = min(self.scroll_offset, max(0, len(self.tracks) - visible_rows))
        if self.selected >= self.scroll_offset + visible_rows:
            self.scroll_offset = self.selected - visible_rows + 1
        if self.selected < self.scroll_offset:
            self.scroll_offset = self.selected
        for row_index in range(visible_rows):
            index = self.scroll_offset + row_index
            if index >= len(self.tracks):
                break
            track = self.tracks[index]
            row = pygame.Rect(x + 30, list_top + row_index * 32, width - 60, 28)
            if index == self.selected:
                pygame.draw.rect(surface, (40, 88, 135), row, border_radius=7)
            label = f"{index + 1:02d}  {track.parent.name}/{track.stem}"
            while self.small_font.size(label)[0] > row.width - 20 and len(label) > 12:
                label = label[:-4] + "..."
            renderer.draw_text(label, self.small_font, (235, 240, 255), pygame.Vector2(row.x + 10, row.y + 5))
        progress = 0.0
        if self.playing or self.paused:
            try:
                length = pygame.mixer.Sound(str(self.tracks[self.selected])).get_length()
                progress = max(0.0, min(1.0, pygame.mixer.music.get_pos() / 1000 / length)) if length else 0.0
            except pygame.error:
                progress = 0.0
        progress_rect = pygame.Rect(x + 30, y + height - 112, width - 60, 6)
        pygame.draw.rect(surface, (55, 65, 100), progress_rect, border_radius=3)
        pygame.draw.rect(surface, (88, 190, 255), (progress_rect.x, progress_rect.y, int(progress_rect.width * progress), progress_rect.height), border_radius=3)
        volume_rect = pygame.Rect(x + 30, y + height - 92, width - 60, 5)
        pygame.draw.rect(surface, (55, 65, 100), volume_rect, border_radius=3)
        pygame.draw.rect(surface, (110, 220, 170), (volume_rect.x, volume_rect.y, int(volume_rect.width * self.volume), volume_rect.height), border_radius=3)
        renderer.draw_text(f"VOLUME {int(self.volume * 100)}%", self.small_font, (160, 175, 215), pygame.Vector2(x + 30, y + height - 82))
        button = pygame.Rect(x + 100, y + height - 64, 180, 44)
        pygame.draw.rect(surface, (44, 170, 125) if self.playing and not self.paused else (46, 105, 190), button, border_radius=12)
        label = "PAUSE" if self.playing and not self.paused else "PLAY"
        renderer.draw_text(label, self.font, (255, 255, 255), pygame.Vector2(button.centerx - 28, button.y + 11))
        for button_rect, label in ((pygame.Rect(x + 30, y + height - 64, 54, 44), "<<"), (pygame.Rect(x + width - 84, y + height - 64, 54, 44), ">>")):
            pygame.draw.rect(surface, (42, 75, 130), button_rect, border_radius=10)
            renderer.draw_text(label, self.font, (255, 255, 255), pygame.Vector2(button_rect.centerx - 10, button_rect.y + 11))
