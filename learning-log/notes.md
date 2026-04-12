# OpsPortal – Development Notes

## Environment Setup

### Windows vs. sudo

* Windows does not use `sudo`
* Administrative privileges are handled by running the terminal as Administrator
* Most development tasks (Flask, `pip`, virtual environments) do not require admin access

---

### Virtual Environment (venv)

Create:

```
python -m venv venv
```

Activate (PowerShell):

```
.\venv\Scripts\Activate.ps1
```

If script execution is blocked:

```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Purpose:**

* Isolates project dependencies
* Prevents conflicts with system Python
* Standard practice for Python development

---

## Dependencies

Install required packages:

```
pip install flask flask-login flask-sqlalchemy
```

Save environment:

```
pip freeze > requirements.txt
```

---

### Key Concepts

* `pip freeze` captures a snapshot of the current environment
* Ensures consistent dependency versions across different machines

---

### requirements.txt

Install dependencies from file:

```
pip install -r requirements.txt
```

**Purpose:**

* Enables reproducible environments
* Required for deployment and collaboration

---

### Notes

* Flask installs additional dependencies automatically (e.g., Jinja2, Werkzeug)
* Including all dependencies via `pip freeze` is acceptable for this project

---

## Version Control

### .gitignore

```
venv/
```

Do not include:

* Virtual environment (`venv/`)

---

### Commit Conventions

* `feat` → new feature
* `fix` → bug fix
* `chore` → setup or maintenance
* `docs` → documentation
* `refactor` → code improvements without changing behavior

Example:

```
git commit -m "chore: add requirements"
```
## Flask-SQLAlchemy

### Import
from flask_sqlalchemy import SQLAlchemy

### Purpose
- Connects Flask app to a database
- Lets you use Python instead of raw SQL (ORM)

### Setup
db = SQLAlchemy(app)

### Key Idea
- Tables are defined as Python classes

Example:
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))

### Mental Model
- SQLAlchemy = translates Python ↔ SQL