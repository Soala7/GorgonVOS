from __future__ import annotations

import math
import pygame
import datetime

from desktop.ui.widgets.widget import Widget
from desktop.assests.icon_manager import IconManager

class Launcher(Widget):

    def __init__(self, app_launcher=None) -> None:

        self.app_launcher = app_launcher

        self.snake = IconManager.get("launcher/snake", 350)
        self.user_icon = IconManager.get("launcher/user", 36)

        self.breathing_time = 0.0

        self.animation = 0.0
        self.animation_speed = 8.0

        self.search_hover_anim = 0.0
        self.bottom_search_hover_anim = 0.0
        self.search_anim_speed = 5.5

        self.clock_is_digital = False
        self.clock_ripple_radius = 0.0
        self.custom_time_offset = 0

        self.power_icons = [
            IconManager.get("launcher/logout", 40),
            IconManager.get("launcher/sleep", 40),
            IconManager.get("launcher/restart", 40),
            IconManager.get("launcher/shutdown", 40),
        ]

        self.wifi_icon = IconManager.get("launcher/wifi", 36)
        self.notification_icon = IconManager.get("launcher/notification", 36)

        self.recent_icons = [
            IconManager.get("launcher/browser", 90),
            None,
        ]

        self.sidebar_icons = [
            IconManager.get("launcher/explorer", 36),
            IconManager.get("launcher/game", 36),
            IconManager.get("launcher/terminal", 36),
            IconManager.get("launcher/settings", 36),
        ]
        self.plus_icon_base = IconManager.get("launcher/plus", 36)

        self.my_apps_under = [
            IconManager.get("launcher/browser", 42),
            IconManager.get("launcher/camera", 42),
        ]
        self.my_apps_side = [
            IconManager.get("launcher/gallery", 42),
            None,
        ]

        self.clock_cover = IconManager.get("launcher/clock_cover", 110)

        self.search_icon = IconManager.get("launcher/search", 24)

        super().__init__("Launcher")

        self.title_font = pygame.font.SysFont("arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("arial", 22)
        self.large_font = pygame.font.SysFont("arial", 24, bold=True)
        self.apps_label_font = pygame.font.SysFont("arial", 25, bold=True)
        self.time_font = pygame.font.SysFont("arial", 30, bold=True)
        self.card_font = pygame.font.SysFont("arial", 16)
        self.clock_btn_font = pygame.font.SysFont("arial", 14, bold=True)
        self.search_font = pygame.font.SysFont("arial", 18)

        self.visible = False

    def open(self):
        """Make the launcher visible."""
        self.visible = True

    def close(self):
        """Hide the launcher."""
        self.visible = False

    def toggle(self):
        """Toggle launcher visibility state."""
        self.visible = not self.visible
        print(f"[Launcher] Visible = {self.visible}")

    def launch_app(self, app_name: str) -> bool:
        if self.app_launcher is None:
            print(f"[Launcher] No AppLauncher connected for '{app_name}'.")
            return False

        try:
            launched = self.app_launcher.launch_app(app_name)
        except Exception as exc:
            print(f"[Launcher] Failed to launch '{app_name}': {exc}")
            return False

        if launched:
            self.close()
        return bool(launched)

    def update(self, dt):
        """Handle animations and value updates based on delta-time (dt)."""
        target = 1.0 if self.visible else 0.0

        if self.animation < target:
            self.animation += self.animation_speed * dt
            self.animation = min(self.animation, target)

        elif self.animation > target:
            self.animation -= self.animation_speed * dt
            self.animation = max(self.animation, target)

        if self.visible:
            self.breathing_time += dt

            self.clock_ripple_radius += 35 * dt
            if self.clock_ripple_radius > 75:
                self.clock_ripple_radius = 55

            mouse_pos = pygame.mouse.get_pos()

            search_rect = pygame.Rect(470 + 180, 330 + 18, 300, 48)
            search_target = 1.0 if search_rect.collidepoint(mouse_pos) else 0.0

            if self.search_hover_anim < search_target:
                self.search_hover_anim = min(1.0, self.search_hover_anim + self.search_anim_speed * dt)
            elif self.search_hover_anim > search_target:
                self.search_hover_anim = max(0.0, self.search_hover_anim - self.search_anim_speed * dt)

            bottom_search_rect = pygame.Rect(470 + 135, 330 + 515, 310, 45)
            bottom_target = 1.0 if bottom_search_rect.collidepoint(mouse_pos) else 0.0

            if self.bottom_search_hover_anim < bottom_target:
                self.bottom_search_hover_anim = min(1.0, self.bottom_search_hover_anim + self.search_anim_speed * dt)
            elif self.bottom_search_hover_anim > bottom_target:
                self.bottom_search_hover_anim = max(0.0, self.bottom_search_hover_anim - self.search_anim_speed * dt)

    def draw_smooth_rect(self, target_surface, rect, color, border_radius=0, width=0):
        """Draws a clean, anti-aliased rounded rectangle without color double-blending bugs."""
        if rect.width <= 0 or rect.height <= 0:
            return

        scaler = 1
        scratch = pygame.Surface((rect.width * scaler, rect.height * scaler), pygame.SRCALPHA)

        if width == 0:
            pygame.draw.rect(scratch, color, scratch.get_rect(), border_radius=border_radius * scaler)
        else:
            pygame.draw.rect(scratch, color, scratch.get_rect(), width * scaler, border_radius=border_radius * scaler)

        result = pygame.transform.smoothscale(scratch, rect.size)
        target_surface.blit(result, rect.topleft)

    def draw_alpha_circle(self, surface, color, center, radius):
        """Draws a true alpha-blended circle to fix the solid white block bug."""
        circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, color, (radius, radius), radius)
        surface.blit(circle_surface, (center[0] - radius, center[1] - radius))

    def draw_hover_icon(self, surface, icon, center, base_size, hover=False):
        """Draw an icon with a subtle hover-based growth effect (16% larger on hover)."""
        if not icon:
            return

        size = int(base_size * 1.16) if hover else base_size
        scaled_icon = pygame.transform.smoothscale(icon, (size, size))
        surface.blit(scaled_icon, (center[0] - size // 2, center[1] - size // 2))

    def handle_click(self, mouse_pos) -> bool:
        """Processes launcher interactions.
        Closes launcher if click lands outside of all interactive panels.
        Returns True if an interaction was processed, False otherwise.
        """
        if not self.visible:
            return False

        panel_y = 330
        panel_rect = pygame.Rect(470, panel_y, 760, 580)
        qa_panel_rect = pygame.Rect(panel_rect.right + 22, panel_rect.y, 78, panel_rect.height)

        if not panel_rect.collidepoint(mouse_pos) and not qa_panel_rect.collidepoint(mouse_pos):
            print("[Launcher] Clicked outside boundaries. Closing launcher.")
            self.visible = False
            return True

        rail = pygame.Rect(panel_rect.x + 18, panel_rect.y + 15, 70, panel_rect.height - 30)
        start_y = rail.y + 115
        for index, app_name in enumerate(("explorer", "game", "terminal", "settings")):
            item_rect = pygame.Rect(rail.centerx - 25, start_y + index * 80 - 25, 50, 50)
            if item_rect.collidepoint(mouse_pos):
                return self.launch_app(app_name)

        card_width = 145
        card_height = 130
        for index, app_name in enumerate(("browser", None)):
            if app_name is None:
                continue
            card_rect = pygame.Rect(panel_rect.x + 135 + index * (card_width + 30), panel_rect.y + 330, card_width, card_height)
            if card_rect.collidepoint(mouse_pos):
                return self.launch_app(app_name)

        app_radius = 28
        for index, app_name in enumerate(("browser", "camera")):
            app_rect = pygame.Rect(panel_rect.x + 622 - app_radius, panel_rect.y + 188 + index * 72 - app_radius, app_radius * 2, app_radius * 2)
            if app_rect.collidepoint(mouse_pos):
                return self.launch_app(app_name)

        for index, app_name in enumerate(("gallery", None)):
            if app_name is None:
                continue
            app_rect = pygame.Rect(panel_rect.x + 704 - app_radius, panel_rect.y + 120 + index * 72 - app_radius, app_radius * 2, app_radius * 2)
            if app_rect.collidepoint(mouse_pos):
                return self.launch_app(app_name)

        power_start_y = qa_panel_rect.bottom - 190
        for index, action in enumerate(("logout", "sleep", "restart", "shutdown")):
            power_rect = pygame.Rect(qa_panel_rect.centerx - 22, power_start_y + index * 50 - 22, 44, 44)
            if power_rect.collidepoint(mouse_pos):
                if self.app_launcher and hasattr(self.app_launcher, "power_action"):
                    return bool(self.app_launcher.power_action(action))
                return True

        clock_panel_x = 470 + 565
        clock_panel_y = panel_y + 580 - 260
        util_y = clock_panel_y + 240 - 35
        util_spacing = 48

        for i in range(3):
            cx = clock_panel_x + 40 + (i * util_spacing)
            distance = math.hypot(mouse_pos[0] - cx, mouse_pos[1] - util_y)

            if distance <= 16:
                if i == 0:
                    print("[Clock Widget] Alarm icon triggered!")
                elif i == 1:
                    print("[Clock Widget] Custom time increment triggered!")
                    self.custom_time_offset += 3600
                elif i == 2:
                    print("[Clock Widget] Toggle clock mode triggered!")
                    self.clock_is_digital = not self.clock_is_digital
                return True

        return True

    def draw_panel(self, panel_surface, rect, fill_color=(255, 255, 255, 45), outline_color=(255, 255, 255, 120), border_radius=28, shadow_alpha=35, outline_width=1):
        """Draw a rounded panel with a subtle shadow and a single-pixel highlight outline."""
        shadow_rect = rect.inflate(8, 8)
        shadow_rect.move_ip(0, 6)
        self.draw_smooth_rect(panel_surface, shadow_rect, (0, 0, 0, shadow_alpha), border_radius=border_radius)

        self.draw_smooth_rect(panel_surface, rect, fill_color, border_radius=border_radius)
        self.draw_smooth_rect(panel_surface, rect, outline_color, border_radius=border_radius, width=outline_width)

        pygame.draw.rect(
            panel_surface,
            (255, 255, 255, 25),
            rect.inflate(-2, -2),
            outline_width,
            border_radius=border_radius,
        )

    def draw(self, renderer):

        if self.animation <= 0:
            return

        surface = renderer.surface

        alpha = int(255 * self.animation)
        offset = int((1.0 - self.animation) * 40)
        mouse_pos = pygame.mouse.get_pos()

        screen_size = surface.get_size()
        temp_surface = pygame.Surface(screen_size, pygame.SRCALPHA)

        panel = pygame.Rect(470, 330 - offset, 760, 580)
        self.draw_panel(temp_surface, panel, border_radius=28)

        qa_panel = pygame.Rect(panel.right + 22, panel.y, 78, panel.height)
        self.draw_panel(temp_surface, qa_panel, fill_color=(22, 22, 24, 185), outline_color=(95, 95, 125, 120), border_radius=28)

        user_y = qa_panel.y + 45
        user_rect = pygame.Rect(qa_panel.centerx - 24, user_y - 24, 48, 48)
        user_bg = (85, 85, 90) if user_rect.collidepoint(mouse_pos) else (65, 65, 70)
        pygame.draw.circle(temp_surface, user_bg, (qa_panel.centerx, user_y), 24)

        if self.user_icon:
            temp_surface.blit(
                self.user_icon,
                (
                    qa_panel.centerx - self.user_icon.get_width() // 2,
                    user_y - self.user_icon.get_height() // 2,
                ),
            )

        start_y = qa_panel.bottom - 190
        spacing = 50

        for i, icon in enumerate(self.power_icons):
            cy = start_y + i * spacing
            icon_rect = pygame.Rect(qa_panel.centerx - 18, cy - 18, 36, 36)
            hover = icon_rect.collidepoint(mouse_pos)

            btn_bg = (85, 85, 90, 180) if hover else (65, 65, 70, 0)
            if hover:
                self.draw_alpha_circle(temp_surface, btn_bg, (qa_panel.centerx, cy), 20)

            if icon:
                self.draw_hover_icon(temp_surface, icon, (qa_panel.centerx, cy), 32, hover=hover)

        clock_panel = pygame.Rect(panel.x + 565, panel.y + panel.height - 260, 175, 240)
        self.draw_panel(temp_surface, clock_panel, border_radius=28)

        clock_center_x = clock_panel.centerx
        clock_center_y = clock_panel.y + 75
        clock_base_radius = 55

        if self.clock_ripple_radius > clock_base_radius:
            ripple_progress = (self.clock_ripple_radius - clock_base_radius) / 20.0
            ripple_alpha = max(0, int(150 * (1.0 - ripple_progress)))
            self.draw_alpha_circle(temp_surface, (255, 255, 255, ripple_alpha), (clock_center_x, clock_center_y), int(self.clock_ripple_radius))

        if self.clock_cover:

            cover_x = clock_center_x - self.clock_cover.get_width() // 2
            cover_y = clock_center_y - self.clock_cover.get_height() // 2
            temp_surface.blit(self.clock_cover, (cover_x, cover_y))
        else:

            pygame.draw.circle(temp_surface, (255, 255, 255, 45), (clock_center_x, clock_center_y), clock_base_radius, 1)

        now = datetime.datetime.now() + datetime.timedelta(seconds=self.custom_time_offset)

        if not self.clock_is_digital:

            seconds = now.second + now.microsecond / 1000000.0
            minutes = now.minute + seconds / 60.0
            hours = (now.hour % 12) + minutes / 60.0

            sec_angle = math.radians(seconds * 6 - 90)
            min_angle = math.radians(minutes * 6 - 90)
            hour_angle = math.radians(hours * 30 - 90)

            hx = clock_center_x + 28 * math.cos(hour_angle)
            hy = clock_center_y + 28 * math.sin(hour_angle)
            pygame.draw.line(temp_surface, (60, 60, 60), (clock_center_x, clock_center_y), (hx, hy), 3)

            mx = clock_center_x + 40 * math.cos(min_angle)
            my = clock_center_y + 40 * math.sin(min_angle)
            pygame.draw.line(temp_surface, (60, 60, 60), (clock_center_x, clock_center_y), (mx, my), 2)

            sx = clock_center_x + 46 * math.cos(sec_angle)
            sy = clock_center_y + 46 * math.sin(sec_angle)
            pygame.draw.line(temp_surface, (160, 160, 160), (clock_center_x, clock_center_y), (sx, sy), 1)

            pygame.draw.circle(temp_surface, (60, 60, 60), (clock_center_x, clock_center_y), 3)
        else:

            time_str = now.strftime("%H:%M")
            time_surf = self.time_font.render(time_str, True, (240, 240, 240))
            text_rect = time_surf.get_rect(center=(clock_center_x, clock_center_y))
            temp_surface.blit(time_surf, text_rect)

        base_icon_size = 36
        bg_radius = 24

        if self.wifi_icon:
            wifi_center = (panel.right - 42, panel.y + 42)
            wifi_rect = pygame.Rect(wifi_center[0] - 18, wifi_center[1] - 18, 36, 36)
            wifi_hover = wifi_rect.collidepoint(mouse_pos)

            if wifi_hover:
                self.draw_alpha_circle(temp_surface, (255, 255, 255, 45), wifi_center, bg_radius)

            self.draw_hover_icon(temp_surface, self.wifi_icon, wifi_center, base_icon_size, hover=wifi_hover)

        if self.notification_icon:
            notif_center = (panel.right - 92, panel.y + 42)
            notif_rect = pygame.Rect(notif_center[0] - 18, notif_center[1] - 18, 36, 36)
            notif_hover = notif_rect.collidepoint(mouse_pos)

            if notif_hover:
                self.draw_alpha_circle(temp_surface, (255, 255, 255, 45), notif_center, bg_radius)

            self.draw_hover_icon(temp_surface, self.notification_icon, notif_center, base_icon_size, hover=notif_hover)

        rail = pygame.Rect(panel.x + 18, panel.y + 15, 70, panel.height - 30)
        self.draw_panel(temp_surface, rail, fill_color=(22, 22, 24, 185), outline_color=(95, 95, 105, 120), border_radius=28)

        start_y = rail.y + 115
        spacing = 80
        for i, icon in enumerate(self.sidebar_icons):
            cy = start_y + i * spacing
            item_rect = pygame.Rect(rail.centerx - 25, cy - 25, 50, 50)
            bg_color = (85, 85, 90) if item_rect.collidepoint(mouse_pos) else (65, 65, 70)

            pygame.draw.circle(temp_surface, bg_color, (rail.centerx, cy), 25)
            if icon is not None:
                self.draw_hover_icon(temp_surface, icon, (rail.centerx, cy), 36, hover=item_rect.collidepoint(mouse_pos))

        plus_y = rail.bottom - 45
        plus_rect = pygame.Rect(rail.centerx - 25, plus_y - 25, 50, 50)

        if plus_rect.collidepoint(mouse_pos):
            plus_bg = (85, 85, 90)
            target_plus_size = 42
        else:
            plus_bg = (65, 65, 70)
            target_plus_size = 36

        pygame.draw.circle(temp_surface, plus_bg, (rail.centerx, plus_y), 25)
        if self.plus_icon_base is not None:
            scaled_plus = pygame.transform.smoothscale(self.plus_icon_base, (target_plus_size, target_plus_size))
            temp_surface.blit(
                scaled_plus,
                (
                    rail.centerx - scaled_plus.get_width() // 2,
                    plus_y - scaled_plus.get_height() // 2
                )
            )

        breathe_factor = 1.0 + 0.02 * math.sin(self.breathing_time * 2.5)

        card_base_w = 351
        card_base_h = 160
        card_base_center_x = panel.x + 125 + (card_base_w // 2)
        card_base_center_y = panel.y + 92 + (card_base_h // 2)

        card_w = int(card_base_w * breathe_factor)
        card_h = int(card_base_h * breathe_factor)
        card_x = card_base_center_x - (card_w // 2)
        card_y = card_base_center_y - (card_h // 2)

        card = pygame.Rect(card_x, card_y, card_w, card_h)
        self.draw_panel(temp_surface, card, fill_color=(255, 255, 255, 65), outline_color=(255, 255, 255, 100), border_radius=28)

        greeting_surf = self.small_font.render("Good Morning", True, (0, 0, 0))
        temp_surface.blit(greeting_surf, (card.x + 18, card.y + 22))

        user_name_surf = self.large_font.render("User_name", True, (0, 0, 0))
        temp_surface.blit(user_name_surf, (card.x + 18, card.y + 55))

        if self.snake:
            snake_base_w = self.snake.get_width()
            snake_base_h = self.snake.get_height()

            scaled_snake_w = int(snake_base_w * breathe_factor)
            scaled_snake_h = int(snake_base_h * breathe_factor)
            snake_scaled = pygame.transform.smoothscale(self.snake, (scaled_snake_w, scaled_snake_h))

            offset_x = (scaled_snake_w - snake_base_w) // 2
            offset_y = (scaled_snake_h - snake_base_h) // 2

            snake_to_draw = snake_scaled.copy()
            snake_to_draw.set_alpha(185)
            temp_surface.blit(
                snake_to_draw,
                (
                    card.right - 299 - offset_x,
                    card.y - 113 - offset_y,
                ),
            )

        top_search = pygame.Rect(panel.x + 180, panel.y + 18, 300, 48)
        self.draw_panel(temp_surface, top_search, fill_color=(255, 255, 255, 55), outline_color=(255, 255, 255, 90), border_radius=28)

        if self.search_icon:
            icon_w = self.search_icon.get_width()
            start_top_x = top_search.x + 14
            end_top_x = top_search.centerx - (icon_w // 2)

            top_icon_x = start_top_x + (end_top_x - start_top_x) * self.search_hover_anim
            temp_surface.blit(self.search_icon, (top_icon_x, top_search.y + 12))

            text_alpha = int(180 * (1.0 - self.search_hover_anim))
            if text_alpha > 5:
                placeholder_surf = self.search_font.render("Search...", True, (240, 240, 240))
                placeholder_surf.set_alpha(text_alpha)
                temp_surface.blit(placeholder_surf, (top_search.x + 50, top_search.y + 13))

        recent_label_surf = self.small_font.render("Recent tabs", True, (240, 240, 240))
        temp_surface.blit(recent_label_surf, (panel.x + 135, panel.y + 280))

        card_width = 145
        card_height = 130
        start_x = panel.x + 135
        start_y = panel.y + 330
        spacing = 30

        recent_names = ["Browser", "+"]

        for i in range(2):
            x = start_x + i * (card_width + spacing)
            card_rect = pygame.Rect(x, start_y, card_width, card_height)
            is_hovered = card_rect.collidepoint(mouse_pos)

            if self.recent_icons[i] is not None:
                bg_alpha = 55 if is_hovered else 25
                self.draw_panel(temp_surface, card_rect, fill_color=(255, 255, 255, bg_alpha), border_radius=28)
                text_color = (20, 20, 20)
            else:
                bg_alpha = 55 if is_hovered else 35
                self.draw_panel(temp_surface, card_rect, fill_color=(255, 255, 255, bg_alpha), outline_color=(255, 255, 255, 80), border_radius=28)
                text_color = (240, 240, 240)

            icon = self.recent_icons[i]
            if icon is not None:
                temp_surface.blit(
                    icon,
                    (
                        card_rect.centerx - icon.get_width() // 2,
                        card_rect.y + 15,
                    ),
                )

            name_surf = self.card_font.render(recent_names[i], True, text_color)
            temp_surface.blit(
                name_surf,
                (
                    card_rect.centerx - name_surf.get_width() // 2,
                    card_rect.bottom - 28
                )
            )

        lbl_my_surf = self.apps_label_font.render("My", True, (240, 240, 240))
        temp_surface.blit(lbl_my_surf, (panel.x + 592, panel.y + 90))

        lbl_apps_surf = self.apps_label_font.render("Apps", True, (240, 240, 240))
        temp_surface.blit(lbl_apps_surf, (panel.x + 592, panel.y + 118))

        app_base_size = 42
        app_radius = 28

        under_x = panel.x + 622
        under_start_y = panel.y + 188
        under_spacing = 72

        for i, icon in enumerate(self.my_apps_under):
            cy = under_start_y + i * under_spacing
            app_rect = pygame.Rect(under_x - app_radius, cy - app_radius, app_radius * 2, app_radius * 2)
            hover = app_rect.collidepoint(mouse_pos)

            bg_alpha = 90 if hover else 45
            self.draw_alpha_circle(temp_surface, (255, 255, 255, bg_alpha), (under_x, cy), app_radius)

            if icon:
                self.draw_hover_icon(temp_surface, icon, (under_x, cy), app_base_size, hover=hover)

        side_x = panel.x + 704
        side_start_y = panel.y + 120
        side_spacing = 72

        for i, icon in enumerate(self.my_apps_side):
            cy = side_start_y + i * side_spacing
            app_rect = pygame.Rect(side_x - app_radius, cy - app_radius, app_radius * 2, app_radius * 2)
            hover = app_rect.collidepoint(mouse_pos)

            bg_alpha = 70 if hover else 45
            self.draw_alpha_circle(temp_surface, (255, 255, 255, bg_alpha), (side_x, cy), app_radius)

            if icon:
                self.draw_hover_icon(temp_surface, icon, (side_x, cy), app_base_size, hover=hover)

        plus_app_y = side_start_y + 2 * side_spacing
        plus_app_rect = pygame.Rect(side_x - app_radius, plus_app_y - app_radius, app_radius * 2, app_radius * 2)
        plus_app_hover = plus_app_rect.collidepoint(mouse_pos)

        if plus_app_hover:
            self.draw_alpha_circle(temp_surface, (255, 255, 255, 75), (side_x, plus_app_y), app_radius)
            target_app_plus_size = 48
        else:
            self.draw_alpha_circle(temp_surface, (255, 255, 255, 45), (side_x, plus_app_y), app_radius)
            target_app_plus_size = 42

        if self.plus_icon_base:
            scaled_app_plus = pygame.transform.smoothscale(self.plus_icon_base, (target_app_plus_size, target_app_plus_size))
            temp_surface.blit(
                scaled_app_plus,
                (
                    side_x - scaled_app_plus.get_width() // 2,
                    plus_app_y - scaled_app_plus.get_height() // 2,
                ),
            )

        lbl_section_surf = self.small_font.render("Section", True, (240, 240, 240))
        temp_surface.blit(lbl_section_surf, (panel.x + 135, panel.y + 480))

        bottom_search = pygame.Rect(panel.x + 135, panel.y + 515, 310, 45)
        self.draw_panel(temp_surface, bottom_search, fill_color=(255, 255, 255, 55), outline_color=(255, 255, 255, 90), border_radius=28)

        if self.search_icon:
            icon_w = self.search_icon.get_width()
            start_bottom_x = bottom_search.x + 14
            end_bottom_x = bottom_search.centerx - (icon_w // 2)

            bottom_icon_x = start_bottom_x + (end_bottom_x - start_bottom_x) * self.bottom_search_hover_anim
            temp_surface.blit(self.search_icon, (bottom_icon_x, bottom_search.y + 10))

            bottom_text_alpha = int(180 * (1.0 - self.bottom_search_hover_anim))
            if bottom_text_alpha > 5:
                bottom_placeholder_surf = self.search_font.render("Search Section...", True, (240, 240, 240))
                bottom_placeholder_surf.set_alpha(bottom_text_alpha)
                temp_surface.blit(bottom_placeholder_surf, (bottom_search.x + 50, bottom_search.y + 12))

        temp_surface.set_alpha(alpha)
        surface.blit(temp_surface, (0, 0))









