import pytest

from chxchx_security.config import ConfigurationError, Settings


def test_settings_use_safe_defaults(monkeypatch):
    monkeypatch.delenv("CHXSEC_TOR_SOCKS_PORT", raising=False)
    monkeypatch.delenv("CHXSEC_HTTP_TIMEOUT_SECONDS", raising=False)

    settings = Settings.from_env()

    assert settings.tor_socks_port == 9050
    assert settings.http_timeout_seconds == 15
    assert settings.allow_direct_network_tests is False


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("CHXSEC_TOR_SOCKS_PORT", "not-a-port"),
        ("CHXSEC_TOR_SOCKS_PORT", "0"),
        ("CHXSEC_TOR_SOCKS_PORT", "65536"),
        ("CHXSEC_HTTP_TIMEOUT_SECONDS", "-1"),
    ],
)
def test_invalid_numeric_settings_fail_closed(monkeypatch, name, value):
    monkeypatch.setenv(name, value)

    with pytest.raises(ConfigurationError):
        Settings.from_env()
