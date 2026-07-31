# apps/explorer/explorer_render.py
"""Rendering methods for Explorer - All drawing logic separated"""

import pygame

class ExplorerRender:
    """Mixin class for rendering the explorer window"""
    
    def draw(self, renderer):
        """Main draw method"""
        if self.minimized or self.closed:
            return

        super().draw(renderer)

        try:
            surface = renderer.surface
            wx, wy = self.transform.position.x, self.transform.position.y
            ww, wh = self.transform.size.width, self.transform.size.height

            mx, my = pygame.mouse.get_pos()
            rel_x, rel_y = mx - wx, my - wy

            scale = max(0.65, min(ww / 920.0, wh / 620.0))

            # Fonts
            font_main = pygame.font.SysFont("Segoe UI", max(11, int(15 * scale)))
            font_small = pygame.font.SysFont("Segoe UI", max(9, int(12 * scale)))
            font_greeting = pygame.font.SysFont("Segoe UI", max(18, int(24 * scale)), bold=True)
            font_tooltip = pygame.font.SysFont("Segoe UI", max(9, int(11 * scale)))

            # Main window surface
            window_surf = pygame.Surface((ww, wh), pygame.SRCALPHA)

            # 1. Base Window Layer
            pygame.draw.rect(window_surf, (22, 22, 24, 120), (0, 0, ww, wh), border_radius=18)

            # 2. Solid Top Bar
            pygame.draw.rect(window_surf, (5, 5, 5, 245), (0, 0, ww, self.TITLEBAR_HEIGHT), 
                           border_top_left_radius=16, border_top_right_radius=16)

            # 3. Top Navigation Buttons
            self._draw_navigation_buttons(window_surf, scale)

            # Panel Layout
            left_w = max(145, int(ww * 0.185))
            center_w = max(48, int(ww * 0.065))
            bottom_margin = int(20 * scale)
            right_margin = int(24 * scale)

            left_panel_rect = pygame.Rect(16, self.TITLEBAR_HEIGHT + 10, left_w, 
                                        wh - self.TITLEBAR_HEIGHT - bottom_margin - 10)
            center_strip_rect = pygame.Rect(left_panel_rect.right + 10, self.TITLEBAR_HEIGHT + 10, 
                                          center_w, wh - self.TITLEBAR_HEIGHT - bottom_margin - 10)

            content_x = center_strip_rect.right + 24
            content_w = max(180, ww - content_x - right_margin)
            content_h = max(180, wh - self.TITLEBAR_HEIGHT - bottom_margin - 10)

            # Draw panels
            self._draw_left_panel(window_surf, left_panel_rect, rel_x, rel_y, font_main, scale)
            self._draw_center_strip(window_surf, center_strip_rect, rel_x, rel_y, scale)
            self._draw_right_content(window_surf, content_x, content_w, content_h, rel_x, rel_y, 
                                   font_small, font_greeting, font_tooltip, scale)

            surface.blit(window_surf, (wx, wy))
            
        except Exception as e:
            print(f"[VOS] ERROR in draw loop: {e}")
            import traceback
            traceback.print_exc()

    def _draw_navigation_buttons(self, surface, scale):
        """Draw back, forward, and up buttons in titlebar"""
        nav_x = int(18 * scale)
        top_icon_sz = max(12, int(16 * scale))
        nav_y = (self.TITLEBAR_HEIGHT - top_icon_sz) // 2
        
        for key in ["back", "forward", "down"]:
            icon = self._get_scaled_icon(key, top_icon_sz)
            if icon:
                surface.blit(icon, (nav_x, nav_y))
            nav_x += int(24 * scale)
            
    def _get_scaled_icon(self, key: str, target_size: int) -> pygame.Surface | None:
        """Get scaled icon with fallback loading"""
        raw = self.raw_icons.get(key)
        if raw and target_size > 4:
            try:
                # If it's already a surface
                if hasattr(raw, 'get_width'):
                    return pygame.transform.smoothscale(raw, (target_size, target_size))
                # If it's a path string
                elif isinstance(raw, str):
                    try:
                        img = pygame.image.load(raw)
                        if img:
                            return pygame.transform.smoothscale(img, (target_size, target_size))
                    except:
                        pass
            except Exception as e:
                print(f"[VOS] Error scaling icon '{key}': {e}")
        
        # Try to load directly from assets if not found
        try:
            import os
            # Try to find the icon file
            icon_paths = [
                f"assets/icons/explorer/{key}.png",
                f"assets/icons/explorer/{key}.svg",
                f"assets/icons/explorer/{key}.jpg",
            ]
            for path in icon_paths:
                if os.path.exists(path):
                    img = pygame.image.load(path)
                    if img:
                        return pygame.transform.smoothscale(img, (target_size, target_size))
        except:
            pass
        
        return None
    # In apps/explorer/explorer_render.py - Update _draw_left_panel method

    def _draw_left_panel(self, surface, rect, rel_x, rel_y, font_main, scale):
        """Draw the sidebar panel with proper folder icons"""
        # Panel background with glass effect
        pygame.draw.rect(surface, (250, 250, 250, 180), rect, border_radius=18)
        pygame.draw.rect(surface, (255, 255, 255, 30), rect, border_radius=18, width=1)

        y = rect.y + int(10 * scale)
        item_h = max(24, int(rect.height * 0.054))
        icon_sz = max(14, int(18 * scale))

        # Group items with proper icons
        for name, icon_path in self.sidebar_items:
            item_rect = pygame.Rect(rect.x + 6, y, rect.width - 12, item_h)
            is_selected = (name == self.selected_sidebar)
            is_hovered = item_rect.collidepoint(rel_x, rel_y) and not is_selected

            # Background
            if is_selected:
                pygame.draw.rect(surface, (45, 45, 48, 255), item_rect, border_radius=10)
                pygame.draw.rect(surface, (120, 180, 255), 
                            (item_rect.x + 2, item_rect.y + 4, 3, item_h - 8), border_radius=2)
                text_color = (255, 255, 255)
            elif is_hovered:
                pygame.draw.rect(surface, (0, 0, 0, 60), item_rect, border_radius=10)
                text_color = (255, 255, 255)
            else:
                text_color = (65, 65, 70)

            # Get proper icon - use folder icon for all navigation items
            if name == "Computer":
                icon = self._get_scaled_icon("computer", icon_sz)
            elif name == "Documents":
                icon = self._get_scaled_icon("documents_folder", icon_sz)
            elif name == "Pictures":
                icon = self._get_scaled_icon("images_folder", icon_sz)
            elif name == "Videos":
                icon = self._get_scaled_icon("videos_folder", icon_sz)
            elif name == "Music":
                icon = self._get_scaled_icon("musics_folder", icon_sz)
            elif name == "Downloads":
                icon = self._get_scaled_icon("downloads_folder", icon_sz)
            elif name == "Storage":
                icon = self._get_scaled_icon("storages", icon_sz)
            elif name == "Trash":
                icon = self._get_scaled_icon("trashs", icon_sz)
            else:
                icon = self._get_scaled_icon("folder", icon_sz)
            
            # Fallback to folder icon if specific icon not found
            if not icon:
                icon = self._get_scaled_icon("folder", icon_sz)
            
            if icon:
                surface.blit(icon, (item_rect.x + 8, item_rect.centery - icon.get_height() // 2))

            # Text
            txt = font_main.render(name, True, text_color)
            surface.blit(txt, (item_rect.x + int(32 * scale), item_rect.centery - txt.get_height() // 2))

            y += item_h + int(2 * scale)

    def _draw_center_strip(self, surface, rect, rel_x, rel_y, scale):
        """Draw the quick-access center strip"""
        pygame.draw.rect(surface, (250, 250, 250, 180), rect, border_radius=20)

        center_items = ["center_1", "center_2", "center_3", "center_4", "center_5", "center_6"]
        icon_sz = max(18, int(24 * scale))
        ring_size = int(36 * scale)

        y = rect.y + int(10 * scale)
        spacing_y = int(40 * scale)

        for key in center_items:
            base_ring_rect = pygame.Rect(rect.centerx - ring_size // 2, y, ring_size, ring_size)
            is_hovered = base_ring_rect.collidepoint(rel_x, rel_y)

            current_ring_size = int(ring_size * 1.15) if is_hovered else ring_size
            ring_rect = pygame.Rect(rect.centerx - current_ring_size // 2, 
                                   y - (current_ring_size - ring_size)//2, 
                                   current_ring_size, current_ring_size)

            ring_bg = (255, 255, 255, 100) if is_hovered else (255, 255, 255, 35)
            ring_border = (255, 255, 255, 190) if is_hovered else (255, 255, 255, 70)

            circle_radius = current_ring_size // 2
            pygame.draw.rect(surface, ring_bg, ring_rect, border_radius=circle_radius)
            pygame.draw.rect(surface, ring_border, ring_rect, width=1, border_radius=circle_radius)

            curr_icon_sz = int(icon_sz * 1.1) if is_hovered else icon_sz
            img = self._get_scaled_icon(key, curr_icon_sz)
            if img:
                surface.blit(img, (ring_rect.centerx - (img.get_width() // 2), 
                                  ring_rect.centery - (img.get_height() // 2)))

            y += spacing_y

        # Plus button at bottom
        self._draw_plus_button(surface, rect, rel_x, rel_y, scale)

    def _draw_plus_button(self, surface, rect, rel_x, rel_y, scale):
        """Draw the plus button at bottom of center strip"""
        plus_sz = max(14, int(18 * scale))
        plus_ring_sz = int(34 * scale)
        plus_y = rect.bottom - int(38 * scale)
        
        plus_base_rect = pygame.Rect(rect.centerx - plus_ring_sz // 2, 
                                    plus_y - plus_ring_sz // 2, 
                                    plus_ring_sz, plus_ring_sz)
        
        is_plus_hovered = plus_base_rect.collidepoint(rel_x, rel_y)
        curr_plus_ring_sz = int(plus_ring_sz * 1.15) if is_plus_hovered else plus_ring_sz
        
        plus_ring_rect = pygame.Rect(rect.centerx - curr_plus_ring_sz // 2, 
                                    plus_y - curr_plus_ring_sz // 2, 
                                    curr_plus_ring_sz, curr_plus_ring_sz)

        plus_bg = (255, 255, 255, 100) if is_plus_hovered else (255, 255, 255, 35)
        plus_border = (255, 255, 255, 190) if is_plus_hovered else (255, 255, 255, 70)

        plus_radius = curr_plus_ring_sz // 2
        pygame.draw.rect(surface, plus_bg, plus_ring_rect, border_radius=plus_radius)
        pygame.draw.rect(surface, plus_border, plus_ring_rect, width=1, border_radius=plus_radius)

        curr_plus_sz = int(plus_sz * 1.1) if is_plus_hovered else plus_sz
        plus_img = self._get_scaled_icon("plus", curr_plus_sz)
        if plus_img:
            surface.blit(plus_img, (plus_ring_rect.centerx - (plus_img.get_width() // 2), 
                                   plus_ring_rect.centery - (plus_img.get_height() // 2)))

    def _draw_right_content(self, surface, content_x, content_w, content_h, rel_x, rel_y, 
                           font_small, font_greeting, font_tooltip, scale):
        """Draw the main content area"""
        top_y = self.TITLEBAR_HEIGHT + 10

        # Search bar and status icons
        self._draw_search_bar(surface, content_x, top_y, content_w, rel_x, rel_y, font_small, scale)
        self._draw_status_icons(surface, content_x, top_y, content_w, scale)

        # Content area
        grid_start_y = top_y + self._get_search_bar_height(scale) + int(16 * scale)
        
        if self.current_folder is None:
            self._draw_dashboard(surface, content_x, grid_start_y, content_w, content_h, 
                               rel_x, rel_y, font_greeting, font_small, font_tooltip, scale)
        else:
            self._draw_folder_contents(surface, content_x, grid_start_y, content_w, content_h, 
                                     rel_x, rel_y, font_greeting, font_small, font_tooltip, scale)

    def _get_search_bar_height(self, scale):
        """Calculate search bar height"""
        return max(28, int(36 * scale))

    def _draw_search_bar(self, surface, content_x, top_y, content_w, rel_x, rel_y, font_small, scale):
        """Draw the search bar with animation"""
        base_search_w = min(int(260 * scale), int(content_w * 0.60))
        base_search_h = max(28, int(36 * scale))
        
        search_w = int(base_search_w + (45 * scale * self.search_progress))
        search_h = int(base_search_h + (6 * scale * self.search_progress))
        search_y = top_y - int(3 * scale * self.search_progress)
        search_rect = pygame.Rect(content_x, search_y, search_w, search_h)

        search_alpha = int(70 + 30 * self.search_progress)
        search_bg = (230, 230, 230, search_alpha)

        pygame.draw.rect(surface, search_bg, search_rect, border_radius=search_h // 2)

        # Search icon
        base_icon_sz = max(12, int(16 * scale))
        search_icon_sz = int(base_icon_sz + (base_icon_sz * 0.25) * self.search_progress)
        s_icon = self._get_scaled_icon("search", search_icon_sz)
        if s_icon:
            start_icon_x = search_rect.x + int(14 * scale)
            target_icon_x = search_rect.centerx - (s_icon.get_width() // 2)
            s_icon_x = int(start_icon_x + (target_icon_x - start_icon_x) * self.search_progress)
            s_icon_y = search_rect.centery - (s_icon.get_height() // 2)
            surface.blit(s_icon, (s_icon_x, s_icon_y))

        # Search placeholder text
        text_alpha = int(240 * (1.0 - self.search_progress))
        if text_alpha > 5:
            txt = font_small.render("Search...", True, (240, 240, 240))
            if text_alpha < 240:
                faded_txt = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
                faded_txt.blit(txt, (0, 0))
                faded_txt.set_alpha(text_alpha)
                txt = faded_txt
            txt_x = search_rect.x + int(38 * scale)
            txt_y = search_rect.centery - txt.get_height() // 2
            surface.blit(txt, (txt_x, txt_y))

    def _draw_status_icons(self, surface, content_x, top_y, content_w, scale):
        """Draw status icons (bell, wifi, user)"""
        status_icon_sz = max(14, int(18 * scale))
        tr_x = content_x + content_w - (3 * int(26 * scale))
        
        for key in ["bell", "wifi", "user"]:
            icon = self._get_scaled_icon(key, status_icon_sz)
            if icon:
                surface.blit(icon, (tr_x, top_y + (self._get_search_bar_height(scale) // 2) - (status_icon_sz // 2)))
            tr_x += int(26 * scale)

    def _draw_dashboard(self, surface, content_x, grid_start_y, content_w, content_h, 
                       rel_x, rel_y, font_greeting, font_small, font_tooltip, scale):
        """Draw the dashboard view when at root"""
        grid_w = content_w
        grid_h = (self.TITLEBAR_HEIGHT + 10 + content_h) - grid_start_y

        spacing = int(20 * scale)
        col_w = (grid_w - spacing) / 2
        row_h = (grid_h - (2 * spacing)) / 3

        # Greeting
        cell_00_rect = pygame.Rect(content_x, grid_start_y, col_w, row_h)
        greeting = font_greeting.render(f"Hi, {self.user_name}", True, (245, 245, 245))
        surface.blit(greeting, (cell_00_rect.x, cell_00_rect.y + int(4 * scale)))

        # AI Assistant button
        ai_w = min(int(110 * scale), int(col_w * 0.8))
        ai_h = max(26, int(34 * scale))
        ai_box_rect = pygame.Rect(cell_00_rect.x, cell_00_rect.y + greeting.get_height() + int(12 * scale), ai_w, ai_h)
        
        pygame.draw.rect(surface, (255, 255, 255, 30), ai_box_rect, border_radius=10)
        ai_icon_sz = max(14, int(18 * scale))
        ai_icon = self._get_scaled_icon("chatgpt", ai_icon_sz)
        if ai_icon:
            surface.blit(ai_icon, (ai_box_rect.x + 10, ai_box_rect.centery - (ai_icon_sz // 2)))

        # Cards
        cards = [
            pygame.Rect(content_x + col_w + spacing, grid_start_y, col_w, row_h),
            pygame.Rect(content_x, grid_start_y + row_h + spacing, col_w, row_h),
            pygame.Rect(content_x + col_w + spacing, grid_start_y + row_h + spacing, col_w, row_h),
            pygame.Rect(content_x, grid_start_y + (row_h + spacing) * 2, col_w, row_h),
            pygame.Rect(content_x + col_w + spacing, grid_start_y + (row_h + spacing) * 2, col_w, row_h)
        ]

        for i, card_rect in enumerate(cards):
            is_hovered = card_rect.collidepoint(rel_x, rel_y)

            render_rect = card_rect
            if is_hovered:
                render_rect = card_rect.inflate(int(4 * scale), int(4 * scale))

            card_bg = (0, 0, 0, 180) if is_hovered else (220, 220, 220, 60)
            pygame.draw.rect(surface, card_bg, render_rect, border_radius=16)

            plus_sz = max(14, int(min(render_rect.width, render_rect.height) * 0.35))
            plus_icon = self._get_scaled_icon("plus", plus_sz)
            if plus_icon:
                if is_hovered:
                    plus_icon = plus_icon.copy()
                    plus_icon.set_alpha(255)

                px = render_rect.centerx - (plus_sz // 2)
                py = render_rect.centery - (plus_sz // 2)
                surface.blit(plus_icon, (px, py))

            if is_hovered:
                tip_surf = font_tooltip.render(f"Add Widget {i+1}", True, (255, 255, 255))
                tip_bg = pygame.Rect(render_rect.centerx - tip_surf.get_width()//2 - 6, 
                                    render_rect.bottom - int(24 * scale), 
                                    tip_surf.get_width() + 12, int(18 * scale))

    def _draw_folder_contents(self, surface, content_x, grid_start_y, content_w, content_h, 
                             rel_x, rel_y, font_greeting, font_small, font_tooltip, scale):
        """Draw folder contents in grid view"""
        if self.current_folder is None:
            return
        
        # Get folder items
        items = self._get_folder_items(self.current_folder)
        self.item_rects = []  # Clear previous rects
        
        if not items:
            # Show empty folder message
            txt = font_small.render("This folder is empty", True, (150, 150, 150))
            surface.blit(txt, (content_x + 20, grid_start_y + 20))
            return
        
        # Display items in grid
        icon_size = max(48, int(60 * scale))
        padding = int(10 * scale)
        items_per_row = max(1, int((content_w - padding) / (icon_size + padding)))
        
        x = content_x
        y = grid_start_y
        col = 0
        
        # Breadcrumb path
        self._draw_breadcrumb(surface, content_x, grid_start_y - int(20 * scale), scale, font_small)
        
        # Adjust grid start after breadcrumb
        grid_y = grid_start_y + int(10 * scale)
        
        for item in items:
            item_name = getattr(item, 'name', 'Unknown')
            is_folder = self._is_item_folder(item)
            
            # Calculate position
            item_rect = pygame.Rect(x, grid_y, icon_size, icon_size + 30)
            self.item_rects.append((item_rect, item))
            
            # Draw icon
            if is_folder:
                icon = self._get_scaled_icon("folder", icon_size)
            else:
                # Try to get file icon based on extension
                icon = self._get_file_icon(item_name, icon_size)
            
            if icon:
                surface.blit(icon, (x + (icon_size - icon.get_width())//2, grid_y))
            
            # Draw name
            display_name = item_name[:15] + "..." if len(item_name) > 15 else item_name
            txt = font_small.render(display_name, True, (200, 200, 200))
            surface.blit(txt, (x + (icon_size - txt.get_width())//2, grid_y + icon_size + 4))
            
            # Highlight selected item
            if self.selected_item == item:
                pygame.draw.rect(surface, (120, 180, 255, 50), item_rect, border_radius=8, width=2)
            
            # Move to next position
            col += 1
            if col >= items_per_row:
                col = 0
                x = content_x
                grid_y += icon_size + 40
            else:
                x += icon_size + padding

    def _draw_breadcrumb(self, surface, content_x, y, scale, font_small):
        """Draw breadcrumb navigation path"""
        if self.current_folder is None:
            return
        
        path = self.get_breadcrumb_path()
        x = content_x
        
        for i, name in enumerate(path):
            # Draw folder name
            txt = font_small.render(name, True, (180, 180, 190))
            surface.blit(txt, (x, y))
            x += txt.get_width() + 4
            
            # Draw separator arrow
            if i < len(path) - 1:
                arrow = font_small.render("›", True, (100, 100, 110))
                surface.blit(arrow, (x, y))
                x += arrow.get_width() + 4

    def _get_file_icon(self, filename, target_size):
        """Get appropriate icon for file type"""
        ext = filename.split('.')[-1].lower() if '.' in filename else ''
        
        # Map extensions to icon keys
        icon_map = {
            'py': 'python',
            'txt': 'text',
            'md': 'text',
            'json': 'json',
            'html': 'html',
            'css': 'css',
            'js': 'javascript',
            'jpg': 'image',
            'jpeg': 'image',
            'png': 'image',
            'gif': 'image',
            'mp3': 'music',
            'wav': 'music',
            'mp4': 'video',
            'avi': 'video',
            'pdf': 'pdf',
            'xls': 'spreadsheet',
            'xlsx': 'spreadsheet',
            'zip': 'zip',
            'csv': 'spreadsheet',
        }
        
        icon_key = icon_map.get(ext, 'document')
        
        # Try to get file icon, fallback to document
        icon = self._get_scaled_icon(icon_key, target_size)
        if not icon:
            icon = self._get_scaled_icon('document', target_size)
        return icon

    def _draw_context_menu(self, surface, x, y, items, scale):
        """Draw a context menu (placeholder for future implementation)"""
        # This is a placeholder - will be implemented when context menu is needed
        pass