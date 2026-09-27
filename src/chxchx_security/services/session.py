from __future__ import annotations

import re
import secrets
from dataclasses import dataclass
from enum import Enum


class SessionError(ValueError):
    """Raised when a protected-session lifecycle operation is invalid."""


class SessionState(str, Enum):
    CREATED = "CREATED"
    STARTING = "STARTING"
    ACTIVE = "ACTIVE"
    STOPPING = "STOPPING"
    DESTROYED = "DESTROYED"
    FAILED = "FAILED"


class SessionEvent(str, Enum):
    START = "start"
    READY = "ready"
    STOP = "stop"
    DESTROY = "destroy"
    FAIL = "fail"


_SESSION_ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,30}[a-z0-9])?$")

_TRANSITIONS: dict[SessionState, dict[SessionEvent, SessionState]] = {
    SessionState.CREATED: {
        SessionEvent.START: SessionState.STARTING,
        SessionEvent.FAIL: SessionState.FAILED,
        SessionEvent.DESTROY: SessionState.DESTROYED,
    },
    SessionState.STARTING: {
        SessionEvent.READY: SessionState.ACTIVE,
        SessionEvent.FAIL: SessionState.FAILED,
    },
    SessionState.ACTIVE: {
        SessionEvent.STOP: SessionState.STOPPING,
        SessionEvent.FAIL: SessionState.FAILED,
    },
    SessionState.STOPPING: {
        SessionEvent.DESTROY: SessionState.DESTROYED,
        SessionEvent.FAIL: SessionState.FAILED,
    },
    SessionState.FAILED: {
        SessionEvent.DESTROY: SessionState.DESTROYED,
    },
    SessionState.DESTROYED: {},
}


def validate_session_id(session_id: str) -> str:
    """Validate an identifier before it can become a namespace name."""
    if not _SESSION_ID_RE.fullmatch(session_id):
        raise SessionError(
            "session id must use lowercase letters, numbers and internal hyphens"
        )
    return session_id


def new_session_id() -> str:
    return secrets.token_hex(4)


def namespace_name(session_id: str) -> str:
    return f"chxsec-{validate_session_id(session_id)}"


@dataclass(frozen=True)
class SessionLifecycle:
    session_id: str
    state: SessionState = SessionState.CREATED

    def __post_init__(self) -> None:
        validate_session_id(self.session_id)

    @property
    def namespace(self) -> str:
        return namespace_name(self.session_id)

    def advance(self, event: SessionEvent) -> "SessionLifecycle":
        try:
            next_state = _TRANSITIONS[self.state][event]
        except KeyError as exc:
            raise SessionError(
                f"cannot apply {event.value} while session is {self.state.value}"
            ) from exc
        return SessionLifecycle(self.session_id, next_state)
