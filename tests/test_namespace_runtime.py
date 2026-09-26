from chxchx_security.services.namespace_runtime import NamespaceRuntime
from chxchx_security.services.session import SessionState
from chxchx_security.utils.process import CmdResult


def test_runtime_dry_run_never_calls_runner():
    calls = []
    runtime = NamespaceRuntime(runner=lambda command: calls.append(command))

    result = runtime.create("demo", dry_run=True)

    assert result.ok is True
    assert result.network_ready is False
    assert result.state is SessionState.STARTING
    assert calls == []


def test_runtime_creates_namespace_and_loopback():
    calls = []

    def runner(command):
        calls.append(tuple(command))
        return CmdResult(True, 0, "", "")

    runtime = NamespaceRuntime(runner=runner, privileged_prefix=("sudo",))
    result = runtime.create("demo")

    assert result.ok is True
    assert result.state is SessionState.ACTIVE
    assert result.network_ready is False
    assert calls == [
        ("sudo", "ip", "netns", "add", "chxsec-demo"),
        ("sudo", "ip", "netns", "exec", "chxsec-demo", "ip", "link", "set", "lo", "up"),
    ]


def test_runtime_rolls_back_when_loopback_setup_fails():
    calls = []

    def runner(command):
        calls.append(tuple(command))
        if len(calls) == 2:
            return CmdResult(False, 1, "", "loopback failed")
        return CmdResult(True, 0, "", "")

    runtime = NamespaceRuntime(runner=runner)
    result = runtime.create("demo")

    assert result.ok is False
    assert "rollback completed" in result.detail
    assert calls[-1] == ("sudo", "ip", "netns", "delete", "chxsec-demo")


def test_runtime_destroy_is_deterministic():
    calls = []
    runtime = NamespaceRuntime(
        runner=lambda command: calls.append(tuple(command))
        or CmdResult(True, 0, "", "")
    )

    result = runtime.destroy("demo")

    assert result.ok is True
    assert result.state is SessionState.DESTROYED
    assert calls == [("sudo", "ip", "netns", "delete", "chxsec-demo")]
