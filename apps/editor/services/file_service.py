"""
Gorgon OS (VOS)

Editor File Service
-------------------
Handles opening, creating, and saving VirtualFS files.

The editor window should not need to know how the VFS
stores files internally.
"""

from __future__ import annotations

from typing import Any


class EditorFileService:
    """
    Handles file operations for the text editor.

    This class works with the VOS VirtualFile abstraction.

    It intentionally supports both:
        - read_text() / write_text()
        - content

    so it can work with the VFS implementation you
    currently have while remaining easy to change later.
    """

    # --------------------------------------------------
    # Reading
    # --------------------------------------------------

    def read_file(self, virtual_file: Any) -> str:
        """
        Read text from a VirtualFile.
        """

        if virtual_file is None:
            return ""

        if hasattr(virtual_file, "read_text"):

            content = virtual_file.read_text()

            if content is None:
                return ""

            return str(content)

        if hasattr(virtual_file, "content"):

            content = virtual_file.content

            if content is None:
                return ""

            return str(content)

        raise TypeError(
            "VirtualFile does not support text reading."
        )

    # --------------------------------------------------
    # Writing
    # --------------------------------------------------

    def write_file(
        self,
        virtual_file: Any,
        content: str,
    ) -> bool:
        """
        Write text into a VirtualFile.
        """

        if virtual_file is None:
            return False

        if hasattr(virtual_file, "write_text"):

            virtual_file.write_text(content)
            return True

        if hasattr(virtual_file, "content"):

            virtual_file.content = content
            return True

        raise TypeError(
            "VirtualFile does not support text writing."
        )

    # --------------------------------------------------
    # File Name
    # --------------------------------------------------

    def get_file_name(
        self,
        virtual_file: Any,
    ) -> str:
        """
        Returns the filename used by the editor.
        """

        if virtual_file is None:
            return "Untitled.txt"

        return str(
            getattr(
                virtual_file,
                "name",
                "Untitled.txt",
            )
        )

    # --------------------------------------------------
    # Convert VFS File -> Editor Buffer
    # --------------------------------------------------

    def load_file(
        self,
        virtual_file: Any,
    ) -> tuple[str, str]:
        """
        Loads a VirtualFile.

        Returns:

            (filename, content)
        """

        file_name = self.get_file_name(
            virtual_file
        )

        content = self.read_file(
            virtual_file
        )

        return (
            file_name,
            content.replace(
                "\r\n",
                "\n",
            ).replace(
                "\r",
                "\n",
            ),
        )

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    def save_file(
        self,
        virtual_file: Any,
        content: str,
    ) -> bool:
        """
        Saves editor content to a VirtualFile.
        """

        return self.write_file(
            virtual_file,
            content,
        )