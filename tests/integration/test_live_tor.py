import os

import pytest

from chxchx_security.config import Settings
from chxchx_security.services.tor import run_protected, verify


pytestmark = pytest.mark.live


def _require_live_tests():
    if os.getenv("CHXSEC_RUN_LIVE_TESTS") != "1":
        pytest.skip("set CHXSEC_RUN_LIVE_TESTS=1 to run live Tor tests")


def test_live_tor_route_is_verified():
    _require_live_tests()

    result = verify(Settings.from_env())

    assert result.ok is True
    assert result.is_tor is True


def test_live_protected_https_request():
    _require_live_tests()

    exit_code = run_protected(
        Settings.from_env(),
        [
            "curl",
            "--fail",
            "--silent",
            "--show-error",
            "--output",
            "/dev/null",
            "https://example.com",
        ],
    )

    assert exit_code == 0
