import datetime
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).parents[1] / "scripts" / "publish_to_meta.py"
spec = importlib.util.spec_from_file_location("publish_to_meta", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PublishDateGuardTests(unittest.TestCase):
    def test_selects_only_taipei_today_ready_post(self):
        calendar = {
            "posts": [
                {"id": "future", "date": "2026-08-28", "status": "ready"},
                {"id": "today", "date": "2026-08-27", "status": "ready"},
            ]
        }
        with patch.object(module, "taipei_today", return_value="2026-08-27"):
            selected = module.find_todays_post(calendar)
        self.assertEqual(selected["id"], "today")

    def test_future_ready_post_is_blocked(self):
        calendar = {"posts": [{"id": "future", "date": "2026-08-28", "status": "ready"}]}
        with patch.object(module, "taipei_today", return_value="2026-08-27"):
            selected = module.find_todays_post(calendar)
        self.assertIsNone(selected)

    def test_yaml_date_object_is_normalized(self):
        self.assertEqual(module.normalize_post_date(datetime.date(2026, 8, 27)), "2026-08-27")
        self.assertEqual(module.normalize_post_date("2026-08-27"), "2026-08-27")
        self.assertIsNone(module.normalize_post_date("not-a-date"))


if __name__ == "__main__":
    unittest.main()
