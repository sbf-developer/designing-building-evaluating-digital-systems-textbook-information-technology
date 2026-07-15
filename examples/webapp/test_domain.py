import sqlite3
import unittest
from pathlib import Path

from .domain import reschedule_appointment


ROOT = Path(__file__).resolve().parents[1]


def connection_with_seed() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript((ROOT / "sql" / "schema.sql").read_text())
    connection.executescript((ROOT / "sql" / "seed.sql").read_text())
    return connection


class DomainTests(unittest.TestCase):
    def test_success_moves_appointment_and_writes_audit_event(self):
        connection = connection_with_seed()
        outcome = reschedule_appointment(connection, 1, 1, 2)
        self.assertTrue(outcome.is_success)
        statuses = connection.execute(
            "SELECT slot_id, status FROM appointments ORDER BY id"
        ).fetchall()
        self.assertEqual([(1, "cancelled"), (2, "confirmed")], [tuple(row) for row in statuses])
        self.assertEqual(1, connection.execute("SELECT COUNT(*) FROM audit_events").fetchone()[0])

    def test_wrong_owner_cannot_change_appointment(self):
        connection = connection_with_seed()
        outcome = reschedule_appointment(connection, 1, 2, 2)
        self.assertEqual(outcome.status, "not_found")

    def test_occupied_slot_is_a_conflict_and_original_remains(self):
        connection = connection_with_seed()
        connection.execute(
            """
            INSERT INTO appointments (citizen_id, slot_id, status, created_at)
            VALUES (2, 3, 'confirmed', '2099-01-01T09:00:00+00:00')
            """
        )
        connection.commit()
        outcome = reschedule_appointment(connection, 1, 1, 3)
        self.assertEqual(outcome.status, "conflict")
        appointment = connection.execute(
            "SELECT slot_id, status FROM appointments WHERE id = 1"
        ).fetchone()
        self.assertEqual((1, "confirmed"), tuple(appointment))


if __name__ == "__main__":
    unittest.main()
