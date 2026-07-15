-- Confirmed appointments with human-readable context.
SELECT a.id,
       c.display_name,
       s.name AS service_name,
       sl.starts_at,
       a.status
FROM appointments AS a
JOIN citizens AS c ON c.id = a.citizen_id
JOIN slots AS sl ON sl.id = a.slot_id
JOIN services AS s ON s.id = sl.service_id
WHERE a.status = 'confirmed'
ORDER BY sl.starts_at;

-- Count confirmed appointments by service.
SELECT s.name, COUNT(*) AS appointment_count
FROM appointments AS a
JOIN slots AS sl ON sl.id = a.slot_id
JOIN services AS s ON s.id = sl.service_id
WHERE a.status = 'confirmed'
GROUP BY s.id, s.name;
