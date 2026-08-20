"""
Gorgon OS (VOS)

FileSystemStorage Manager
Handles serializing, saving, and loading the virtual filesystem hierarchy
to/from virtual disk block storage with local file system backup support.
"""

from __future__ import annotations

import json
import os
from typing import Any, Optional

from filesystem.folder import Folder
from filesystem.virtual_file import VirtualFile

class FileSystemStorage:
    """Manages filesystem state persistence and tree serialization."""

    def __init__(self, disk: Any) -> None:
        self.disk = disk

    def save(self, root: Folder, path: str = "VOS.os") -> bool:
        """
        Serializes the filesystem tree and writes it to the virtual disk Registry,
        with a secondary JSON backup written to the local host filesystem path.
        """
        if not root:
            print("[STORAGE] Error: Cannot save null root directory.")
            return False

        try:
            data = self._folder_to_dict(root)
            metadata = json.dumps(data)
            payload = metadata.encode("utf-8")

            if hasattr(self.disk, "file_table") and "Registry" in self.disk.file_table:
                if hasattr(self.disk, "delete_file"):
                    self.disk.delete_file("Registry")

            if hasattr(self.disk, "create_file"):
                self.disk.create_file("Registry", payload)
                print("[STORAGE] Filesystem registry written to virtual disk.")

            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            print(f"[STORAGE] Filesystem successfully backed up: {path}")
            return True

        except Exception as e:
            print(f"[STORAGE] Save error: {e}")
            return False

    def load(self, path: str = "VOS.os") -> Optional[Folder]:
        """
        Restores the filesystem hierarchy. Priority is given to the virtual disk
        Registry file; falls back to the local backup file if unavailable.
        """

        if hasattr(self.disk, "file_table") and "Registry" in self.disk.file_table:
            try:
                raw_data = self.disk.read_file("Registry")
                if isinstance(raw_data, bytes):
                    metadata = raw_data.decode("utf-8")
                else:
                    metadata = str(raw_data)

                data = json.loads(metadata)
                print("[STORAGE] Filesystem loaded successfully from virtual disk.")
                return self._dict_to_folder(data)
            except Exception as e:
                print(f"[STORAGE] Virtual disk loading failed: {e}. Checking backup...")

        if not os.path.exists(path):
            print(f"[STORAGE] Save backup not found: {path}")
            return None

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            print(f"[STORAGE] Filesystem restored from local backup: {path}")
            return self._dict_to_folder(data)

        except Exception as e:
            print(f"[STORAGE] Failed to load local backup: {e}")
            return None

    def _folder_to_dict(self, folder: Folder) -> dict[str, Any]:
        """Recursively converts a Folder tree into a serializable dictionary structure."""
        return {
            "name": getattr(folder, "name", "root"),
            "files": {
                name: {
                    "name": getattr(virtual_file, "name", name),
                    "content": getattr(virtual_file, "content", ""),
                }
                for name, virtual_file in getattr(folder, "files", {}).items()
            },
            "folders": {
                name: self._folder_to_dict(subfolder)
                for name, subfolder in getattr(folder, "folders", {}).items()
            },
        }

    def _dict_to_folder(self, data: dict[str, Any], parent: Optional[Folder] = None) -> Folder:
        """Recursively deserializes a dictionary structure back into a Folder hierarchy."""
        folder_name = data.get("name", "root")
        folder = Folder(folder_name, parent=parent)

        for filename, file_data in data.get("files", {}).items():
            if isinstance(file_data, dict):
                fname = file_data.get("name", filename)
                fcontent = file_data.get("content", "")
            else:
                fname = filename
                fcontent = str(file_data)

            virtual_file = VirtualFile(fname, fcontent)
            folder.files[filename] = virtual_file

        for name, subfolder_data in data.get("folders", {}).items():
            subfolder = self._dict_to_folder(subfolder_data, parent=folder)
            if hasattr(folder, "add_folder"):
                folder.add_folder(subfolder)
            else:
                folder.folders[name] = subfolder

        return folder
