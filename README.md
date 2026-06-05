# Campus Milk Tea Group Ordering System

P0 implementation of a Flask + MySQL database engineering demo system.

## What Is Included

- Flask web app: `app.py`
- MySQL connection helper: `db.py`
- Database reset and object script: `schema.sql`
- HTML templates: `templates/`
- CSS: `static/style.css`
- Demo walkthrough: `docs/DEMO_CASES.md`

## Environment

- Python managed by conda
- MySQL 8.0 or a compatible MySQL server
- Python packages listed in `requirements.txt`

Activate the project environment before running Python commands:

```bash
source <conda_root>/etc/profile.d/conda.sh
conda activate db
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

Create or reset the database by executing `schema.sql` with a MySQL client:

```bash
mysql -u <db_user> -p < schema.sql
```

The script recreates `milk_tea_group_db`, creates all P0 tables, seed data,
trigger, stored procedure, and view.

## Connection Configuration

`db.py` reads these environment variables and falls back to local defaults:

| Variable | Meaning | Default |
| --- | --- | --- |
| `DB_HOST` | MySQL host | `127.0.0.1` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_USER` | MySQL user | `root` |
| `DB_PASSWORD` | MySQL password | empty string |
| `DB_NAME` | Database name | `milk_tea_group_db` |
| `DB_CHARSET` | Client character set | `utf8mb4` |

Example:

```bash
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_USER=<db_user>
export DB_PASSWORD=<database_password>
export DB_NAME=milk_tea_group_db
export DB_CHARSET=utf8mb4
```

`autocommit` is set to `False` in `db.py` for transaction demos.

## Run The App

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

If port `5000` is already in use, start the app from Python on another port:

```bash
python -c "from app import app; app.run(host='127.0.0.1', port=5001, debug=True)"
```

## P0 Pages

| Page | Path | Purpose |
| --- | --- | --- |
| Homepage | `/` | System name, database statistics, and P0 entrances |
| Add order | `/order/add` | Trigger-controlled insert |
| Finish group order | `/group/finish` | Stored-procedure-controlled update |
| Cancel group order | `/group/cancel` | Explicit transaction delete |
| Query group detail | `/group/query` | View-based multi-table query |

## Demo Inputs

Use `docs/DEMO_CASES.md` for the recommended input values and expected results.
Re-run `schema.sql` before repeating a destructive demo such as canceling a group
order.

## Common Issues

- Homepage shows database unavailable: start MySQL, import `schema.sql`, and check `DB_*` variables.
- MySQL import fails on an existing database: `schema.sql` already drops and recreates `milk_tea_group_db`; confirm the MySQL user has permission.
- Stored procedure or trigger text displays incorrectly: confirm the MySQL client uses `utf8mb4`.
- Port `5000` is busy: run the alternate port command shown above.
