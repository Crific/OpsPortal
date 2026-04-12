# =========================
# Development Roadmap
# =========================

# Phase 1: Database Setup
# - [ ] Set up database (SQLAlchemy)
# - [ ] Create User model
# - [ ] Create Request model
# - [ ] Run db.create_all()

# Phase 2: Authentication
# - [ ] User registration
# - [ ] User login (Flask-Login)
# - [ ] Password hashing
# - [ ] Protect routes

# Phase 3: Core Features
# - [ ] Create request/ticket system
# - [ ] View requests
# - [ ] Edit requests
# - [ ] Assign requests (admin/operator)

# Phase 4: Dashboard
# - [ ] Status tracking (pending, in progress, resolved)
# - [ ] Basic analytics (counts)

# Notes:
# Keep everything in app.py for now.
# Refactor into folders (models, routes) later.

from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

# Home route 
@app.route("/")
def home():
    return render_template("home.html") 

# Login Page Route
@app.route("/login")
def login():
    return render_template("login.html")

# Run app only when executed directly
if __name__ == "__main__":
    app.run(debug=True)