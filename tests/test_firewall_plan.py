from chxchx_security.services.firewall_plan import build_firewall_plan


def test_firewall_plan_is_fail_closed_and_uses_private_tor_redirects():
    plan = build_firewall_plan("demo", subnet="10.203.0.0/30")

    assert plan.executable is False
    assert "policy drop" in plan.ruleset
    assert "tcp redirect to :9040" in plan.ruleset
    assert "udp dport 53 redirect to :5353" in plan.ruleset
    assert 'iifname "chxh-2a97516c" ip saddr 10.203.0.2 drop' in plan.ruleset
    assert "chxsec_nat_2a97516c" in plan.ruleset


def test_firewall_plan_reuses_network_and_tor_validation():
    plan = build_firewall_plan(
        "demo",
        subnet="10.203.0.0/30",
        trans_port=19040,
        dns_port=15353,
    )

    assert plan.trans_port == 19040
    assert plan.dns_port == 15353
    assert ":19040" in plan.ruleset
    assert ":15353" in plan.ruleset
