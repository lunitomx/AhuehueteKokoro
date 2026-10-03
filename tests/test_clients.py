"""Guest registry (`.kokoro/clients.json`) that replaces `src/kokoro/clients/`.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "runtime"))

import clients  # noqa: E402
from agent_graph import GraphError  # noqa: E402

GUEST = {"name": "Cliente 01", "group": "despachos", "segments": ["contadores"]}


class Registry(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="kokoro-clients-"))
        (self.tmp / ".kokoro").mkdir()
        (self.tmp / ".kokoro" / ".gitignore").write_text("local/\n", encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_missing_registry_is_none(self) -> None:
        self.assertIsNone(clients.load_registry(self.tmp))

    def test_create_and_find(self) -> None:
        created = clients.create_client(self.tmp, GUEST)
        self.assertEqual(created["id"], "cliente-01")
        registry = clients.load_registry(self.tmp)
        assert registry is not None
        self.assertEqual(clients.find_by_name(registry, "CLIENTE")["id"], "cliente-01")
        self.assertIsNone(clients.find_by_name(registry, "otro"))
        self.assertEqual([c["id"] for c in clients.find_by_segment(registry, "Contadores")], ["cliente-01"])
        self.assertEqual(clients.list_groups(registry), ["despachos"])

    def test_duplicate_guest_is_rejected(self) -> None:
        clients.create_client(self.tmp, GUEST)
        with self.assertRaisesRegex(clients.ClientError, "already exists"):
            clients.create_client(self.tmp, GUEST)

    def test_session_log_keeps_newest_twenty(self) -> None:
        clients.create_client(self.tmp, GUEST)
        for number in range(25):
            clients.append_session_log(
                self.tmp,
                "cliente-01",
                {"date": "2026-10-03", "type": "skill", "skill": "kokoro-ads", "summary": f"sesion {number}"},
            )
        log = clients.find_by_id(clients.load_registry(self.tmp) or {}, "cliente-01")["metadata"]["session_log"]
        self.assertEqual(len(log), clients.SESSION_LOG_LIMIT)
        self.assertEqual(log[0]["summary"], "sesion 24")

    def test_session_log_is_reserved_for_append(self) -> None:
        clients.create_client(self.tmp, GUEST)
        with self.assertRaises(clients.ClientError):
            clients.set_metadata(self.tmp, "cliente-01", "session_log", [])
        clients.set_metadata(self.tmp, "cliente-01", "meta_ads", {"account_ref": "act_slug"})

    def test_secret_is_rejected(self) -> None:
        token = "sk-" + "ant-" + "b" * 32
        with self.assertRaises(clients.ClientError):
            clients.create_client(self.tmp, {**GUEST, "description": f"llave {token}"})
        self.assertIsNone(clients.load_registry(self.tmp))

    def test_unknown_and_automatic_fields_are_rejected(self) -> None:
        for extra in ({"phone": "x"}, {"created": "2026-10-03T00:00:00+00:00"}):
            with self.assertRaises(clients.ClientError):
                clients.create_client(self.tmp, {**GUEST, **extra})

    def test_absolute_paths_are_rejected(self) -> None:
        for field, value in (("campaign_folder", "/var/campaigns"), ("repos", ["~/repo"])):
            with self.assertRaises(clients.ClientError, msg=field):
                clients.create_client(self.tmp, {**GUEST, field: value})

    def test_package_checkout_cannot_hold_a_registry(self) -> None:
        with self.assertRaises(GraphError):
            clients.save_registry(REPO_ROOT, clients.create_empty_registry())
        self.assertFalse((REPO_ROOT / ".kokoro" / "clients.json").exists())

    def test_symlinked_kokoro_dir_cannot_redirect_the_registry(self) -> None:
        outside = Path(tempfile.mkdtemp(prefix="kokoro-outside-"))
        self.addCleanup(shutil.rmtree, outside, True)
        (outside / ".gitignore").write_text("local/\n", encoding="utf-8")
        shutil.rmtree(self.tmp / ".kokoro")
        (self.tmp / ".kokoro").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(GraphError):
            clients.create_client(self.tmp, GUEST)
        self.assertFalse((outside / "clients.json").exists())

    def test_cli_round_trip(self) -> None:
        script = REPO_ROOT / "runtime" / "kokoro.py"
        guest_file = self.tmp / "guest.json"
        guest_file.write_text(json.dumps(GUEST), encoding="utf-8")

        def run(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [sys.executable, str(script), "client", *args, "--target", str(self.tmp)],
                capture_output=True, text=True, check=False,
            )

        self.assertEqual(run("create", "--input-file", str(guest_file)).returncode, 0)
        found = run("find", "--name", "cliente")
        self.assertEqual(found.returncode, 0, found.stderr)
        self.assertIn("cliente-01", found.stdout)
        self.assertEqual(run("create", "--input-file", str(guest_file)).returncode, 2)


if __name__ == "__main__":
    unittest.main()
