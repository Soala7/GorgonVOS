"""
Gorgon OS (VOS)

Base animation class.
"""

from __future__ import annotations

class Animation:
    """
    Base animation class.
    """

    def __init__(self, duration: float = 1.0) -> None:

        self.duration = max(duration, 0.001)

        self.elapsed = 0.0

        self.playing = False

        self.finished = False

    def start(self) -> None:

        self.elapsed = 0.0

        self.playing = True

        self.finished = False

    def stop(self) -> None:

        self.playing = False

    def restart(self) -> None:

        self.start()

    def reset(self) -> None:

        self.elapsed = 0.0

        self.playing = False

        self.finished = False

    def update(self, dt: float) -> None:

        if not self.playing:
            return

        self.elapsed += dt

        if self.elapsed >= self.duration:

            self.elapsed = self.duration

            self.playing = False

            self.finished = True

    @property
    def progress(self) -> float:

        return self.elapsed / self.duration
