from chxchx_security.services.network import ALLOWED_MAC_MODES


def test_supported_modes_are_explicit():
    assert {"random", "stable", "stable-ssid"}.issubset(ALLOWED_MAC_MODES)
