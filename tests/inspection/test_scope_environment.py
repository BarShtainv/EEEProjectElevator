"""Deterministic SP-06.9 repository-boundary inspections."""

from __future__ import annotations

import ast
from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src" / "elevator_access_sim"
DOCUMENTS = ROOT / "docs"
TITLE = "Literature-Based Engineering Analysis and Software Simulation of a 16-Floor Dual-Frequency RFID Elevator Access-Control Controller"


def _python_trees() -> dict[Path, ast.Module]:
    return {
        path: ast.parse(path.read_text(encoding="utf-8"), filename=str(path.relative_to(ROOT)))
        for path in sorted(SOURCE.glob("*.py"))
    }


def _import_roots(tree: ast.Module) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def _assigned_self_attributes(tree: ast.Module) -> set[str]:
    assigned: set[str] = set()
    for node in ast.walk(tree):
        targets: list[ast.expr] = []
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = list(node.targets) if isinstance(node, ast.Assign) else [node.target]
        elif isinstance(node, ast.AugAssign):
            targets = [node.target]
        for target in targets:
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
            ):
                assigned.add(target.attr)
    return assigned


def test_tst_rev_001_working_title_and_approval_boundary() -> None:
    requirements = (DOCUMENTS / "requirements.md").read_text(encoding="utf-8")
    architecture = (DOCUMENTS / "architecture.md").read_text(encoding="utf-8")
    decisions = (DOCUMENTS / "decision_log.md").read_text(encoding="utf-8")
    for text in (requirements, architecture, decisions):
        assert TITLE in text
        assert "supervisor approval" in text.lower()
        assert "pending" in text.lower()


def test_tst_scp_001_002_003_scope_and_optional_change_control() -> None:
    trees = _python_trees()
    forbidden_imports = {
        "RPi",
        "gpiozero",
        "serial",
        "socket",
        "sqlite3",
        "tkinter",
        "asyncio",
        "threading",
    }
    assert not set().union(*(_import_roots(tree) for tree in trees.values())) & forbidden_imports

    requirements = (DOCUMENTS / "requirements.md").read_text(encoding="utf-8").lower()
    decisions = (DOCUMENTS / "decision_log.md").read_text(encoding="utf-8").lower()
    sequence = (DOCUMENTS / "implementation_sequence.md").read_text(encoding="utf-8").lower()
    software_design = (DOCUMENTS / "software_design.md").read_text(encoding="utf-8").lower()
    assert "access-authorization layer" in requirements
    assert "optional requirements" in software_design and "cannot gate the mvp" in software_design
    assert "task 10" in sequence and "task 11" in sequence
    assert "physical integration" in decisions and "supervisor approval" in decisions


def test_tst_nfr_002_single_mutable_state_owners_and_thin_cli() -> None:
    trees = _python_trees()
    owners = {
        "_next_sequence": "event_log.py",
        "_snapshot": "outputs.py",
        "_index": "credentials.py",
        "_next_heartbeat": "watchdog.py",
        "_deadline": "watchdog.py",
        "_last_service": "watchdog.py",
    }
    for attribute, expected_owner in owners.items():
        actual = {
            path.name
            for path, tree in trees.items()
            if attribute in _assigned_self_attributes(tree)
        }
        assert actual == {expected_owner}

    cli = (SOURCE / "cli.py").read_text(encoding="utf-8")
    assert "Controller(" in cli
    assert "load_startup_files(" in cli
    assert "floor_mask" not in cli
    assert "validate_frame" not in cli
    assert "authorize(" not in cli


def test_tst_env_001_002_003_004_offline_dependency_and_runner_boundary() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert metadata["project"]["requires-python"] == ">=3.11"
    assert metadata["project"]["dependencies"] == []
    assert metadata["project"]["optional-dependencies"]["test"] == ["pytest>=7"]
    assert metadata["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]

    imports = set().union(*(_import_roots(tree) for tree in _python_trees().values()))
    assert not imports & {"requests", "httpx", "serial", "RPi", "gpiozero", "sqlite3"}
    assert not any(
        path.is_dir()
        for name in (".venv", "venv", "env")
        if (path := ROOT / name).exists()
    )


def test_tst_rep_003_utf8_and_repository_relative_internal_paths() -> None:
    authored = [ROOT / "pyproject.toml"]
    for directory in (SOURCE, DOCUMENTS, ROOT / "tests"):
        authored.extend(path for path in directory.rglob("*") if path.is_file() and path.suffix in {".py", ".md", ".csv"})
    for path in authored:
        path.read_bytes().decode("utf-8", errors="strict")

    for csv_path in DOCUMENTS.glob("*.csv"):
        text = csv_path.read_text(encoding="utf-8")
        assert "C:\\" not in text
        assert "/mnt/" not in text
        assert "/home/" not in text


def test_tst_lim_001_002_003_004_contextual_claim_boundaries() -> None:
    requirements = (DOCUMENTS / "requirements.md").read_text(encoding="utf-8").lower()
    architecture = (DOCUMENTS / "architecture.md").read_text(encoding="utf-8").lower()
    software_design = (DOCUMENTS / "software_design.md").read_text(encoding="utf-8").lower()

    assert "proposed project-model requirement" in requirements
    assert "logical outputs" in architecture
    assert "logical `lf`/`hf`" in architecture
    assert "simulated time" in software_design
    assert "software-only" in requirements
    assert software_design.startswith("# python software model design")
    assert "does not describe verified commercial-product behavior" in requirements
    assert "no physical-control interface" in requirements

    production_names = {path.name.lower() for path in SOURCE.glob("*.py")}
    forbidden_adapter_names = {"gpio.py", "relay.py", "serial_reader.py", "network.py", "database.py", "gui.py", "hardware_watchdog.py"}
    assert production_names.isdisjoint(forbidden_adapter_names)
