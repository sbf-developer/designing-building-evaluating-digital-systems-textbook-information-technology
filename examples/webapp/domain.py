"""Domain service for the CivicQueue example."""

from dataclasses import dataclass
import sqlite3


@dataclass(frozen=True)
class Outcome:
    status: str
    appointment_id: int | None = None
    message: str = ""

    @property
    def is_success(self) -> bool:
        return self.status == "success"


def reschedule_appointment(
    connection: sqlite3.Connection,
    appointment_id: int,
    citizen_id: int,
    new_slot_id: int,
) -> Outcome:
    """Move an owned confirmed appointment in one transaction.

    The database uniqueness constraint is the final arbiter of slot ownership.
    """
    try:
        connection.execute("BEGIN IMMEDIATE")
        current = connection.execute(
            """
            SELECT a.id, a.slot_id
            FROM appointments AS a
            WHERE a.id = ? AND a.citizen_id = ? AND a.status = 'confirmed'
            """,
            (appointment_id, citizen_id),
        ).fetchone()
        if current is None:
            connection.rollback()
            return Outcome("not_found", message="appointment not found")

        slot = connection.execute(
            """
            SELECT sl.id
            FROM slots AS sl
            WHERE sl.id = ?
              AND sl.starts_at > '2099-01-01T00:00:00+00:00'
              AND NOT EXISTS (
                  SELECT 1
                  FROM appointments AS a2
                  WHERE a2.slot_id = sl.id
                    AND a2.status IN ('requested', 'confirmed')
              )
            """,
            (new_slot_id,),
        ).fetchone()
        if slot is None:
            connection.rollback()
            return Outcome("conflict", message="slot is unavailable")

        connection.execute(
            "UPDATE appointments SET status = 'cancelled' WHERE id = ?",
            (appointment_id,),
        )
        cursor = connection.execute(
            """
            INSERT INTO appointments (citizen_id, slot_id, status, created_at)
            VALUES (?, ?, 'confirmed', '2099-08-01T09:00:00+00:00')
            """,
            (citizen_id, new_slot_id),
        )
        new_id = int(cursor.lastrowid)
        connection.execute(
            """
            INSERT INTO audit_events (appointment_id, event_type, created_at)
            VALUES (?, 'rescheduled', '2099-08-01T09:00:00+00:00')
            """,
            (new_id,),
        )
        connection.commit()
        return Outcome("success", appointment_id=new_id, message="appointment rescheduled")
    except sqlite3.IntegrityError:
        connection.rollback()
        return Outcome("conflict", message="slot became unavailable")
    except Exception:
        connection.rollback()
        raise
