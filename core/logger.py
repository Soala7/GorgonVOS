from datetime import datetime

class Logger:
    def __init__(self, name = "VOS"):
        self.name = name

    def _format(self, level, message):
        time = datetime.now().strftime("%H:%M:%S")
        return f"[{time}] [{self.name}] [{level}] {message}"

    def info(self, message):
        print(self._format("INFO", message))

    def warning(self, message):
        print(self._format("WARN", message))

    def error(self, message):
        print(self._format("ERROR", message))

    def debug(self, message):
        print(self._format("DEBUG", message))