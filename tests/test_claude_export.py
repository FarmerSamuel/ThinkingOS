"""Sync contract between canonical skill packages and the Claude export."""

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "tools" / "export_claude_skills.py"
OUTPUT_ROOT = ROOT / ".claude" / "skills"
FRONTMATTER = re.compile(r"\A---\nname: (?P<name>[a-z0-9-]+)\ndescription: \"(?P<description>.+)\"\n---\n", re.DOTALL)


def registered_skill_ids() -> set[str]:
    registry = (ROOT / "skills" / "registry.yaml").read_text(encoding="utf-8")
    return set(re.findall(r"(?m)^  - id: ([a-z0-9-]+)$", registry))


class ClaudeExportTests(unittest.TestCase):
    def test_export_is_in_sync_with_canonical_packages(self) -> None:
        result = subprocess.run(
            [sys.executable, str(EXPORTER), "--check"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            "Claude skill export drifted from skills/ packages. "
            "Run `python tools/export_claude_skills.py` and commit.\n"
            + result.stderr,
        )

    def test_every_registered_skill_has_a_claude_package(self) -> None:
        for skill_id in sorted(registered_skill_ids() | {"thinkingos"}):
            with self.subTest(skill=skill_id):
                self.assertTrue((OUTPUT_ROOT / skill_id / "SKILL.md").is_file())

    def test_frontmatter_satisfies_claude_skill_constraints(self) -> None:
        for skill_file in sorted(OUTPUT_ROOT.rglob("SKILL.md")):
            with self.subTest(skill=skill_file.parent.name):
                match = FRONTMATTER.match(skill_file.read_text(encoding="utf-8"))
                self.assertIsNotNone(match, f"{skill_file} has invalid frontmatter")
                name = match.group("name")
                description = match.group("description")
                self.assertEqual(name, skill_file.parent.name)
                self.assertLessEqual(len(name), 64)
                self.assertLessEqual(len(description), 1024)
                self.assertNotIn("\n", description)


if __name__ == "__main__":
    unittest.main()
