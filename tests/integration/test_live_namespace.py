import os

import pytest

from chxchx_security.services.namespace_runtime import NamespaceRuntime
from chxchx_security.services.firewall_plan import table_names
from chxchx_security.services.firewall_runtime import FirewallRuntime
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


def test_live_firewall_apply_and_remove_leaves_other_rules_untouched():
    if os.getenv("CHXSEC_RUN_NAMESPACE_TESTS") != "1":
        pytest.skip("set CHXSEC_RUN_NAMESPACE_TESTS=1 to run namespace tests")

    if os.geteuid() != 0:
        sudo_check = run(["sudo", "-n", "true"], timeout=5)
        if not sudo_check.ok:
            pytest.skip("namespace test requires root or passwordless sudo")

    def ruleset():
        return run(["sudo", "nft", "-s", "list", "ruleset"]).stdout

    before = ruleset()
    runtime = FirewallRuntime()
    filter_table, nat_table = table_names("integration-fw")
    result = runtime.apply("integration-fw", subnet="10.203.10.0/30")
    try:
        assert result.ok is True, result.detail
        during = ruleset()
        assert filter_table in during and nat_table in during
        assert runtime.apply("integration-fw", subnet="10.203.10.0/30").ok is False
    finally:
        removed = runtime.remove("integration-fw")
        assert removed.ok is True, removed.detail
    assert ruleset() == before
