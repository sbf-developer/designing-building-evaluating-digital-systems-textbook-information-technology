INSERT INTO citizens (id, display_name, contact) VALUES
    (1, 'Alex Citizen', 'alex@example.invalid'),
    (2, 'Morgan Citizen', 'morgan@example.invalid');

INSERT INTO services (id, name) VALUES
    (1, 'Benefits advice'),
    (2, 'Permit support');

INSERT INTO slots (id, service_id, starts_at, ends_at) VALUES
    (1, 1, '2099-09-01T09:00:00+00:00', '2099-09-01T09:30:00+00:00'),
    (2, 1, '2099-09-01T10:00:00+00:00', '2099-09-01T10:30:00+00:00'),
    (3, 2, '2099-09-02T09:00:00+00:00', '2099-09-02T09:30:00+00:00');

INSERT INTO appointments (id, citizen_id, slot_id, status, created_at) VALUES
    (1, 1, 1, 'confirmed', '2099-08-01T09:00:00+00:00');
