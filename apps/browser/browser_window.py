from __future__ import annotations

import html
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pygame

from desktop.ui.core.event import KeyPressEvent, MouseButton, MouseMoveEvent, MousePressEvent, MouseWheelEvent
from desktop.ui.window.window import Window
from resources.cursor_manager import cursor_manager


class BrowserWindow(Window):
    def __init__(self, window_manager=None):
        super().__init__(title="Browser", width=929, height=723, name="Browser")
        self.window_manager = window_manager
        self.transform.position.x = 160
        self.transform.position.y = 70

        # Palette matched strictly to Figma dark design
        self.COLOR_CANVAS = (24, 25, 28)
        self.COLOR_TOOLBAR = (36, 38, 43)
        self.COLOR_TAB_ACTIVE = (52, 56, 64)
        self.COLOR_TAB_INACTIVE = (36, 38, 43)
        self.COLOR_INPUT = (58, 62, 71)
        self.COLOR_CARD = (75, 80, 92)
        self.COLOR_TEXT = (235, 240, 245)
        self.COLOR_MUTED = (150, 158, 170)

        # Typography
        self.font = pygame.font.SysFont("DejaVu Sans", 14, bold=True)
        self.title_font = pygame.font.SysFont("DejaVu Sans", 32, bold=True)
        self.small_font = pygame.font.SysFont("DejaVu Sans", 13)

        # State Variables
        self.tabs = [{"title": "Github Soala7", "url": "vos://home"}, {"title": "New Tab", "url": "vos://home"}]
        self.active_tab_index = 0
        self.address = "vos://home"
        self.address_editing = False
        self.cursor_blink_time = time.time()

        self.history = []
        self.history_index = -1
        self.lines = []
        self.scroll_y = 0
        self.status = "Ready"

        self.load_url(self.address, add_history=True)

    def open(self):
        self.restore()
        if self.window_manager and self not in self.window_manager.windows:
            self.window_manager.add_window(self)
        elif self.window_manager:
            self.window_manager.focus_window(self)

    def load_url(self, url: str, add_history: bool = True):
        url = url.strip()
        if not url:
            return

        if add_history:
            self.history = self.history[:self.history_index + 1]
            self.history.append(url)
            self.history_index += 1

        self.address = url
        self.tabs[self.active_tab_index]["url"] = url
        self.scroll_y = 0

        if url == "vos://home":
            self.tabs[self.active_tab_index]["title"] = "New Tab"
            self.status = "VOS Home"
            self.lines = []
            return

        # Handle real web searches & live URLs
        if not url.startswith(("http://", "https://", "file://", "vos://")):
            if "." in url and " " not in url:
                url = "https://" + url
            else:
                query = urllib.parse.quote(url)
                url = f"https://html.duckduckgo.com/html/?q={query}"

        try:
            if url.startswith("file://"):
                text = Path(url[7:]).read_text(encoding="utf-8", errors="replace")
            else:
                req = urllib.request.Request(
                    url, 
                    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) VOS/1.0 GorgonBrowser"}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    text = response.read(300000).decode("utf-8", errors="replace")
                text = html.unescape(text)

            self.lines = self.parse_web_text(text)
            self.tabs[self.active_tab_index]["title"] = url.replace("https://", "").replace("http://", "").split("/")[0]
            self.status = f"Loaded {url}"
        except Exception as exc:
            self.lines = [f"Failed to load: {url}", "", str(exc)]
            self.status = "Load Error"

    def parse_web_text(self, raw_html: str) -> list[str]:
        text = re.sub(r"<(script|style).*?>.*?</\1>", "", raw_html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        lines = []
        for raw_line in text.splitlines():
            clean = " ".join(raw_line.split())
            if clean:
                lines.extend(clean[i:i + 110] for i in range(0, len(clean), 110))
        return lines[:1000] or ["(empty page)"]

    def handle_event(self, event):
        super().handle_event(event)
        if getattr(event, "handled", False) or not self.active or self.minimized:
            return

        x = int(self.transform.position.x)
        y = int(self.transform.position.y) + self.TITLEBAR_HEIGHT
        w = int(self.transform.size.width) - 4

        if isinstance(event, MouseWheelEvent):
            delta = getattr(event, "delta", getattr(event, "y", 0))
            self.scroll_y = max(0, self.scroll_y - delta * 2)
            event.handled = True

        elif isinstance(event, KeyPressEvent) and self.address_editing:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.address_editing = False
                self.load_url(self.address)
            elif event.key == pygame.K_BACKSPACE:
                self.address = self.address[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.address_editing = False
            elif event.unicode and event.unicode.isprintable():
                self.address += event.unicode
            event.handled = True

        elif isinstance(event, MousePressEvent) and event.button == MouseButton.LEFT:
            # Tab clicks
            for i in range(len(self.tabs)):
                tab_rect = pygame.Rect(x + 120 + (i * 144), y + 6, 136, 30)
                if tab_rect.collidepoint(event.x, event.y):
                    self.active_tab_index = i
                    self.load_url(self.tabs[i]["url"], add_history=False)
                    event.handled = True
                    return

            # Add Tab (+) button
            add_tab_rect = pygame.Rect(x + 120 + (len(self.tabs) * 144) + 4, y + 10, 22, 22)
            if add_tab_rect.collidepoint(event.x, event.y):
                self.tabs.append({"title": "New Tab", "url": "vos://home"})
                self.active_tab_index = len(self.tabs) - 1
                self.load_url("vos://home")
                event.handled = True
                return

            # Address bar click
            address_rect = pygame.Rect(x + 180, y + 46, w - 360, 32)
            if address_rect.collidepoint(event.x, event.y):
                self.address_editing = True
                self.cursor_blink_time = time.time()
            else:
                self.address_editing = False

            event.handled = True

    def draw(self, renderer):
        if self.minimized:
            return
        super().draw(renderer)

        surface = renderer.surface
        x = int(self.transform.position.x) + 2
        y = int(self.transform.position.y) + self.TITLEBAR_HEIGHT
        w = int(self.transform.size.width) - 4
        h = int(self.transform.size.height) - self.TITLEBAR_HEIGHT - 2

        client = pygame.Rect(x, y, w, h)
        old_clip = surface.get_clip()
        surface.set_clip(client)

        # Background Canvas
        pygame.draw.rect(surface, self.COLOR_CANVAS, client)

        # 1. Top Tab Strip
        tab_strip = pygame.Rect(x, y, w, 38)
        pygame.draw.rect(surface, self.COLOR_TOOLBAR, tab_strip)

        for i, tab in enumerate(self.tabs):
            tab_rect = pygame.Rect(x + 120 + (i * 144), y + 8, 136, 30)
            is_active = (i == self.active_tab_index)
            color = self.COLOR_TAB_ACTIVE if is_active else self.COLOR_TAB_INACTIVE
            pygame.draw.rect(surface, color, tab_rect, border_top_left_radius=8, border_top_right_radius=8)
            
            # Tab label truncation
            label = tab["title"][:12] + ".." if len(tab["title"]) > 12 else tab["title"]
            renderer.draw_text(label, self.small_font, self.COLOR_TEXT, pygame.Vector2(tab_rect.x + 12, tab_rect.y + 6))

        # Plus button for new tab
        add_btn = pygame.Rect(x + 120 + (len(self.tabs) * 144) + 6, y + 12, 20, 20)
        renderer.draw_text("+", self.font, self.COLOR_MUTED, pygame.Vector2(add_btn.x + 4, add_btn.y + 1))

        # 2. Main Navigation Toolbar
        nav_toolbar = pygame.Rect(x, y + 38, w, 48)
        pygame.draw.rect(surface, self.COLOR_TOOLBAR, nav_toolbar)

        # Control Icons (Back, Forward, Refresh)
        for idx, symbol in enumerate(["‹", "›", "↻"]):
            btn_rect = pygame.Rect(x + 20 + (idx * 32), y + 48, 26, 26)
            renderer.draw_text(symbol, self.font, self.COLOR_TEXT, pygame.Vector2(btn_rect.x + 8, btn_rect.y + 3))

        # Address / Search Bar
        address_rect = pygame.Rect(x + 180, y + 46, w - 360, 32)
        pygame.draw.rect(surface, (20, 21, 24), address_rect, border_radius=16)

        display_text = self.address
        renderer.draw_text(display_text, self.small_font, self.COLOR_TEXT, pygame.Vector2(address_rect.x + 16, address_rect.y + 8))

        if self.address_editing and (int((time.time() - self.cursor_blink_time) * 2) % 2 == 0):
            text_w = self.small_font.size(display_text)[0]
            cx = address_rect.x + 16 + text_w
            pygame.draw.line(surface, self.COLOR_TEXT, (cx, address_rect.y + 8), (cx, address_rect.bottom - 8), 2)

        # 3. Canvas Content (Home vs Parsed Web Content)
        if self.address == "vos://home":
            self.draw_home_dashboard(renderer, surface, x, y + 86, w, h - 86)
        else:
            self.draw_page_content(renderer, surface, x, y + 86, w, h - 86)

        surface.set_clip(old_clip)

    def draw_home_dashboard(self, renderer, surface, x, y, w, h):
        """Draws the exact Figma layout grid and card spacing."""
        left_margin = 48
        
        # Search Pill (Left Top)
        search_rect = pygame.Rect(x + left_margin, y + 60, 360, 48)
        pygame.draw.rect(surface, self.COLOR_INPUT, search_rect, border_radius=24)
        renderer.draw_text("G", self.font, self.COLOR_TEXT, pygame.Vector2(search_rect.x + 18, search_rect.y + 14))
        renderer.draw_text("Search or enter URL", self.small_font, self.COLOR_MUTED, pygame.Vector2(search_rect.x + 44, search_rect.y + 16))

        # Circular Speed-Dial Icons under Search
        for i in range(3):
            circle_x = x + left_margin + (i * 44)
            pygame.draw.circle(surface, self.COLOR_INPUT, (circle_x + 16, y + 138), 16)
        renderer.draw_text("+", self.font, self.COLOR_MUTED, pygame.Vector2(x + left_margin + 138, y + 128))

        # Hero Card (Right Top)
        hero_card = pygame.Rect(x + w - 380, y + 40, 330, 210)
        pygame.draw.rect(surface, self.COLOR_CARD, hero_card, border_radius=20)
        renderer.draw_text("+", self.title_font, self.COLOR_MUTED, pygame.Vector2(hero_card.centerx - 10, hero_card.centery - 20))

        # Bottom Grid (3 Cards spaced evenly)
        grid_y = y + 280
        card_w = (w - (left_margin * 2) - 40) // 3
        card_h = 200

        for col in range(3):
            card_rect = pygame.Rect(x + left_margin + col * (card_w + 20), grid_y, card_w, card_h)
            pygame.draw.rect(surface, self.COLOR_CARD, card_rect, border_radius=20)
            renderer.draw_text("+", self.title_font, self.COLOR_MUTED, pygame.Vector2(card_rect.centerx - 10, card_rect.centery - 20))

    def draw_page_content(self, renderer, surface, x, y, w, h):
        visible_lines = max(1, (h - 20) // 22)
        self.scroll_y = min(self.scroll_y, max(0, len(self.lines) - visible_lines))

        for idx in range(visible_lines):
            line_idx = self.scroll_y + idx
            if line_idx >= len(self.lines):
                break
            renderer.draw_text(self.lines[line_idx], self.small_font, self.COLOR_TEXT, pygame.Vector2(x + 24, y + 16 + idx * 22))


















        
