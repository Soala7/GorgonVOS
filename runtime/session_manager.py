

import time
from core.logger import Logger

class Session:
    """
    Represents a single user session in VOS.
    """

    def __init__(self, session_id, user):
        self.session_id = session_id
        self.user = user

        self.state = "ACTIVE"
        self.created_at = time.time()
        self.closed_at = None

        self.processes = []

    def add_process(self, pid):
        if pid not in self.processes:
            self.processes.append(pid)

    def remove_process(self, pid):
        if pid in self.processes:
            self.processes.remove(pid)

    def close(self):
        self.state = "CLOSED"
        self.closed_at = time.time()

class SessionManager:
    """
    Handles user sessions inside VOS.
    """

    def __init__(self, event_bus, process_table):
        self.logger = Logger("SessionManager")

        self.event_bus = event_bus
        self.process_table = process_table

        self.sessions = {}
        self.active_session = None
        self.next_session_id = 1

    def create_session(self, user):
        session_id = self.next_session_id
        self.next_session_id += 1

        session = Session(session_id, user)

        self.sessions[session_id] = session
        self.active_session = session

        self.logger.info(f"Session created for user: {user}")

        if self.event_bus:
            self.event_bus.emit("session:created", {
                "session_id": session_id,
                "user": user
            })

        return session

    def close_session(self, session_id):
        session = self.sessions.get(session_id)

        if not session:
            self.logger.error(f"Session {session_id} not found")
            return False

        session.close()

        for pid in list(session.processes):
            self.process_table.terminate_process(pid)

        if self.active_session and self.active_session.session_id == session_id:
            self.active_session = None

        self.logger.info(f"Session closed: {session_id}")

        if self.event_bus:
            self.event_bus.emit("session:closed", {
                "session_id": session_id
            })

        return True

    def close_all_sessions(self):
        self.logger.info("Closing all sessions...")

        for session_id in list(self.sessions.keys()):
            self.close_session(session_id)

    def get_active_session(self):
        return self.active_session

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def list_sessions(self):
        return list(self.sessions.values())
