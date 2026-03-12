import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cat_updater import CatUpdateError, update_cat_record


class TestCatUpdater(unittest.TestCase):
    def test_update_cat_record_merges_values(self):
        current = {"id": "cat-1", "name": "Mochi", "age": 4}
        updates = {"name": "Mochi II", "favorite_food": "salmon"}

        updated = update_cat_record(current, updates)

        self.assertEqual(
            updated,
            {
                "id": "cat-1",
                "name": "Mochi II",
                "age": 4,
                "favorite_food": "salmon",
            },
        )

    def test_update_cat_record_rejects_immutable_changes(self):
        with self.assertRaisesRegex(CatUpdateError, 'field "id" is immutable'):
            update_cat_record({"id": "cat-1", "name": "Mochi"}, {"id": "cat-2"})

    def test_update_cat_record_removes_field_when_value_is_none(self):
        updated = update_cat_record({"name": "Mochi", "chip": "X1"}, {"chip": None})
        self.assertEqual(updated, {"name": "Mochi"})

    def test_cli_outputs_updated_record(self):
        with self.subTest("cli output"):
            with TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                current_path = tmp_path / "current.json"
                updates_path = tmp_path / "updates.json"

                current_path.write_text(json.dumps({"id": "cat-9", "name": "Luna"}), encoding="utf-8")
                updates_path.write_text(json.dumps({"name": "Nova"}), encoding="utf-8")

                proc = subprocess.run(
                    [sys.executable, "cat_updater.py", str(current_path), str(updates_path)],
                    check=True,
                    cwd=Path(__file__).resolve().parents[1],
                    capture_output=True,
                    text=True,
                )

                self.assertEqual(json.loads(proc.stdout), {"id": "cat-9", "name": "Nova"})


if __name__ == "__main__":
    unittest.main()
