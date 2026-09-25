from chxchx_security.utils.redact import mask_ip, redact_text


def test_mask_ipv4():
    assert mask_ip("203.0.113.42") == "203.0.x.x"


def test_redact_mac():
    assert "AA:BB:CC:DD:EE:FF" not in redact_text("mac AA:BB:CC:DD:EE:FF")
