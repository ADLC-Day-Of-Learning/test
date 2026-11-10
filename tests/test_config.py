"""Tests for repository configuration and Ruff linter behavior."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_pyproject_toml_configuration():
    """Verify that pyproject.toml defines project metadata and tool settings."""
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    assert pyproject_path.exists(), "pyproject.toml must exist at repo root"

    if sys.version_info >= (3, 11):
        import tomllib
    else:
        try:
            import tomli as tomllib
        except ImportError:
            pytest.skip("tomllib or tomli required to parse pyproject.toml on Python < 3.11")

    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)

    assert config["build-system"]["build-backend"] == "setuptools.build_meta"
    assert "setuptools>=61.0" in config["build-system"]["requires"]
    assert config["project"]["name"] == "pong"
    assert config["project"]["requires-python"] == ">=3.8"
    assert config["tool"]["ruff"]["target-version"] == "py38"
    assert "FA" in config["tool"]["ruff"]["lint"]["select"]
    assert config["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]


@pytest.mark.skipif(shutil.which("ruff") is None, reason="ruff is not installed")
def test_ruff_enforces_python_38_future_annotations(tmp_path):
    """Verify that Ruff flags PEP 604 syntax without future annotations under Python 3.8 target."""
    snippet = tmp_path / "snippet.py"
    snippet.write_text("def fn(val: int | None) -> None:\n    pass\n")

    result = subprocess.run(
        ["ruff", "check", str(snippet), "--config", str(PROJECT_ROOT / "pyproject.toml")],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert any(code in result.stdout for code in ("FA100", "FA102", "UP007"))

    # Adding future annotations must resolve the violation
    clean_code = (
        "from __future__ import annotations\n\n\n"
        "def fn(val: int | None) -> None:\n"
        "    pass\n"
    )
    snippet.write_text(clean_code)
    clean_result = subprocess.run(
        ["ruff", "check", str(snippet), "--config", str(PROJECT_ROOT / "pyproject.toml")],
        capture_output=True,
        text=True,
    )
    assert clean_result.returncode == 0
