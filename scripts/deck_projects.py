#!/usr/bin/env python3
"""Manage Riftbound decks as validated, versioned local projects."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import unicodedata
import uuid
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[1]
SKILL_ROOT = WORKSPACE / ".agents" / "skills" / "riftbound-deck-mvp"
RIFTBOUND_PATH = SKILL_ROOT / "scripts" / "riftbound.py"
DEFAULT_PROJECTS_ROOT = WORKSPACE / "decks"


def load_riftbound() -> Any:
    spec = importlib.util.spec_from_file_location("riftbound_deck_mvp", RIFTBOUND_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load Riftbound CLI: {RIFTBOUND_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RIFTBOUND = load_riftbound()
DEFAULT_DB = RIFTBOUND.DEFAULT_DB
DEFAULT_RULES = RIFTBOUND.DEFAULT_RULES
PROJECT_ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
ZONES = ("main_deck", "battlefields", "runes", "sideboard")
PIPELINE_VERSION = 1
PIPELINE_STAGES = (
    "entry",
    "requirements",
    "identity",
    "brief_confirmation",
    "core_plan",
    "deck_skeleton",
    "card_selection",
    "resources",
    "review",
    "final_confirmation",
    "completed",
)
ENTRY_MODES = ("style_first", "hero_first", "undecided", "imported")


class ProjectError(ValueError):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def print_json(value: Any) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(value, ensure_ascii=False, indent=2))


def read_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def atomic_write_text(path: str | Path, content: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.tmp-{uuid.uuid4().hex}")
    try:
        temporary.write_text(content, encoding="utf-8")
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_write_json(path: str | Path, value: Any) -> None:
    atomic_write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def object_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slugify(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.casefold()).strip("-")[:64].strip("-")
    return slug or f"deck-{uuid.uuid4().hex[:8]}"


def validate_project_id(project_id: str) -> str:
    if not PROJECT_ID_RE.fullmatch(project_id):
        raise ProjectError("project ID must contain only lowercase letters, digits, and internal hyphens (max 64)")
    return project_id


def load_metadata(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    value = read_json(path)
    if not isinstance(value, dict):
        raise ProjectError("metadata JSON must contain an object")
    return value


def load_optional_object(path: str | None, label: str) -> dict[str, Any]:
    if not path:
        return {}
    value = read_json(path)
    if not isinstance(value, dict):
        raise ProjectError(f"{label} JSON must contain an object")
    return value


def new_build_session(project_id: str, entry_mode: str | None = None, *, imported: bool = False) -> dict[str, Any]:
    if entry_mode is not None and entry_mode not in ENTRY_MODES:
        raise ProjectError(f"Unsupported entry mode: {entry_mode}")
    timestamp = utc_now()
    stage = "completed" if imported else "entry"
    return {
        "schema_version": 1,
        "pipeline_version": PIPELINE_VERSION,
        "project_id": project_id,
        "status": "completed" if imported else "in_progress",
        "current_stage": stage,
        "entry_mode": "imported" if imported else entry_mode,
        "created_at": timestamp,
        "updated_at": timestamp,
        "state": {
            "brief": {},
            "identity": {},
            "core_plan": {},
            "skeleton": {},
            "draft_deck": {},
            "locked_cards": [],
            "rejected_cards": [],
            "pending_questions": [],
        },
        "stage_history": [{
            "from": None,
            "to": stage,
            "at": timestamp,
            "note": "Imported validated deck" if imported else "Started guided deckbuilding",
        }],
    }


def load_build_session(project: Path) -> dict[str, Any]:
    path = project / "build-session.json"
    if not path.is_file():
        manifest = load_project_manifest(project)
        if int(manifest.get("current_revision", 0)) > 0:
            return new_build_session(manifest["project_id"], imported=True)
        raise ProjectError(f"Missing build session: {path}")
    session = read_json(path)
    if session.get("schema_version") != 1 or session.get("pipeline_version") != PIPELINE_VERSION:
        raise ProjectError(f"Unsupported build-session schema in {path}")
    if session.get("current_stage") not in PIPELINE_STAGES:
        raise ProjectError(f"Unknown build stage in {path}: {session.get('current_stage')}")
    return session


def snapshot_build_session(project: Path, session: dict[str, Any]) -> Path:
    history = project / "build-history"
    history.mkdir(parents=True, exist_ok=True)
    number = len([path for path in history.iterdir() if path.is_file() and path.suffix == ".json"]) + 1
    target = history / f"{number:04d}.json"
    atomic_write_json(target, session)
    return target


def ensure_layout(projects_root: Path) -> None:
    for name in ("active", "archive", ".data_versions"):
        (projects_root / name).mkdir(parents=True, exist_ok=True)


def project_path(projects_root: Path, project_id: str, status: str = "active") -> Path:
    validate_project_id(project_id)
    if status not in {"active", "archive"}:
        raise ProjectError(f"Unsupported project status: {status}")
    return projects_root / status / project_id


def find_project(projects_root: Path, project_id: str, *, active_only: bool = False) -> tuple[Path, str]:
    active = project_path(projects_root, project_id, "active")
    if active.is_dir():
        return active, "active"
    if not active_only:
        archived = project_path(projects_root, project_id, "archive")
        if archived.is_dir():
            return archived, "archived"
    raise ProjectError(f"Deck project not found: {project_id}")


def validate_deck_source(deck_path: str | Path, db_path: str | Path, rules_path: str | Path) -> tuple[dict[str, Any], dict[str, Any], str]:
    deck = RIFTBOUND.read_deck(deck_path)
    connection = RIFTBOUND.connect(db_path)
    try:
        report = RIFTBOUND.validate_deck(deck, connection, RIFTBOUND.load_rules(rules_path))
        if not report["valid"]:
            raise ProjectError("Deck validation failed:\n" + json.dumps(report, ensure_ascii=False, indent=2))
        exported = RIFTBOUND.export_riftatlas(deck, connection, True)
    finally:
        connection.close()
    return deck, report, exported


def ensure_data_version(projects_root: Path, db_path: str | Path, rules_path: str | Path) -> dict[str, Any]:
    database = Path(db_path).resolve()
    rules = Path(rules_path).resolve()
    if not database.is_file() or not rules.is_file():
        raise ProjectError("Card database and rules file must exist before saving a deck project")
    db_hash = file_sha256(database)
    rules_hash = file_sha256(rules)
    version_id = hashlib.sha256(f"{db_hash}:{rules_hash}".encode("ascii")).hexdigest()[:20]
    versions_root = projects_root / ".data_versions"
    versions_root.mkdir(parents=True, exist_ok=True)
    destination = versions_root / version_id
    manifest_source = database.with_suffix(".manifest.json")
    if not destination.exists():
        temporary = versions_root / f".tmp-{version_id}-{uuid.uuid4().hex}"
        temporary.mkdir()
        try:
            shutil.copy2(database, temporary / "cards.sqlite")
            shutil.copy2(rules, temporary / "rules.json")
            manifest: dict[str, Any] | None = None
            if manifest_source.is_file():
                shutil.copy2(manifest_source, temporary / "cards.manifest.json")
                manifest = read_json(manifest_source)
            version = {
                "schema_version": 1,
                "version_id": version_id,
                "created_at": utc_now(),
                "database_sha256": db_hash,
                "rules_sha256": rules_hash,
                "database_manifest": manifest,
                "rules": read_json(rules),
            }
            atomic_write_json(temporary / "version.json", version)
            try:
                os.replace(temporary, destination)
            except FileExistsError:
                shutil.rmtree(temporary)
        finally:
            if temporary.exists():
                shutil.rmtree(temporary)
    version = read_json(destination / "version.json")
    if file_sha256(destination / "cards.sqlite") != version["database_sha256"]:
        raise ProjectError(f"Stored data version is corrupted: {version_id}")
    if file_sha256(destination / "rules.json") != version["rules_sha256"]:
        raise ProjectError(f"Stored rules version is corrupted: {version_id}")
    return version


def quantities(deck: dict[str, Any], zone: str) -> tuple[dict[str, int], list[str]]:
    values: dict[str, int] = {}
    order: list[str] = []
    for entry in deck.get(zone, []):
        code = str(entry["code"]).upper()
        values[code] = values.get(code, 0) + int(entry["quantity"])
        order.append(code)
    return values, order


def deck_diff(before: dict[str, Any] | None, after: dict[str, Any], db_path: str | Path) -> dict[str, Any]:
    previous = before or {}
    connection = RIFTBOUND.connect(db_path)
    try:
        def card_name(code: str) -> str:
            return RIFTBOUND.resolve_card(connection, code)["display_name"]

        fields: dict[str, Any] = {}
        for field in ("name", "rules_profile", "legend", "chosen_champion"):
            old, new = previous.get(field), after.get(field)
            if old != new:
                fields[field] = {"from": old, "to": new}
        strategy_changes: dict[str, Any] = {}
        old_strategy = previous.get("strategy") or {}
        new_strategy = after.get("strategy") or {}
        for field in ("style", "win_condition", "operating_plan", "core_cards"):
            if old_strategy.get(field) != new_strategy.get(field):
                strategy_changes[field] = {"from": old_strategy.get(field), "to": new_strategy.get(field)}
        zone_changes: dict[str, Any] = {}
        for zone in ZONES:
            old_values, old_order = quantities(previous, zone)
            new_values, new_order = quantities(after, zone)
            cards = []
            for code in sorted(set(old_values) | set(new_values)):
                old_quantity = old_values.get(code, 0)
                new_quantity = new_values.get(code, 0)
                if old_quantity != new_quantity:
                    cards.append({
                        "code": code,
                        "name": card_name(code),
                        "from": old_quantity,
                        "to": new_quantity,
                        "delta": new_quantity - old_quantity,
                    })
            if cards or old_order != new_order:
                zone_changes[zone] = {"cards": cards, "order_changed": old_order != new_order}
    finally:
        connection.close()
    return {
        "changed": before is None or canonical_bytes(before) != canonical_bytes(after),
        "fields": fields,
        "strategy": strategy_changes,
        "zones": zone_changes,
    }


def revision_name(number: int) -> str:
    if number < 1:
        raise ProjectError("revision must be a positive integer")
    return f"{number:04d}"


def write_revision_bundle(
    directory: Path,
    *,
    deck: dict[str, Any],
    validation: dict[str, Any],
    exported: str,
    revision: dict[str, Any],
) -> None:
    directory.mkdir(parents=True, exist_ok=False)
    atomic_write_json(directory / "deck.json", deck)
    atomic_write_json(directory / "validation.json", validation)
    atomic_write_text(directory / "riftatlas.txt", exported)
    atomic_write_json(directory / "revision.json", revision)


def write_current_files(project: Path, deck: dict[str, Any], validation: dict[str, Any], exported: str) -> None:
    atomic_write_json(project / "deck.json", deck)
    atomic_write_json(project / "validation.json", validation)
    atomic_write_text(project / "riftatlas.txt", exported)


def project_result(project: Path, manifest: dict[str, Any], status: str) -> dict[str, Any]:
    session_path = project / "build-session.json"
    stage = None
    if session_path.is_file():
        stage = read_json(session_path).get("current_stage")
    elif int(manifest.get("current_revision", 0)) > 0:
        stage = "completed"
    return {
        "project_id": manifest["project_id"],
        "name": manifest["name"],
        "status": status,
        "lifecycle": manifest.get("lifecycle", "ready" if int(manifest.get("current_revision", 0)) > 0 else "building"),
        "current_stage": stage,
        "current_revision": manifest["current_revision"],
        "project_path": str(project.resolve()),
        "build_session_json": str(session_path.resolve()),
        "deck_json": str((project / "deck.json").resolve()),
        "validation_json": str((project / "validation.json").resolve()),
        "riftatlas_txt": str((project / "riftatlas.txt").resolve()),
    }


def create_project(
    *,
    projects_root: Path,
    name: str,
    deck_path: str | Path,
    db_path: str | Path,
    rules_path: str | Path,
    project_id: str | None = None,
    reason: str = "Initial deck project",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ensure_layout(projects_root)
    identifier = validate_project_id(project_id or slugify(name))
    target = project_path(projects_root, identifier, "active")
    archived = project_path(projects_root, identifier, "archive")
    if target.exists() or archived.exists():
        raise ProjectError(f"Deck project ID already exists: {identifier}")
    deck, validation, exported = validate_deck_source(deck_path, db_path, rules_path)
    data_version = ensure_data_version(projects_root, db_path, rules_path)
    timestamp = utc_now()
    revision = {
        "schema_version": 1,
        "revision": 1,
        "parent_revision": None,
        "created_at": timestamp,
        "reason": reason,
        "metadata": metadata or {},
        "deck_sha256": object_sha256(deck),
        "data_version": data_version["version_id"],
        "rules_profile": validation["rules_profile"],
        "rules_as_of": validation["rules_as_of"],
        "diff": deck_diff(None, deck, db_path),
    }
    manifest = {
        "schema_version": 1,
        "project_id": identifier,
        "name": name,
        "status": "active",
        "lifecycle": "ready",
        "created_at": timestamp,
        "updated_at": timestamp,
        "current_revision": 1,
        "metadata": metadata or {},
        "files": {
            "deck": "deck.json",
            "validation": "validation.json",
            "riftatlas": "riftatlas.txt",
            "revisions": "revisions",
            "build_session": "build-session.json",
        },
    }
    temporary = projects_root / "active" / f".tmp-{identifier}-{uuid.uuid4().hex}"
    temporary.mkdir()
    try:
        write_current_files(temporary, deck, validation, exported)
        write_revision_bundle(
            temporary / "revisions" / revision_name(1),
            deck=deck,
            validation=validation,
            exported=exported,
            revision=revision,
        )
        atomic_write_json(temporary / "build-session.json", new_build_session(identifier, imported=True))
        atomic_write_json(temporary / "project.json", manifest)
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    result = project_result(target, manifest, "active")
    result["validation"] = validation
    result["data_version"] = data_version["version_id"]
    return result


def load_project_manifest(project: Path) -> dict[str, Any]:
    manifest = read_json(project / "project.json")
    if manifest.get("schema_version") != 1:
        raise ProjectError(f"Unsupported project schema in {project}")
    return manifest


def start_build_project(
    *,
    projects_root: Path,
    name: str,
    project_id: str | None = None,
    entry_mode: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ensure_layout(projects_root)
    identifier = validate_project_id(project_id or slugify(name))
    target = project_path(projects_root, identifier, "active")
    archived = project_path(projects_root, identifier, "archive")
    if target.exists() or archived.exists():
        raise ProjectError(f"Deck project ID already exists: {identifier}")
    timestamp = utc_now()
    manifest = {
        "schema_version": 1,
        "project_id": identifier,
        "name": name,
        "status": "active",
        "lifecycle": "building",
        "created_at": timestamp,
        "updated_at": timestamp,
        "current_revision": 0,
        "metadata": metadata or {},
        "files": {
            "deck": "deck.json",
            "validation": "validation.json",
            "riftatlas": "riftatlas.txt",
            "revisions": "revisions",
            "build_session": "build-session.json",
            "build_history": "build-history",
        },
    }
    session = new_build_session(identifier, entry_mode)
    temporary = projects_root / "active" / f".tmp-{identifier}-{uuid.uuid4().hex}"
    temporary.mkdir()
    try:
        (temporary / "revisions").mkdir()
        (temporary / "build-history").mkdir()
        atomic_write_json(temporary / "build-session.json", session)
        atomic_write_json(temporary / "project.json", manifest)
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    result = project_result(target, manifest, "active")
    result["build_session"] = session
    return result


def update_build_session(
    *,
    projects_root: Path,
    project_id: str,
    stage: str | None = None,
    entry_mode: str | None = None,
    state_patch: dict[str, Any] | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    project, _ = find_project(projects_root, project_id, active_only=True)
    manifest = load_project_manifest(project)
    if manifest.get("lifecycle", "ready" if int(manifest.get("current_revision", 0)) > 0 else "building") != "building":
        raise ProjectError("Build session is already finalized; create a deck revision instead")
    session = load_build_session(project)
    if session["status"] != "in_progress":
        raise ProjectError("Build session is not in progress")
    if stage == "completed":
        raise ProjectError("Only finalize-build can move a session to completed")
    if stage is not None and stage not in PIPELINE_STAGES:
        raise ProjectError(f"Unsupported build stage: {stage}")
    if entry_mode is not None and entry_mode not in ENTRY_MODES[:-1]:
        raise ProjectError(f"Unsupported guided entry mode: {entry_mode}")
    if stage is None and entry_mode is None and not state_patch:
        raise ProjectError("No build-session update was supplied")
    previous_stage = session["current_stage"]
    if stage is not None and stage != previous_stage:
        previous_index = PIPELINE_STAGES.index(previous_stage)
        next_index = PIPELINE_STAGES.index(stage)
        if next_index > previous_index + 1:
            raise ProjectError(
                f"Cannot skip guided-build stages: {previous_stage} -> {stage}; next is {PIPELINE_STAGES[previous_index + 1]}"
            )
        if previous_stage == "entry" and stage == "requirements" and (entry_mode or session.get("entry_mode")) is None:
            raise ProjectError("Choose style_first, hero_first, or undecided before leaving entry")
    snapshot = snapshot_build_session(project, session)
    timestamp = utc_now()
    if entry_mode is not None:
        session["entry_mode"] = entry_mode
    if state_patch:
        session["state"].update(state_patch)
    if stage is not None and stage != previous_stage:
        session["current_stage"] = stage
        session["stage_history"].append({
            "from": previous_stage,
            "to": stage,
            "at": timestamp,
            "note": note or "",
        })
    session["updated_at"] = timestamp
    manifest["updated_at"] = timestamp
    atomic_write_json(project / "build-session.json", session)
    atomic_write_json(project / "project.json", manifest)
    return {
        "project_id": project_id,
        "lifecycle": "building",
        "current_stage": session["current_stage"],
        "entry_mode": session["entry_mode"],
        "snapshot": str(snapshot.resolve()),
        "build_session": session,
    }


def build_status(projects_root: Path, project_id: str) -> dict[str, Any]:
    project, status = find_project(projects_root, project_id)
    manifest = load_project_manifest(project)
    result = project_result(project, manifest, status)
    result["build_session"] = load_build_session(project)
    result["artifacts"] = {
        "deck_json_exists": (project / "deck.json").is_file(),
        "validation_json_exists": (project / "validation.json").is_file(),
        "riftatlas_txt_exists": (project / "riftatlas.txt").is_file(),
    }
    result["validation"] = read_json(project / "validation.json") if (project / "validation.json").is_file() else None
    return result


def finalize_build_project(
    *,
    projects_root: Path,
    project_id: str,
    deck_path: str | Path,
    db_path: str | Path,
    rules_path: str | Path,
    reason: str,
) -> dict[str, Any]:
    project, _ = find_project(projects_root, project_id, active_only=True)
    manifest = load_project_manifest(project)
    if manifest.get("lifecycle") != "building" or int(manifest.get("current_revision", 0)) != 0:
        raise ProjectError("Project is not an unfinished guided build")
    session = load_build_session(project)
    if session["current_stage"] != "final_confirmation":
        raise ProjectError("Move the build session to final_confirmation after player approval before finalizing")
    deck, validation, exported = validate_deck_source(deck_path, db_path, rules_path)
    data_version = ensure_data_version(projects_root, db_path, rules_path)
    timestamp = utc_now()
    revision = {
        "schema_version": 1,
        "revision": 1,
        "parent_revision": None,
        "created_at": timestamp,
        "reason": reason,
        "metadata": {"pipeline_version": PIPELINE_VERSION},
        "deck_sha256": object_sha256(deck),
        "data_version": data_version["version_id"],
        "rules_profile": validation["rules_profile"],
        "rules_as_of": validation["rules_as_of"],
        "diff": deck_diff(None, deck, db_path),
    }
    revision_target = project / "revisions" / revision_name(1)
    if revision_target.exists():
        raise ProjectError("Initial revision already exists")
    snapshot_build_session(project, session)
    write_revision_bundle(
        revision_target,
        deck=deck,
        validation=validation,
        exported=exported,
        revision=revision,
    )
    write_current_files(project, deck, validation, exported)
    session["status"] = "completed"
    session["current_stage"] = "completed"
    session["updated_at"] = timestamp
    session["stage_history"].append({
        "from": "final_confirmation",
        "to": "completed",
        "at": timestamp,
        "note": reason,
    })
    manifest["lifecycle"] = "ready"
    manifest["current_revision"] = 1
    manifest["updated_at"] = timestamp
    atomic_write_json(project / "build-session.json", session)
    atomic_write_json(project / "project.json", manifest)
    result = project_result(project, manifest, "active")
    result["validation"] = validation
    result["revision"] = revision
    result["data_version"] = data_version["version_id"]
    return result


def save_project(
    *,
    projects_root: Path,
    project_id: str,
    deck_path: str | Path,
    db_path: str | Path,
    rules_path: str | Path,
    reason: str,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    project, _ = find_project(projects_root, project_id, active_only=True)
    manifest = load_project_manifest(project)
    if int(manifest.get("current_revision", 0)) < 1:
        raise ProjectError("Guided build has no validated deck yet; use finalize-build first")
    previous = read_json(project / "deck.json")
    deck, validation, exported = validate_deck_source(deck_path, db_path, rules_path)
    data_version = ensure_data_version(projects_root, db_path, rules_path)
    parent = int(manifest["current_revision"])
    number = parent + 1
    timestamp = utc_now()
    revision = {
        "schema_version": 1,
        "revision": number,
        "parent_revision": parent,
        "created_at": timestamp,
        "reason": reason,
        "metadata": metadata or {},
        "deck_sha256": object_sha256(deck),
        "data_version": data_version["version_id"],
        "rules_profile": validation["rules_profile"],
        "rules_as_of": validation["rules_as_of"],
        "diff": deck_diff(previous, deck, db_path),
    }
    revision_target = project / "revisions" / revision_name(number)
    if revision_target.exists():
        raise ProjectError(f"Revision already exists: {number}")
    write_revision_bundle(
        revision_target,
        deck=deck,
        validation=validation,
        exported=exported,
        revision=revision,
    )
    write_current_files(project, deck, validation, exported)
    manifest["current_revision"] = number
    manifest["lifecycle"] = "ready"
    manifest["updated_at"] = timestamp
    atomic_write_json(project / "project.json", manifest)
    result = project_result(project, manifest, "active")
    result["revision"] = revision
    result["validation"] = validation
    return result


def list_projects(projects_root: Path, include_archived: bool) -> list[dict[str, Any]]:
    statuses = (("active", "active"), ("archive", "archived")) if include_archived else (("active", "active"),)
    output = []
    for directory_name, status in statuses:
        parent = projects_root / directory_name
        if not parent.exists():
            continue
        for child in sorted(parent.iterdir(), key=lambda path: path.name):
            if not child.is_dir() or child.name.startswith(".") or not (child / "project.json").is_file():
                continue
            manifest = load_project_manifest(child)
            session_path = child / "build-session.json"
            current_stage = read_json(session_path).get("current_stage") if session_path.is_file() else (
                "completed" if int(manifest.get("current_revision", 0)) > 0 else None
            )
            output.append({
                "project_id": manifest["project_id"],
                "name": manifest["name"],
                "status": status,
                "lifecycle": manifest.get("lifecycle", "ready" if int(manifest.get("current_revision", 0)) > 0 else "building"),
                "current_stage": current_stage,
                "current_revision": manifest["current_revision"],
                "updated_at": manifest["updated_at"],
                "riftatlas_txt": str((child / "riftatlas.txt").resolve()) if (child / "riftatlas.txt").is_file() else None,
            })
    return output


def show_project(projects_root: Path, project_id: str) -> dict[str, Any]:
    project, status = find_project(projects_root, project_id)
    manifest = load_project_manifest(project)
    output = project_result(project, manifest, status)
    output["metadata"] = manifest.get("metadata", {})
    output["build_session"] = load_build_session(project)
    output["strategy"] = read_json(project / "deck.json").get("strategy", {}) if (project / "deck.json").is_file() else None
    output["validation"] = read_json(project / "validation.json") if (project / "validation.json").is_file() else None
    return output


def project_history(projects_root: Path, project_id: str) -> list[dict[str, Any]]:
    project, _ = find_project(projects_root, project_id)
    revisions = project / "revisions"
    if not revisions.is_dir():
        return []
    return [read_json(path / "revision.json") for path in sorted(revisions.iterdir()) if path.is_dir()]


def restore_revision(
    *,
    projects_root: Path,
    project_id: str,
    revision_number: int,
    db_path: str | Path,
    rules_path: str | Path,
    reason: str,
) -> dict[str, Any]:
    project, _ = find_project(projects_root, project_id, active_only=True)
    source = project / "revisions" / revision_name(revision_number) / "deck.json"
    if not source.is_file():
        raise ProjectError(f"Revision not found: {revision_number}")
    return save_project(
        projects_root=projects_root,
        project_id=project_id,
        deck_path=source,
        db_path=db_path,
        rules_path=rules_path,
        reason=reason,
        metadata={"restored_from_revision": revision_number},
    )


def copy_project(
    *,
    projects_root: Path,
    source_id: str,
    name: str,
    project_id: str | None,
    db_path: str | Path,
    rules_path: str | Path,
    reason: str,
) -> dict[str, Any]:
    source, _ = find_project(projects_root, source_id)
    source_manifest = load_project_manifest(source)
    if int(source_manifest.get("current_revision", 0)) < 1 or not (source / "deck.json").is_file():
        raise ProjectError("Cannot copy an unfinished guided build")
    return create_project(
        projects_root=projects_root,
        name=name,
        deck_path=source / "deck.json",
        db_path=db_path,
        rules_path=rules_path,
        project_id=project_id,
        reason=reason,
        metadata={
            "copied_from": source_manifest["project_id"],
            "copied_from_revision": source_manifest["current_revision"],
        },
    )


def move_project(projects_root: Path, project_id: str, *, archive: bool) -> dict[str, Any]:
    source_status = "active" if archive else "archive"
    destination_status = "archive" if archive else "active"
    source = project_path(projects_root, project_id, source_status)
    destination = project_path(projects_root, project_id, destination_status)
    if not source.is_dir():
        action = "archive" if archive else "unarchive"
        raise ProjectError(f"Cannot {action}; project is not in {source_status}: {project_id}")
    if destination.exists():
        raise ProjectError(f"Destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))
    manifest = load_project_manifest(destination)
    manifest["status"] = "archived" if archive else "active"
    manifest["updated_at"] = utc_now()
    atomic_write_json(destination / "project.json", manifest)
    return project_result(destination, manifest, manifest["status"])


def verify_revision(projects_root: Path, project_id: str, revision_number: int | None) -> dict[str, Any]:
    project, status = find_project(projects_root, project_id)
    manifest = load_project_manifest(project)
    number = revision_number or int(manifest["current_revision"])
    if number < 1:
        raise ProjectError("Project has no validated revision to verify")
    revision_dir = project / "revisions" / revision_name(number)
    if not revision_dir.is_dir():
        raise ProjectError(f"Revision not found: {number}")
    revision = read_json(revision_dir / "revision.json")
    data_root = projects_root / ".data_versions" / revision["data_version"]
    if not data_root.is_dir():
        raise ProjectError(f"Data version not found: {revision['data_version']}")
    deck, report, exported = validate_deck_source(
        revision_dir / "deck.json",
        data_root / "cards.sqlite",
        data_root / "rules.json",
    )
    saved_report = read_json(revision_dir / "validation.json")
    saved_export = (revision_dir / "riftatlas.txt").read_text(encoding="utf-8")
    checks = {
        "deck_hash": object_sha256(deck) == revision["deck_sha256"],
        "validation_report": report == saved_report,
        "riftatlas_txt": exported == saved_export,
    }
    return {
        "project_id": project_id,
        "status": status,
        "revision": number,
        "data_version": revision["data_version"],
        "verified": all(checks.values()),
        "checks": checks,
        "rules_as_of": report["rules_as_of"],
    }


def cmd_create(args: argparse.Namespace) -> int:
    print_json(create_project(
        projects_root=Path(args.projects_root),
        name=args.name,
        deck_path=args.deck,
        db_path=args.db,
        rules_path=args.rules,
        project_id=args.project_id,
        reason=args.reason,
        metadata=load_metadata(args.metadata),
    ))
    return 0


def cmd_start_build(args: argparse.Namespace) -> int:
    print_json(start_build_project(
        projects_root=Path(args.projects_root),
        name=args.name,
        project_id=args.project_id,
        entry_mode=args.entry_mode,
        metadata=load_metadata(args.metadata),
    ))
    return 0


def cmd_build_update(args: argparse.Namespace) -> int:
    print_json(update_build_session(
        projects_root=Path(args.projects_root),
        project_id=args.project,
        stage=args.stage,
        entry_mode=args.entry_mode,
        state_patch=load_optional_object(args.state, "build state") if args.state else None,
        note=args.note,
    ))
    return 0


def cmd_build_status(args: argparse.Namespace) -> int:
    print_json(build_status(Path(args.projects_root), args.project))
    return 0


def cmd_finalize_build(args: argparse.Namespace) -> int:
    print_json(finalize_build_project(
        projects_root=Path(args.projects_root),
        project_id=args.project,
        deck_path=args.deck,
        db_path=args.db,
        rules_path=args.rules,
        reason=args.reason,
    ))
    return 0


def cmd_save(args: argparse.Namespace) -> int:
    print_json(save_project(
        projects_root=Path(args.projects_root),
        project_id=args.project,
        deck_path=args.deck,
        db_path=args.db,
        rules_path=args.rules,
        reason=args.reason,
        metadata=load_metadata(args.metadata),
    ))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    print_json(list_projects(Path(args.projects_root), args.include_archived))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    print_json(show_project(Path(args.projects_root), args.project))
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    print_json(project_history(Path(args.projects_root), args.project))
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    print_json(restore_revision(
        projects_root=Path(args.projects_root),
        project_id=args.project,
        revision_number=args.revision,
        db_path=args.db,
        rules_path=args.rules,
        reason=args.reason,
    ))
    return 0


def cmd_copy(args: argparse.Namespace) -> int:
    print_json(copy_project(
        projects_root=Path(args.projects_root),
        source_id=args.source,
        name=args.name,
        project_id=args.project_id,
        db_path=args.db,
        rules_path=args.rules,
        reason=args.reason,
    ))
    return 0


def cmd_archive(args: argparse.Namespace) -> int:
    print_json(move_project(Path(args.projects_root), args.project, archive=True))
    return 0


def cmd_unarchive(args: argparse.Namespace) -> int:
    print_json(move_project(Path(args.projects_root), args.project, archive=False))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    report = verify_revision(Path(args.projects_root), args.project, args.revision)
    print_json(report)
    return 0 if report["verified"] else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--projects-root", default=str(DEFAULT_PROJECTS_ROOT), help="Root directory for deck projects")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Current cards.sqlite used for new revisions")
    parser.add_argument("--rules", default=str(DEFAULT_RULES), help="Current rules JSON used for new revisions")
    commands = parser.add_subparsers(dest="command", required=True)

    create = commands.add_parser("create", help="Create a validated deck project")
    create.add_argument("--name", required=True)
    create.add_argument("--deck", required=True)
    create.add_argument("--project-id")
    create.add_argument("--reason", default="Initial deck project")
    create.add_argument("--metadata", help="Optional JSON object stored with the project and first revision")
    create.set_defaults(func=cmd_create)

    start_build = commands.add_parser("start-build", help="Start a resumable guided deckbuilding project")
    start_build.add_argument("--name", required=True)
    start_build.add_argument("--project-id")
    start_build.add_argument("--entry-mode", choices=ENTRY_MODES[:-1])
    start_build.add_argument("--metadata", help="Optional JSON object stored with the project")
    start_build.set_defaults(func=cmd_start_build)

    build_update = commands.add_parser("build-update", help="Record guided-build state or move to another stage")
    build_update.add_argument("project")
    build_update.add_argument("--stage", choices=PIPELINE_STAGES[:-1])
    build_update.add_argument("--entry-mode", choices=ENTRY_MODES[:-1])
    build_update.add_argument("--state", help="JSON object merged into build-session state")
    build_update.add_argument("--note")
    build_update.set_defaults(func=cmd_build_update)

    build_status_parser = commands.add_parser("build-status", help="Show resumable guided-build state")
    build_status_parser.add_argument("project")
    build_status_parser.set_defaults(func=cmd_build_status)

    finalize_build = commands.add_parser("finalize-build", help="Validate and finalize a confirmed guided build")
    finalize_build.add_argument("project")
    finalize_build.add_argument("--deck", required=True)
    finalize_build.add_argument("--reason", default="Completed guided deckbuilding pipeline")
    finalize_build.set_defaults(func=cmd_finalize_build)

    save = commands.add_parser("save", help="Validate and save a new project revision")
    save.add_argument("project")
    save.add_argument("--deck", required=True)
    save.add_argument("--reason", required=True)
    save.add_argument("--metadata", help="Optional JSON object stored with this revision")
    save.set_defaults(func=cmd_save)

    listing = commands.add_parser("list", help="List deck projects")
    listing.add_argument("--include-archived", action="store_true")
    listing.set_defaults(func=cmd_list)

    show = commands.add_parser("show", aliases=["open"], help="Show one project and its artifact paths")
    show.add_argument("project")
    show.set_defaults(func=cmd_show)

    history = commands.add_parser("history", help="Show immutable revision history")
    history.add_argument("project")
    history.set_defaults(func=cmd_history)

    restore = commands.add_parser("restore", help="Restore an old revision as a new validated revision")
    restore.add_argument("project")
    restore.add_argument("revision", type=int)
    restore.add_argument("--reason", required=True)
    restore.set_defaults(func=cmd_restore)

    copy_parser = commands.add_parser("copy", help="Copy the current deck into a new project")
    copy_parser.add_argument("source")
    copy_parser.add_argument("--name", required=True)
    copy_parser.add_argument("--project-id")
    copy_parser.add_argument("--reason", default="Copied deck project")
    copy_parser.set_defaults(func=cmd_copy)

    archive = commands.add_parser("archive", help="Move an active project into the archive")
    archive.add_argument("project")
    archive.set_defaults(func=cmd_archive)

    unarchive = commands.add_parser("unarchive", help="Restore an archived project")
    unarchive.add_argument("project")
    unarchive.set_defaults(func=cmd_unarchive)

    verify = commands.add_parser("verify", help="Reproduce a revision with its saved cards and rules data")
    verify.add_argument("project")
    verify.add_argument("--revision", type=int)
    verify.set_defaults(func=cmd_verify)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (OSError, ProjectError, json.JSONDecodeError) as error:
        print_json({"ok": False, "error": str(error)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
