PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS citizens (
    id INTEGER PRIMARY KEY,
    display_name TEXT NOT NULL,
    contact TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS slots (
    id INTEGER PRIMARY KEY,
    service_id INTEGER NOT NULL REFERENCES services(id),
    starts_at TEXT NOT NULL,
    ends_at TEXT NOT NULL,
    CHECK (ends_at > starts_at)
);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY,
    citizen_id INTEGER NOT NULL REFERENCES citizens(id),
    slot_id INTEGER NOT NULL REFERENCES slots(id),
    status TEXT NOT NULL CHECK (status IN ('requested', 'confirmed', 'cancelled', 'completed')),
    created_at TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS one_active_appointment_per_slot
ON appointments(slot_id)
WHERE status IN ('requested', 'confirmed');

CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id),
    event_type TEXT NOT NULL,
    created_at TEXT NOT NULL
);
