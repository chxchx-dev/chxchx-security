import pytest

from chxchx_security.utils.process import run


def test_run_captures_output_and_return_code():
    result = run(["sh", "-c", "printf output; printf error >&2; exit 3"])

    assert result.ok is False
    assert result.returncode == 3
    assert result.stdout == "output"
    assert result.stderr == "error"


def test_run_check_raises_for_failed_command():
    with pytest.raises(RuntimeError, match="failed"):
        run(["sh", "-c", "printf failed >&2; exit 1"], check=True)
