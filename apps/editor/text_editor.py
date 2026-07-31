# apps/editor/text_editor.py
import pygame
from desktop.ui.window.window import Window
from desktop.assests.icon_manager import IconManager

class TextEditorApp(Window):
    """Text Editor with VOS integration and better UI"""
    
    def __init__(self, filename="Untitled", content="", file_path=""):
        super().__init__(f"{filename} - Text Editor", 800, 600, "TextEditor")
        
        self.filename = filename
        self.file_path = file_path
        self.content = content
        self.cursor_pos = len(content)
        self.scroll_offset = 0
        self.modified = False
        self.cursor_visible = True
        self.cursor_timer = 0
        
        # Editor settings
        self.font_size = 14
        self.font = pygame.font.SysFont("Consolas", self.font_size)
        self.font_height = self.font.get_linesize()
        
        # Colors - Dark theme matching your design
        self.bg_color = (28, 28, 30)
        self.text_color = (220, 220, 220)
        self.cursor_color = (255, 255, 255)
        self.line_numbers_color = (80, 80, 85)
        self.line_number_bg = (35, 35, 38)
        self.status_color = (40, 40, 42)
        self.accent_color = (120, 180, 255)
        self.modified_color = (255, 200, 50)
        
        # Editor state
        self.undo_stack = []
        self.redo_stack = []
        self.selection_start = None
        self.selection_end = None
        self.word_wrap = False
        self.show_line_numbers = True
        
        # Create menus
        self.menus = {
            "File": ["New", "Open", "Save", "Save As", "---", "Exit"],
            "Edit": ["Undo", "Redo", "---", "Cut", "Copy", "Paste", "Delete", "---", "Select All"],
            "View": ["Word Wrap", "Line Numbers", "Font Size"]
        }
        
        # Make sure it's positioned properly
        self.transform.position.x = 200
        self.transform.position.y = 100
        
        # Ensure it's active
        self.is_active = True
        
        print(f"[VOS] Text Editor initialized: {filename}")
        
        print(f"[VOS] Text Editor opened: {filename}")
    
    def handle_event(self, event):
        if not self.is_active:
            return
        
        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
        
        super().handle_event(event)
    
    def _handle_keydown(self, event):
        """Handle keyboard input"""
        mods = pygame.key.get_mods()
        ctrl = mods & pygame.KMOD_CTRL
        shift = mods & pygame.KMOD_SHIFT
        
        # Ctrl+S - Save
        if event.key == pygame.K_s and ctrl:
            self.save_file()
            return
        
        # Ctrl+O - Open
        if event.key == pygame.K_o and ctrl:
            self.open_file()
            return
        
        # Ctrl+N - New
        if event.key == pygame.K_n and ctrl:
            self.new_file()
            return
        
        # Ctrl+Z - Undo
        if event.key == pygame.K_z and ctrl:
            self.undo()
            return
        
        # Ctrl+Y - Redo
        if event.key == pygame.K_y and ctrl:
            self.redo()
            return
        
        # Escape - Close
        if event.key == pygame.K_ESCAPE:
            self.close()
            return
        
        # Delete/Backspace
        if event.key == pygame.K_BACKSPACE:
            self._backspace()
            return
        
        if event.key == pygame.K_DELETE:
            self._delete()
            return
        
        # Enter
        if event.key == pygame.K_RETURN:
            self._insert_text("\n")
            return
        
        # Tab
        if event.key == pygame.K_TAB:
            if shift:
                self._unindent()
            else:
                self._insert_text("    ")
            return
        
        # Arrow keys
        if event.key == pygame.K_LEFT:
            self._move_cursor(-1, shift)
            return
        if event.key == pygame.K_RIGHT:
            self._move_cursor(1, shift)
            return
        if event.key == pygame.K_UP:
            self._move_cursor_up(shift)
            return
        if event.key == pygame.K_DOWN:
            self._move_cursor_down(shift)
            return
        
        # Home/End
        if event.key == pygame.K_HOME:
            self._move_to_line_start(shift)
            return
        if event.key == pygame.K_END:
            self._move_to_line_end(shift)
            return
        
        # Regular character input
        if event.unicode and event.unicode.isprintable():
            self._insert_text(event.unicode)
    
    def _backspace(self):
        """Handle backspace"""
        if self.selection_start is not None:
            self._delete_selection()
            return
        
        if self.cursor_pos > 0:
            self._save_undo()
            self.content = self.content[:self.cursor_pos-1] + self.content[self.cursor_pos:]
            self.cursor_pos -= 1
            self.modified = True
    
    def _delete(self):
        """Handle delete"""
        if self.selection_start is not None:
            self._delete_selection()
            return
        
        if self.cursor_pos < len(self.content):
            self._save_undo()
            self.content = self.content[:self.cursor_pos] + self.content[self.cursor_pos+1:]
            self.modified = True
    
    def _insert_text(self, text):
        """Insert text at cursor position"""
        if self.selection_start is not None:
            self._delete_selection()
        
        self._save_undo()
        self.content = self.content[:self.cursor_pos] + text + self.content[self.cursor_pos:]
        self.cursor_pos += len(text)
        self.modified = True
        self.selection_start = None
        self.selection_end = None
    
    def _move_cursor(self, delta, shift=False):
        """Move cursor left/right"""
        new_pos = max(0, min(self.cursor_pos + delta, len(self.content)))
        
        if shift:
            if self.selection_start is None:
                self.selection_start = self.cursor_pos
            self.cursor_pos = new_pos
            self.selection_end = self.cursor_pos
        else:
            self.cursor_pos = new_pos
            self.selection_start = None
            self.selection_end = None
    
    def _move_cursor_up(self, shift=False):
        """Move cursor up one line"""
        lines = self.content.split('\n')
        text_before = self.content[:self.cursor_pos]
        current_line = len(text_before.split('\n')) - 1
        
        if current_line > 0:
            # Calculate column position
            line_start = text_before.rfind('\n') + 1
            col = self.cursor_pos - line_start
            
            # Move to previous line
            prev_line_start = text_before[:line_start-1].rfind('\n') + 1
            new_pos = min(prev_line_start + col, len(self.content))
            new_pos = min(new_pos, self.content.find('\n', prev_line_start) if '\n' in self.content[prev_line_start:] else len(self.content))
            
            if shift:
                if self.selection_start is None:
                    self.selection_start = self.cursor_pos
                self.cursor_pos = new_pos
                self.selection_end = self.cursor_pos
            else:
                self.cursor_pos = new_pos
                self.selection_start = None
                self.selection_end = None
    
    def _move_cursor_down(self, shift=False):
        """Move cursor down one line"""
        lines = self.content.split('\n')
        text_before = self.content[:self.cursor_pos]
        current_line = len(text_before.split('\n')) - 1
        
        if current_line < len(lines) - 1:
            # Calculate column position
            line_start = text_before.rfind('\n') + 1
            col = self.cursor_pos - line_start
            
            # Move to next line
            next_line_start = self.content.find('\n', self.cursor_pos) + 1
            if next_line_start > 0:
                new_pos = min(next_line_start + col, len(self.content))
                new_pos = min(new_pos, self.content.find('\n', next_line_start) if '\n' in self.content[next_line_start:] else len(self.content))
                
                if shift:
                    if self.selection_start is None:
                        self.selection_start = self.cursor_pos
                    self.cursor_pos = new_pos
                    self.selection_end = self.cursor_pos
                else:
                    self.cursor_pos = new_pos
                    self.selection_start = None
                    self.selection_end = None
    
    def _move_to_line_start(self, shift=False):
        """Move to start of current line"""
        line_start = self.content.rfind('\n', 0, self.cursor_pos) + 1
        
        if shift:
            if self.selection_start is None:
                self.selection_start = self.cursor_pos
            self.cursor_pos = line_start
            self.selection_end = self.cursor_pos
        else:
            self.cursor_pos = line_start
            self.selection_start = None
            self.selection_end = None
    
    def _move_to_line_end(self, shift=False):
        """Move to end of current line"""
        line_end = self.content.find('\n', self.cursor_pos)
        if line_end == -1:
            line_end = len(self.content)
        
        if shift:
            if self.selection_start is None:
                self.selection_start = self.cursor_pos
            self.cursor_pos = line_end
            self.selection_end = self.cursor_pos
        else:
            self.cursor_pos = line_end
            self.selection_start = None
            self.selection_end = None
    
    def _delete_selection(self):
        """Delete selected text"""
        if self.selection_start is None:
            return
        
        start = min(self.selection_start, self.selection_end)
        end = max(self.selection_start, self.selection_end)
        
        self._save_undo()
        self.content = self.content[:start] + self.content[end:]
        self.cursor_pos = start
        self.selection_start = None
        self.selection_end = None
        self.modified = True
    
    def _unindent(self):
        """Unindent selected text"""
        if self.selection_start is None:
            return
        
        start = min(self.selection_start, self.selection_end)
        end = max(self.selection_start, self.selection_end)
        
        # Find line start
        line_start = self.content.rfind('\n', 0, start) + 1
        
        # Unindent each line
        lines = self.content[line_start:end].split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('    '):
                new_lines.append(line[4:])
            else:
                new_lines.append(line)
        
        self._save_undo()
        self.content = self.content[:line_start] + '\n'.join(new_lines) + self.content[end:]
        self.modified = True
    
    def _save_undo(self):
        """Save current state for undo"""
        self.undo_stack.append(self.content)
        self.redo_stack.clear()
        if len(self.undo_stack) > 100:
            self.undo_stack.pop(0)
    
    def undo(self):
        """Undo last action"""
        if self.undo_stack:
            self.redo_stack.append(self.content)
            self.content = self.undo_stack.pop()
            self.cursor_pos = len(self.content)
            self.modified = True
    
    def redo(self):
        """Redo last undone action"""
        if self.redo_stack:
            self.undo_stack.append(self.content)
            self.content = self.redo_stack.pop()
            self.cursor_pos = len(self.content)
            self.modified = True
    
    def save_file(self):
        """Save the current content"""
        try:
            from bridge.vos_api import vos_api
            
            if self.file_path and hasattr(vos_api, 'filesystem'):
                # Save through VOS filesystem
                file_obj = vos_api.filesystem.get_file(self.file_path)
                if file_obj:
                    file_obj.content = self.content
                    print(f"[VOS] Saved: {self.file_path}")
                    self.modified = False
                    return
            
            # Fallback: save to local file
            with open(self.filename, 'w') as f:
                f.write(self.content)
            print(f"[VOS] Saved local: {self.filename}")
            self.modified = False
            
        except Exception as e:
            print(f"[VOS] Failed to save: {e}")
    
    def open_file(self):
        """Open a file (placeholder)"""
        print("[VOS] Open file dialog coming soon...")
    
    def new_file(self):
        """Create new file"""
        if self.modified:
            # Ask to save
            print("[VOS] Unsaved changes - save dialog coming soon...")
        self.content = ""
        self.cursor_pos = 0
        self.modified = False
        self.filename = "Untitled"
        self.title = "Untitled - Text Editor"
    
    def _handle_mouse_click(self, event):
        """Handle mouse clicks for cursor positioning"""
        wx, wy = self.transform.position.x, self.transform.position.y
        mx, my = pygame.mouse.get_pos()
        rel_x = mx - wx
        rel_y = my - wy
        
        # Check if click is in text area
        line_num_width = 40 if self.show_line_numbers else 0
        text_start_x = line_num_width + 10
        text_start_y = 50
        
        if rel_x > text_start_x and rel_y > text_start_y:
            # Calculate cursor position from mouse
            lines = self.content.split('\n')
            line_index = (rel_y - text_start_y) // self.font_height
            if line_index < len(lines):
                # Calculate column
                col = (rel_x - text_start_x) // 8  # Approximate char width
                line = lines[line_index]
                
                # Find cursor position
                pos = 0
                for i in range(line_index):
                    pos += len(lines[i]) + 1
                pos += min(col, len(line))
                self.cursor_pos = min(pos, len(self.content))
                self.selection_start = None
                self.selection_end = None
    
    def draw(self, renderer):
        if self.minimized or self.closed:
            return
        
        super().draw(renderer)
        
        try:
            surface = renderer.surface
            wx, wy = self.transform.position.x, self.transform.position.y
            ww, wh = self.transform.size.width, self.transform.size.height
            
            editor_surf = pygame.Surface((ww, wh), pygame.SRCALPHA)
            
            # Background
            pygame.draw.rect(editor_surf, self.bg_color, (0, 0, ww, wh))
            
            # Menu bar
            menu_height = 30
            pygame.draw.rect(editor_surf, (35, 35, 38), (0, 0, ww, menu_height))
            
            # Draw menu items
            menu_x = 10
            font_menu = pygame.font.SysFont("Segoe UI", 12)
            for menu_name in self.menus.keys():
                menu_text = font_menu.render(menu_name, True, (180, 180, 190))
                editor_surf.blit(menu_text, (menu_x, 8))
                menu_x += menu_text.get_width() + 20
            
            # File info in menu bar
            modified_indicator = "*" if self.modified else ""
            file_info = f"{self.filename}{modified_indicator}"
            info_text = font_menu.render(file_info, True, (150, 150, 160))
            editor_surf.blit(info_text, (ww - info_text.get_width() - 10, 8))
            
            # Line numbers
            lines = self.content.split('\n')
            line_num_width = 40 if self.show_line_numbers else 0
            
            if self.show_line_numbers:
                pygame.draw.rect(editor_surf, self.line_number_bg, (0, menu_height, line_num_width, wh - menu_height))
                pygame.draw.line(editor_surf, (45, 45, 48), (line_num_width, menu_height), (line_num_width, wh))
            
            # Draw text
            text_start_y = menu_height + 10
            max_lines = (wh - menu_height - 40) // self.font_height
            visible_lines = lines[:max_lines]
            
            for i, line in enumerate(visible_lines):
                y_pos = text_start_y + i * self.font_height
                
                # Line number
                if self.show_line_numbers:
                    line_num = self.font.render(str(i + 1), True, self.line_numbers_color)
                    editor_surf.blit(line_num, (8, y_pos))
                
                # Line content with syntax highlighting
                if line:
                    # Simple syntax highlighting
                    if line.strip().startswith('#') or line.strip().startswith('//'):
                        color = (100, 180, 100)  # Green for comments
                    elif 'def ' in line or 'class ' in line:
                        color = (200, 150, 80)   # Orange for definitions
                    elif line.strip().startswith('import') or line.strip().startswith('from'):
                        color = (180, 120, 200)  # Purple for imports
                    elif '"' in line or "'" in line:
                        color = (200, 180, 100)  # Yellow for strings
                    else:
                        color = self.text_color
                    
                    text_surf = self.font.render(line, True, color)
                    editor_surf.blit(text_surf, (line_num_width + 10, y_pos))
            
            # Cursor
            if self.cursor_visible:
                # Calculate cursor position
                text_before = self.content[:self.cursor_pos]
                cursor_line = len(text_before.split('\n')) - 1
                if cursor_line < max_lines:
                    line_start = text_before.rfind('\n') + 1
                    cursor_col = self.cursor_pos - line_start
                    cursor_y = text_start_y + cursor_line * self.font_height
                    cursor_x = line_num_width + 10 + cursor_col * 8
                    pygame.draw.line(editor_surf, self.cursor_color,
                                   (cursor_x, cursor_y),
                                   (cursor_x, cursor_y + self.font_height), 2)
            
            # Selection highlighting
            if self.selection_start is not None and self.selection_end is not None:
                start = min(self.selection_start, self.selection_end)
                end = max(self.selection_start, self.selection_end)
                # Draw selection highlight
                # This is simplified - full implementation would need line-by-line rendering
            
            # Status bar
            status_y = wh - 30
            pygame.draw.rect(editor_surf, self.status_color, (0, status_y, ww, 30))
            
            # Status info
            line_count = len(lines)
            char_count = len(self.content)
            status_info = f"Line: {self.content.count('\n', 0, self.cursor_pos) + 1}  |  Col: {self.cursor_pos - (self.content.rfind('\n', 0, self.cursor_pos) + 1) + 1}  |  Lines: {line_count}  |  Chars: {char_count}"
            if self.modified:
                status_info += "  [Modified]"
            
            status_text = pygame.font.SysFont("Segoe UI", 11).render(status_info, True, (150, 150, 155))
            editor_surf.blit(status_text, (10, status_y + 8))
            
            # Line ending info
            line_ending = "LF"  # Unix style
            ending_text = pygame.font.SysFont("Segoe UI", 11).render(line_ending, True, (80, 80, 85))
            editor_surf.blit(ending_text, (ww - ending_text.get_width() - 10, status_y + 8))
            
            surface.blit(editor_surf, (wx, wy))
            
        except Exception as e:
            print(f"[VOS] Error drawing editor: {e}")
            import traceback
            traceback.print_exc()

    def show(self):
        """Show the editor window"""
        self.minimized = False
        self.closed = False
        self.is_active = True
        print(f"[VOS] Text Editor shown: {self.filename}")
        
        # Add to window manager
        try:
            from desktop.ui.window.window_manager import WindowManager
            wm = WindowManager.get_instance()  # Or however you get the WindowManager
            if self not in wm.windows:
                wm.add_window(self)
                print(f"[VOS] Editor added to WindowManager")
            else:
                print(f"[VOS] Editor already in WindowManager")
        except Exception as e:
            print(f"[VOS] Could not add to WindowManager: {e}")
            import traceback
            traceback.print_exc()
    
    def update(self, dt):
        super().update(dt)
        
        # Blink cursor
        self.cursor_timer += dt
        if self.cursor_timer > 0.5:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible