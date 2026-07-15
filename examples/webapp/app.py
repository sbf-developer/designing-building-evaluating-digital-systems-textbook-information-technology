"""Small Flask application for the CivicQueue case."""

from pathlib import Path
import sqlite3

from flask import Flask, jsonify, redirect, render_template, request, url_for

from .domain import reschedule_appointment

BASE_DIR = Path(__file__).resolve().parent
SCHEMA = BASE_DIR.parent / "sql" / "schema.sql"
SEED = BASE_DIR.parent / "sql" / "seed.sql"


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=str(BASE_DIR / "civicqueue.sqlite3"),
        DEMO_CITIZEN_ID=1,
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)

    def get_db() -> sqlite3.Connection:
        if "db" not in app.extensions:
            connection = sqlite3.connect(app.config["DATABASE"])
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            app.extensions["db"] = connection
        return app.extensions["db"]

    @app.teardown_appcontext
    def close_db(_error: BaseException | None) -> None:
        connection = app.extensions.pop("db", None)
        if connection is not None:
            connection.close()

    @app.cli.command("init-db")
    def init_db_command() -> None:
        connection = get_db()
        connection.executescript(SCHEMA.read_text(encoding="utf-8"))
        connection.executescript(SEED.read_text(encoding="utf-8"))
        connection.commit()
        print("Initialised CivicQueue database.")

    @app.get("/")
    def index():
        connection = get_db()
        appointments = connection.execute(
            """
            SELECT a.id, a.status, c.display_name, sl.starts_at, s.name AS service_name
            FROM appointments AS a
            JOIN citizens AS c ON c.id = a.citizen_id
            JOIN slots AS sl ON sl.id = a.slot_id
            JOIN services AS s ON s.id = sl.service_id
            WHERE a.citizen_id = ?
            ORDER BY sl.starts_at
            """,
            (app.config["DEMO_CITIZEN_ID"],),
        ).fetchall()
        return render_template("index.html", appointments=appointments)

    @app.route("/appointments/<int:appointment_id>/reschedule", methods=("GET", "POST"))
    def reschedule(appointment_id: int):
        connection = get_db()
        if request.method == "POST":
            raw_slot = request.form.get("slot_id", "")
            try:
                new_slot_id = int(raw_slot)
            except ValueError:
                return render_template("reschedule.html", slots=[], error="Choose a valid slot."), 400
            outcome = reschedule_appointment(
                connection,
                appointment_id,
                app.config["DEMO_CITIZEN_ID"],
                new_slot_id,
            )
            if outcome.is_success:
                return redirect(url_for("index"))
            return render_template("reschedule.html", slots=[], error=outcome.message), 409

        slots = connection.execute(
            """
            SELECT sl.id, sl.starts_at, s.name AS service_name
            FROM slots AS sl
            JOIN services AS s ON s.id = sl.service_id
            WHERE NOT EXISTS (
                SELECT 1 FROM appointments AS a
                WHERE a.slot_id = sl.id AND a.status IN ('requested', 'confirmed')
            )
            ORDER BY sl.starts_at
            """
        ).fetchall()
        return render_template("reschedule.html", slots=slots, error=None)

    @app.post("/api/appointments/<int:appointment_id>/reschedule")
    def api_reschedule(appointment_id: int):
        payload = request.get_json(silent=True) or {}
        if not isinstance(payload.get("slot_id"), int):
            return jsonify(error="slot_id must be an integer"), 400
        outcome = reschedule_appointment(
            get_db(),
            appointment_id,
            app.config["DEMO_CITIZEN_ID"],
            payload["slot_id"],
        )
        if outcome.status == "not_found":
            return jsonify(error=outcome.message), 404
        if outcome.status == "conflict":
            return jsonify(error=outcome.message), 409
        return jsonify(status="rescheduled", appointment_id=outcome.appointment_id), 200

    return app


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        connection = app.extensions.get("db")
        if connection is None:
            connection = sqlite3.connect(app.config["DATABASE"])
            connection.executescript(SCHEMA.read_text(encoding="utf-8"))
            connection.executescript(SEED.read_text(encoding="utf-8"))
            connection.commit()
            connection.close()
    app.run(debug=False)
