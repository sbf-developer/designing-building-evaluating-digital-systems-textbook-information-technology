import tempfile
import unittest
from pathlib import Path

try:
    from flask import Flask
    from .app import create_app
except ImportError:  # pragma: no cover - environment without optional web dependency
    Flask = None
    create_app = None


class AppTests(unittest.TestCase):
    @unittest.skipIf(Flask is None, "install examples/webapp/requirements.txt")
    def test_api_requires_integer_slot(self):
        with tempfile.TemporaryDirectory() as directory:
            app = create_app({
                "TESTING": True,
                "DATABASE": str(Path(directory) / "test.sqlite3"),
            })
            with app.app_context():
                app.test_cli_runner().invoke(args=["init-db"])
            client = app.test_client()
            response = client.post("/api/appointments/1/reschedule", json={"slot_id": "2"})
            self.assertEqual(response.status_code, 400)

    @unittest.skipIf(Flask is None, "install examples/webapp/requirements.txt")
    def test_api_reschedules_seeded_appointment(self):
        with tempfile.TemporaryDirectory() as directory:
            app = create_app({
                "TESTING": True,
                "DATABASE": str(Path(directory) / "test.sqlite3"),
            })
            with app.app_context():
                app.test_cli_runner().invoke(args=["init-db"])
            response = app.test_client().post(
                "/api/appointments/1/reschedule", json={"slot_id": 2}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["status"], "rescheduled")


if __name__ == "__main__":
    unittest.main()
