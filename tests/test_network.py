from chxchx_security.services.network import ALLOWED_MAC_MODES, ConnectionInfo, connection_label


def test_supported_modes_are_explicit():
    assert {"random", "stable", "stable-ssid"}.issubset(ALLOWED_MAC_MODES)


def test_connection_label_hides_local_identifier_by_default():
    connection = ConnectionInfo("Private WiFi", "802-11-wireless")

    assert connection_label(connection) == "Wi-Fi connection"
    assert connection_label(connection, reveal_identifiers=True) == "Private WiFi (802-11-wireless)"
