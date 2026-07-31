# apps/explorer/explorer_operations.py
"""File operations for Explorer - Create, Delete, Rename, Open"""

class ExplorerOperations:
    """Mixin class for file operations"""
    
    def create_new_file(self, filename=None):
        """Create a new file in the current folder"""
        if self.current_folder is None:
            print("[VOS] Cannot create file: No folder selected")
            return False
        
        if not filename:
            import time
            filename = f"NewFile_{int(time.time())}.txt"
        
        if hasattr(self.current_folder, 'files'):
            if filename in self.current_folder.files:
                print(f"[VOS] File '{filename}' already exists")
                return False
        
        if hasattr(self.current_folder, 'create_file'):
            self.current_folder.create_file(filename, "")
        else:
            if isinstance(self.current_folder.files, dict):
                self.current_folder.files[filename] = ""
            elif isinstance(self.current_folder.files, list):
                self.current_folder.files.append(filename)
        
        print(f"[VOS] Created file: {filename}")
        return True

    def create_new_folder(self, foldername=None):
        """Create a new folder in the current directory"""
        if self.current_folder is None:
            print("[VOS] Cannot create folder: No folder selected")
            return False
        
        if not foldername:
            import time
            foldername = f"NewFolder_{int(time.time())}"
        
        if hasattr(self.current_folder, 'folders'):
            if foldername in self.current_folder.folders:
                print(f"[VOS] Folder '{foldername}' already exists")
                return False
        
        if hasattr(self.current_folder, 'create_folder'):
            self.current_folder.create_folder(foldername)
        else:
            if isinstance(self.current_folder.folders, dict):
                self.current_folder.folders[foldername] = type('Folder', (object,), {
                    'name': foldername,
                    'parent': self.current_folder,
                    'folders': {},
                    'files': {}
                })()
            elif isinstance(self.current_folder.folders, list):
                self.current_folder.folders.append(foldername)
        
        print(f"[VOS] Created folder: {foldername}")
        return True

    def delete_item(self, item):
        """Delete a file or folder"""
        if self.current_folder is None:
            print("[VOS] Cannot delete: No folder selected")
            return False
        
        item_name = getattr(item, 'name', None)
        if not item_name:
            print("[VOS] Cannot delete: Invalid item")
            return False
        
        is_folder = self._is_item_folder(item)
        
        if hasattr(self.current_folder, 'delete_item'):
            success = self.current_folder.delete_item(item_name)
            if success:
                print(f"[VOS] Deleted: {item_name}")
                if self.selected_item == item:
                    self.selected_item = None
                return True
        
        try:
            if is_folder:
                if hasattr(self.current_folder, 'folders'):
                    if isinstance(self.current_folder.folders, dict):
                        if item_name in self.current_folder.folders:
                            del self.current_folder.folders[item_name]
                    elif isinstance(self.current_folder.folders, list):
                        if item_name in self.current_folder.folders:
                            self.current_folder.folders.remove(item_name)
            else:
                if hasattr(self.current_folder, 'files'):
                    if isinstance(self.current_folder.files, dict):
                        if item_name in self.current_folder.files:
                            del self.current_folder.files[item_name]
                    elif isinstance(self.current_folder.files, list):
                        if item_name in self.current_folder.files:
                            self.current_folder.files.remove(item_name)
            
            if self.selected_item == item:
                self.selected_item = None
            print(f"[VOS] Deleted: {item_name}")
            return True
        except Exception as e:
            print(f"[VOS] Failed to delete {item_name}: {e}")
            return False

    def rename_item(self, item, new_name):
        """Rename a file or folder"""
        if self.current_folder is None:
            return False
        
        old_name = getattr(item, 'name', None)
        if not old_name:
            return False
        
        is_folder = self._is_item_folder(item)
        
        if hasattr(self.current_folder, 'rename_item'):
            return self.current_folder.rename_item(old_name, new_name)
        
        try:
            if is_folder:
                if hasattr(self.current_folder, 'folders'):
                    if old_name in self.current_folder.folders:
                        folder_data = self.current_folder.folders.pop(old_name)
                        self.current_folder.folders[new_name] = folder_data
                        folder_data.name = new_name
            else:
                if hasattr(self.current_folder, 'files'):
                    if old_name in self.current_folder.files:
                        file_data = self.current_folder.files.pop(old_name)
                        self.current_folder.files[new_name] = file_data
                        if hasattr(item, 'name'):
                            item.name = new_name
            
            print(f"[VOS] Renamed: {old_name} -> {new_name}")
            return True
        except Exception as e:
            print(f"[VOS] Failed to rename: {e}")
            return False

    def open_item(self, item):
        """Open a file or folder"""
        item_name = getattr(item, 'name', 'Unknown')
        print(f"[VOS] open_item called for: '{item_name}'")
        
        if self._is_item_folder(item):
            print(f"[VOS] Opening folder: '{item_name}'")
            self.navigate_to(item)
        else:
            print(f"[VOS] Opening file: '{item_name}'")
            self.open_file(item_name, item)

    def open_file(self, filename, item=None):
        """Open a file with the appropriate application"""
        ext = filename.split('.')[-1] if '.' in filename else ''
        
        content = ""
        if hasattr(self.current_folder, 'get_file_content'):
            content = self.current_folder.get_file_content(filename)
        elif item and hasattr(item, 'content'):
            content = item.content
        elif hasattr(self.current_folder, 'files'):
            if isinstance(self.current_folder.files, dict):
                content = self.current_folder.files.get(filename, "")
        
        if ext in ['txt', 'py', 'md', 'json', 'xml', 'css', 'js', 'html', 'htm']:
            self.open_in_editor(filename, content)
        elif ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            self.open_in_viewer(filename)
        elif ext in ['mp3', 'wav', 'ogg']:
            self.open_in_player(filename)
        elif ext in ['mp4', 'avi', 'mkv']:
            self.open_in_video_player(filename)
        else:
            self.open_in_editor(filename, content)

    def open_in_editor(self, filename, content=""):
        """Open file in text editor"""
        try:
            from apps.editor.text_editor import TextEditorApp
            
            file_path = self._get_file_path(filename)
            
            print(f"[VOS] Creating editor for: {filename}")
            
            editor = TextEditorApp(filename, content, file_path)
            
            editor.transform.position.x = 200
            editor.transform.position.y = 100
            editor.is_active = True
            editor.minimized = False
            editor.closed = False
            
            # Use the window_manager from explorer
            if hasattr(self, 'window_manager') and self.window_manager:
                self.window_manager.add_window(editor)
                print(f"[VOS] Editor added to WindowManager")
            else:
                print(f"[VOS] No WindowManager - trying fallback")
                # Try to add to window manager via the main window
                try:
                    # Search for window manager in the app
                    import sys
                    for obj in sys.modules.values():
                        if hasattr(obj, 'window_manager'):
                            wm = getattr(obj, 'window_manager')
                            if wm and hasattr(wm, 'add_window'):
                                wm.add_window(editor)
                                print(f"[VOS] Editor added via module")
                                break
                    else:
                        editor.show()
                except:
                    editor.show()
            
            print(f"[VOS] Opened editor for: {filename}")
            return True
            
        except ImportError as e:
            print(f"[VOS] Text editor not found: {e}")
            self.create_simple_editor(filename, content)
            return False
        except Exception as e:
            print(f"[VOS] Failed to open editor: {e}")
            import traceback
            traceback.print_exc()
            return False

    def open_in_viewer(self, filename):
        """Open image in viewer"""
        print(f"[VOS] Opening image viewer for: {filename}")

    def open_in_player(self, filename):
        """Open audio in player"""
        print(f"[VOS] Opening audio player for: {filename}")

    def open_in_video_player(self, filename):
        """Open video in player"""
        print(f"[VOS] Opening video player for: {filename}")

    def _get_file_path(self, filename):
        """Get full path of a file"""
        if hasattr(self.current_folder, 'path'):
            return f"{self.current_folder.path}/{filename}"
        elif self.current_folder is not None:
            folder_name = getattr(self.current_folder, 'name', '')
            return f"/{folder_name}/{filename}"
        return f"/{filename}"

    def create_simple_editor(self, filename, content):
        """Fallback: Create a simple console editor"""
        print("\n" + "="*50)
        print(f"EDITOR: {filename}")
        print("="*50)
        print(content)
        print("="*50)
        print("(Simple editor - open in GUI next time)")