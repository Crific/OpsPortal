# =========================
# Development Roadmap
# =========================

# Phase 1: Database Setup
# - [x] Set up database (SQLAlchemy)
# - [x] Create User model
# - [x] Create Request model
# - [x] Run db.create_all()

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
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Flask DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initializing db
db = SQLAlchemy(app)  

# User class
class User(db.Model):            
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) # 200 for hash
    role = db.Column(db.String(20), default="user") 

    # Human-readable string representation of the User object for debugging
    def __repr__(self):
        return f"<User {self.username}>"

# Request Class
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) # Foreign key linking request to a specific user
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)

    # Default workflow status (pending, in-progress, completed)
    status = db.Column(db.String(30), default="pending", nullable=False) 
    
    # Priority level (low, medium, high)
    priority = db.Column(db.String(10), default="low", nullable=False) # Sets Priority level - defaults to low

    def __repr__(self):
        return f"<Request {self.title}>"
        
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