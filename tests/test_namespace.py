from chxchx_security.services import namespace


def test_namespace_tools_report_readiness(monkeypatch):
    monkeypatch.setattr(
        namespace,
        "exists",
        lambda command: command in {"ip", "nsenter", "nft"},
    )

    tools = namespace.detect_namespace_tools()

    assert tools.ready is True
    assert tools.as_dict() == {
        "ip": True,
        "nsenter": True,
        "nft": True,
        "sudo": False,
        "ready": True,
    }


def test_namespace_plan_is_not_executable_until_wiring_exists():
    plan = namespace.build_namespace_plan("wifi-01")

    assert plan.namespace == "chxsec-wifi-01"
    assert plan.executable is False
    assert any(step.status == "not_implemented" for step in plan.steps)
    assert plan.steps[0].command == ("sudo", "ip", "netns", "add", "chxsec-wifi-01")


def test_namespace_plan_json_contains_no_machine_data():
    payload = namespace.build_namespace_plan("demo").as_json()

    assert "demo" in payload
    assert "/home/" not in payload
    assert "hostname" not in payload
