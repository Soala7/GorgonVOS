
"""Application launcher system"""

class AppLauncher:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_apps()
        return cls._instance

    def _init_apps(self):
        """Initialize app registry"""
        self.apps = {}
        self.associations = {
            '.txt': 'text_editor',
            '.py': 'text_editor',
            '.md': 'text_editor',
            '.json': 'text_editor',
            '.xml': 'text_editor',
            '.css': 'text_editor',
            '.js': 'text_editor',
            '.html': 'browser',
            '.htm': 'browser',
            '.jpg': 'image_viewer',
            '.jpeg': 'image_viewer',
            '.png': 'image_viewer',
            '.gif': 'image_viewer',
            '.bmp': 'image_viewer',
            '.mp3': 'music_player',
            '.wav': 'music_player',
            '.mp4': 'video_player',
            '.avi': 'video_player',
        }

    def launch_app(self, app_name, file_path=None):
        """Launch an application"""
        if app_name == 'explorer':
            return self._launch_explorer()
        elif app_name == 'text_editor':
            return self._launch_editor(file_path)
        elif app_name == 'terminal':
            return self._launch_terminal()
        elif app_name == 'browser':
            return self._launch_browser()
        else:
            print(f"[VOS] Unknown app: {app_name}")
            return False

    def _launch_explorer(self):
        """Launch explorer"""
        try:
            from apps.explorer.explorer_window import ExplorerWindow
            explorer = ExplorerWindow()
            explorer.show()
            return True
        except Exception as e:
            print(f"[VOS] Failed to launch explorer: {e}")
            return False

    def _launch_editor(self, file_path=None):
        """Launch text editor"""
        try:
            from apps.editor.editor import TextEditorApp

            content = ""
            filename = "Untitled"

            if file_path:
                import os
                filename = os.path.basename(file_path)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                except:
                    pass

            editor = TextEditorApp(filename, content, file_path)
            editor.show()
            return True
        except Exception as e:
            print(f"[VOS] Failed to launch editor: {e}")
            return False

    def _launch_terminal(self):
        """Launch terminal"""
        try:
            from apps.terminal.terminal_window import TerminalWindow
            terminal = TerminalWindow()
            terminal.show()
            return True
        except:
            return False

    def _launch_browser(self):
        """Launch browser"""
        try:
            from apps.browser.browser import BrowserWindow
            browser = BrowserWindow()
            browser.show()
            return True
        except:
            return False

    def get_file_association(self, extension):
        """Get app for file extension"""
        return self.associations.get(extension.lower(), None)
