import pytest

from chxchx_security.services.session import (
    SessionError,
    SessionEvent,
    SessionLifecycle,
    SessionState,
    namespace_name,
    validate_session_id,
)


def test_session_lifecycle_reaches_active_and_destroyed():
    session = SessionLifecycle("abc123")

    session = session.advance(SessionEvent.START)
    assert session.state is SessionState.STARTING
    assert session.namespace == "chxsec-abc123"

    session = session.advance(SessionEvent.READY)
    assert session.state is SessionState.ACTIVE
    session = session.advance(SessionEvent.STOP)
    session = session.advance(SessionEvent.DESTROY)
    assert session.state is SessionState.DESTROYED


def test_failed_session_can_only_be_destroyed():
    session = SessionLifecycle("abc123").advance(SessionEvent.FAIL)

    with pytest.raises(SessionError):
        session.advance(SessionEvent.START)

    assert session.advance(SessionEvent.DESTROY).state is SessionState.DESTROYED


@pytest.mark.parametrize("session_id", ["ABC", "has space", "../escape", "a_underscore"])
def test_session_ids_reject_namespace_injection(session_id):
    with pytest.raises(SessionError):
        validate_session_id(session_id)


def test_namespace_name_uses_validated_identifier():
    assert namespace_name("wifi-01") == "chxsec-wifi-01"
