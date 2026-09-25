from chxchx_security.config import Settings
from chxchx_security.services.tor import protected_argv


def settings():
    return Settings(
        app_name="x",
        tor_socks_host="127.0.0.1",
        tor_socks_port=9050,
        tor_check_url="https://check.torproject.org/api/ip",
        http_timeout_seconds=10,
        allow_direct_network_tests=False,
        enable_runtime_logs=False,
        log_level="WARNING",
    )


def test_protected_argv_isolates():
    argv = protected_argv(settings(), ["curl", "https://example.com"])
    assert argv[:2] == ["torsocks", "--isolate"]
    assert "curl" in argv
