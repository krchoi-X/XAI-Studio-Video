from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


class IdeaToProductionFixtureTests(unittest.TestCase):
    def test_versioned_contract_fixtures(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        validator = repository / "tests" / "fixtures" / "idea-to-production" / "validate_fixtures.py"
        result = subprocess.run(
            [sys.executable, str(validator)],
            cwd=repository,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
