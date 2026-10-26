from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("deck_projects", WORKSPACE / "scripts" / "deck_projects.py")
PROJECTS = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(PROJECTS)
FIXTURE = WORKSPACE / ".agents" / "skills" / "riftbound-deck-mvp" / "tests" / "fixtures" / "rengar-radiance.json"


class DeckProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=WORKSPACE, prefix=".deck-project-test-")
        self.root = Path(self.temporary.name) / "decks"
        self.deck = PROJECTS.read_json(FIXTURE)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def create(self, project_id: str = "rengar-radiance") -> dict:
        return PROJECTS.create_project(
            projects_root=self.root,
            name="Rengar Radiance",
            deck_path=FIXTURE,
            db_path=PROJECTS.DEFAULT_DB,
            rules_path=PROJECTS.DEFAULT_RULES,
            project_id=project_id,
            metadata={"owner_note": "test"},
        )

    def advance_build(self, project_id: str, target_stage: str) -> None:
        session = PROJECTS.build_status(self.root, project_id)["build_session"]
        current_index = PROJECTS.PIPELINE_STAGES.index(session["current_stage"])
        target_index = PROJECTS.PIPELINE_STAGES.index(target_stage)
        if target_index < current_index:
            PROJECTS.update_build_session(
                projects_root=self.root,
                project_id=project_id,
                stage=target_stage,
                note="Test moved backward",
            )
            return
        for stage in PROJECTS.PIPELINE_STAGES[current_index + 1:target_index + 1]:
            PROJECTS.update_build_session(
                projects_root=self.root,
                project_id=project_id,
                stage=stage,
                note=f"Test advanced to {stage}",
            )

    def test_create_writes_validated_current_and_revision_files(self) -> None:
        result = self.create()
        project = Path(result["project_path"])
        self.assertTrue((project / "deck.json").is_file())
        self.assertTrue((project / "validation.json").is_file())
        self.assertTrue((project / "riftatlas.txt").is_file())
        self.assertTrue((project / "revisions" / "0001" / "revision.json").is_file())
        self.assertIn("Legend:", (project / "riftatlas.txt").read_text(encoding="utf-8"))
        self.assertTrue(result["validation"]["valid"])
        self.assertTrue((self.root / ".data_versions" / result["data_version"] / "cards.sqlite").is_file())
        self.assertEqual(PROJECTS.read_json(project / "build-session.json")["current_stage"], "completed")

    def test_guided_build_persists_stage_state_and_backward_moves(self) -> None:
        started = PROJECTS.start_build_project(
            projects_root=self.root,
            name="Guided Rengar",
            project_id="guided-rengar",
            entry_mode="hero_first",
        )
        project = Path(started["project_path"])
        self.assertEqual(started["current_revision"], 0)
        self.assertEqual(started["current_stage"], "entry")
        self.assertFalse((project / "riftatlas.txt").exists())
        updated = PROJECTS.update_build_session(
            projects_root=self.root,
            project_id="guided-rengar",
            stage="requirements",
            state_patch={"brief": {"hero": "Rengar"}},
            note="Hero-first path confirmed",
        )
        self.assertEqual(updated["current_stage"], "requirements")
        PROJECTS.update_build_session(
            projects_root=self.root,
            project_id="guided-rengar",
            stage="identity",
            state_patch={"identity": {"hero": "Rengar", "legend": "UNL-183"}},
            note="Resolved Legend",
        )
        moved_back = PROJECTS.update_build_session(
            projects_root=self.root,
            project_id="guided-rengar",
            stage="requirements",
            note="Player wants to revise preferences",
        )
        self.assertEqual(moved_back["current_stage"], "requirements")
        self.assertEqual(moved_back["build_session"]["state"]["brief"]["hero"], "Rengar")
        self.assertEqual(len(list((project / "build-history").glob("*.json"))), 3)
        status = PROJECTS.build_status(self.root, "guided-rengar")
        self.assertFalse(status["artifacts"]["riftatlas_txt_exists"])

    def test_guided_build_cannot_skip_forward_or_leave_entry_without_mode(self) -> None:
        PROJECTS.start_build_project(
            projects_root=self.root,
            name="Guided Gates",
            project_id="guided-gates",
        )
        with self.assertRaises(PROJECTS.ProjectError):
            PROJECTS.update_build_session(
                projects_root=self.root,
                project_id="guided-gates",
                stage="requirements",
            )
        with self.assertRaises(PROJECTS.ProjectError):
            PROJECTS.update_build_session(
                projects_root=self.root,
                project_id="guided-gates",
                stage="core_plan",
                entry_mode="undecided",
            )
        result = PROJECTS.update_build_session(
            projects_root=self.root,
            project_id="guided-gates",
            stage="requirements",
            entry_mode="undecided",
        )
        self.assertEqual(result["current_stage"], "requirements")
        self.assertEqual(len(list((self.root / "active" / "guided-gates" / "build-history").glob("*.json"))), 1)

    def test_guided_build_requires_final_stage_then_finalizes(self) -> None:
        PROJECTS.start_build_project(
            projects_root=self.root,
            name="Guided Rengar",
            project_id="guided-rengar",
            entry_mode="hero_first",
        )
        with self.assertRaises(PROJECTS.ProjectError):
            PROJECTS.finalize_build_project(
                projects_root=self.root,
                project_id="guided-rengar",
                deck_path=FIXTURE,
                db_path=PROJECTS.DEFAULT_DB,
                rules_path=PROJECTS.DEFAULT_RULES,
                reason="Too early",
            )
        self.advance_build("guided-rengar", "final_confirmation")
        PROJECTS.update_build_session(
            projects_root=self.root,
            project_id="guided-rengar",
            state_patch={"pending_questions": []},
            note="Player approved complete draft",
        )
        finalized = PROJECTS.finalize_build_project(
            projects_root=self.root,
            project_id="guided-rengar",
            deck_path=FIXTURE,
            db_path=PROJECTS.DEFAULT_DB,
            rules_path=PROJECTS.DEFAULT_RULES,
            reason="Player confirmed",
        )
        self.assertEqual(finalized["current_revision"], 1)
        self.assertEqual(finalized["current_stage"], "completed")
        self.assertTrue(Path(finalized["riftatlas_txt"]).is_file())
        status = PROJECTS.build_status(self.root, "guided-rengar")
        self.assertEqual(status["build_session"]["status"], "completed")
        self.assertTrue(status["validation"]["valid"])

    def test_invalid_guided_finalize_preserves_building_state(self) -> None:
        PROJECTS.start_build_project(
            projects_root=self.root,
            name="Invalid Guided",
            project_id="invalid-guided",
            entry_mode="style_first",
        )
        self.advance_build("invalid-guided", "final_confirmation")
        invalid = copy.deepcopy(self.deck)
        invalid["main_deck"] = []
        invalid_path = Path(self.temporary.name) / "invalid-guided.json"
        invalid_path.write_text(json.dumps(invalid, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(PROJECTS.ProjectError):
            PROJECTS.finalize_build_project(
                projects_root=self.root,
                project_id="invalid-guided",
                deck_path=invalid_path,
                db_path=PROJECTS.DEFAULT_DB,
                rules_path=PROJECTS.DEFAULT_RULES,
                reason="Invalid finalization",
            )
        status = PROJECTS.build_status(self.root, "invalid-guided")
        self.assertEqual(status["lifecycle"], "building")
        self.assertEqual(status["current_revision"], 0)
        self.assertFalse(status["artifacts"]["riftatlas_txt_exists"])

    def test_save_records_strategy_diff_and_preserves_revision(self) -> None:
        self.create()
        revised = copy.deepcopy(self.deck)
        revised["strategy"]["operating_plan"] += " 测试调整。"
        revised_path = Path(self.temporary.name) / "revised.json"
        revised_path.write_text(json.dumps(revised, ensure_ascii=False), encoding="utf-8")
        result = PROJECTS.save_project(
            projects_root=self.root,
            project_id="rengar-radiance",
            deck_path=revised_path,
            db_path=PROJECTS.DEFAULT_DB,
            rules_path=PROJECTS.DEFAULT_RULES,
            reason="Test adjustment",
        )
        self.assertEqual(result["current_revision"], 2)
        self.assertIn("operating_plan", result["revision"]["diff"]["strategy"])
        history = PROJECTS.project_history(self.root, "rengar-radiance")
        self.assertEqual([item["revision"] for item in history], [1, 2])
        original = PROJECTS.read_json(self.root / "active" / "rengar-radiance" / "revisions" / "0001" / "deck.json")
        self.assertEqual(original, self.deck)

    def test_restore_creates_new_revision_instead_of_rewriting_history(self) -> None:
        self.create()
        restored = PROJECTS.restore_revision(
            projects_root=self.root,
            project_id="rengar-radiance",
            revision_number=1,
            db_path=PROJECTS.DEFAULT_DB,
            rules_path=PROJECTS.DEFAULT_RULES,
            reason="Restore baseline",
        )
        self.assertEqual(restored["current_revision"], 2)
        self.assertEqual(restored["revision"]["metadata"]["restored_from_revision"], 1)

    def test_copy_archive_unarchive_and_list(self) -> None:
        self.create()
        PROJECTS.copy_project(
            projects_root=self.root,
            source_id="rengar-radiance",
            name="Rengar Experiment",
            project_id="rengar-experiment",
            db_path=PROJECTS.DEFAULT_DB,
            rules_path=PROJECTS.DEFAULT_RULES,
            reason="Experiment",
        )
        PROJECTS.move_project(self.root, "rengar-experiment", archive=True)
        listed = PROJECTS.list_projects(self.root, include_archived=True)
        status = {item["project_id"]: item["status"] for item in listed}
        self.assertEqual(status["rengar-experiment"], "archived")
        PROJECTS.move_project(self.root, "rengar-experiment", archive=False)
        self.assertTrue((self.root / "active" / "rengar-experiment").is_dir())

    def test_verify_reproduces_saved_output(self) -> None:
        self.create()
        report = PROJECTS.verify_revision(self.root, "rengar-radiance", 1)
        self.assertTrue(report["verified"], report)

    def test_verify_detects_changed_saved_export(self) -> None:
        self.create()
        export = self.root / "active" / "rengar-radiance" / "revisions" / "0001" / "riftatlas.txt"
        export.write_text("not the saved deck\n", encoding="utf-8")
        report = PROJECTS.verify_revision(self.root, "rengar-radiance", 1)
        self.assertFalse(report["verified"], report)
        self.assertFalse(report["checks"]["riftatlas_txt"])

    def test_invalid_deck_is_never_saved(self) -> None:
        invalid = copy.deepcopy(self.deck)
        invalid["main_deck"] = []
        invalid_path = Path(self.temporary.name) / "invalid.json"
        invalid_path.write_text(json.dumps(invalid, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(PROJECTS.ProjectError):
            PROJECTS.create_project(
                projects_root=self.root,
                name="Invalid",
                deck_path=invalid_path,
                db_path=PROJECTS.DEFAULT_DB,
                rules_path=PROJECTS.DEFAULT_RULES,
                project_id="invalid",
            )
        self.assertFalse((self.root / "active" / "invalid").exists())

    def test_cli_create_and_verify_smoke(self) -> None:
        cli = WORKSPACE / "scripts" / "deck_projects.py"
        created = subprocess.run(
            [
                sys.executable,
                str(cli),
                "--projects-root",
                str(self.root),
                "create",
                "--name",
                "Rengar CLI",
                "--project-id",
                "rengar-cli",
                "--deck",
                str(FIXTURE),
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        create_report = json.loads(created.stdout)
        self.assertTrue(Path(create_report["riftatlas_txt"]).is_file())
        verified = subprocess.run(
            [
                sys.executable,
                str(cli),
                "--projects-root",
                str(self.root),
                "verify",
                "rengar-cli",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)
        self.assertTrue(json.loads(verified.stdout)["verified"])

    def test_cli_guided_pipeline_smoke(self) -> None:
        # Exercise CLI stage transport, not the quality of player decisions.
        cli = WORKSPACE / "scripts" / "deck_projects.py"

        def run(*arguments: str) -> dict:
            completed = subprocess.run(
                [sys.executable, str(cli), "--projects-root", str(self.root), *arguments],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            return json.loads(completed.stdout)

        started = run(
            "start-build",
            "--name",
            "Guided CLI",
            "--project-id",
            "guided-cli",
            "--entry-mode",
            "style_first",
        )
        self.assertEqual(started["current_stage"], "entry")
        updated = started
        for stage in PROJECTS.PIPELINE_STAGES[1:-1]:
            updated = run(
                "build-update",
                "guided-cli",
                "--stage",
                stage,
                "--note",
                f"CLI smoke advanced to {stage}",
            )
        self.assertEqual(updated["current_stage"], "final_confirmation")
        finalized = run(
            "finalize-build",
            "guided-cli",
            "--deck",
            str(FIXTURE),
        )
        self.assertEqual(finalized["current_stage"], "completed")
        self.assertTrue(Path(finalized["riftatlas_txt"]).is_file())


if __name__ == "__main__":
    unittest.main()

