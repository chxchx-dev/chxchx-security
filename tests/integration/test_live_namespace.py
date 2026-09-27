import os

import pytest

from chxchx_security.services.namespace_runtime import NamespaceRuntime
from chxchx_security.services.network_runtime import NetworkRuntime
from chxchx_security.utils.process import run


pytestmark = pytest.mark.live


def test_live_namespace_create_and_destroy():
    if os.getenv("CHXSEC_RUN_NAMESPACE_TESTS") != "1":
        pytest.skip("set CHXSEC_RUN_NAMESPACE_TESTS=1 to run namespace tests")

    if os.geteuid() != 0:
        sudo_check = run(["sudo", "-n", "true"], timeout=5)
        if not sudo_check.ok:
            pytest.skip("namespace test requires root or passwordless sudo")

    runtime = NamespaceRuntime()
    result = runtime.create("integration")
    try:
        assert result.ok is True, result.detail
        assert result.network_ready is False
    finally:
        destroyed = runtime.destroy("integration")
        assert destroyed.ok is True, destroyed.detail


def test_live_network_apply_and_destroy():
    if os.getenv("CHXSEC_RUN_NAMESPACE_TESTS") != "1":
        pytest.skip("set CHXSEC_RUN_NAMESPACE_TESTS=1 to run namespace tests")

    if os.geteuid() != 0:
        sudo_check = run(["sudo", "-n", "true"], timeout=5)
        if not sudo_check.ok:
            pytest.skip("namespace test requires root or passwordless sudo")

    result = NetworkRuntime().apply("integration-net", subnet="10.203.9.0/30")
    try:
        assert result.ok is True, result.detail
        routes = run(["sudo", "ip", "netns", "exec", "chxsec-integration-net", "ip", "route"])
        assert "default" not in routes.stdout
    finally:
        destroyed = NamespaceRuntime().destroy("integration-net")
        assert destroyed.ok is True, destroyed.detail
