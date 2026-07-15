# CivicQueue example application

This is a deliberately small Flask and SQLite application used by the textbook. It demonstrates a domain service, a relational schema, a server-rendered interface, a JSON endpoint, parameterised SQL, transactions, and tests.

It is not production-ready authentication or public-service infrastructure. The demo uses a fixed citizen identity and future seed dates so that the example is deterministic. A real system needs an identity provider, authorisation design, time-zone policy, migrations, secret management, TLS, backups, rate limits, monitoring, accessibility testing, and a data-protection assessment.

Run from the repository root:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r examples/webapp/requirements.txt
export FLASK_APP=examples.webapp.app
flask --app examples.webapp.app init-db
flask --app examples.webapp.app run
```

The test suite rebuilds an in-memory or temporary database and does not modify a production database.
