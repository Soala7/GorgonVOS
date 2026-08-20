# editor_search.py
from __future__ import annotations
from typing import Any, List, Tuple


class EditorSearch:
    """Handles text query matching in the current buffer and folder file search."""

    def __init__(self) -> None:
        self.active_query: str = ""
        self.matches: List[Tuple[int, int]] = []  # List of (row, col) matches
        self.current_match_idx: int = -1

    def find_in_buffer(self, buffer_lines: List[str], query: str) -> List[Tuple[int, int]]:
        """Search for a string query inside active document lines."""
        self.active_query = query
        self.matches = []
        self.current_match_idx = -1

        if not query:
            return self.matches

        query_lower = query.lower()
        for row, line in enumerate(buffer_lines):
            line_lower = line.lower()
            start = 0
            while True:
                idx = line_lower.find(query_lower, start)
                if idx == -1:
                    break
                self.matches.append((row, idx))
                start = idx + max(1, len(query_lower))

        if self.matches:
            self.current_match_idx = 0

        return self.matches

    def next_match(self) -> Tuple[int, int] | None:
        """Jump to the next search result inside the document."""
        if not self.matches:
            return None
        self.current_match_idx = (self.current_match_idx + 1) % len(self.matches)
        return self.matches[self.current_match_idx]

    def search_target_directory(
        self, dir_node: Any, query: str
    ) -> List[dict[str, Any]]:
        """
        Scan a VFS target directory node (e.g. Documents, Downloads) 
        for matching file names and extension types.
        """
        if not dir_node or not query:
            return []

        results = []
        children = []

        if hasattr(dir_node, "get_children"):
            children = dir_node.get_children()
        elif hasattr(dir_node, "children"):
            children = (
                list(dir_node.children.values())
                if isinstance(dir_node.children, dict)
                else dir_node.children
            )

        query_lower = query.lower()
        for node in children:
            name = getattr(node, "name", "")
            if query_lower in name.lower():
                results.append(
                    {
                        "name": name,
                        "node": node,
                        "is_dir": getattr(node, "is_directory", False),
                    }
                )

        return results