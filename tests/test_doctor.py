from chxchx_security.config import Settings
from chxchx_security.services import audit


def settings():
    return Settings(
        app_name="test",
        tor_socks_host="127.0.0.1",
        tor_socks_port=9050,
        tor_check_url="https://check.torproject.org/api/ip",
        http_timeout_seconds=10,
        allow_direct_network_tests=False,
        enable_runtime_logs=False,
        log_level="WARNING",
    )


def test_doctor_reports_required_dependencies(monkeypatch):
    monkeypatch.setattr(audit, "exists", lambda command: command != "firewall-cmd")
    monkeypatch.setattr(audit, "service_state", lambda: "active")
    monkeypatch.setattr(audit, "socks_reachable", lambda _settings: True)

    checks = audit.doctor(settings())

    assert checks
    assert all(check.ok for check in checks)
    assert {check.name for check in checks} == {
        "OS",
        "Tor binary",
        "torsocks",
        "curl",
        "NetworkManager CLI",
        "Tor service",
        "Tor SOCKS",
    }
