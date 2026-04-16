# =========================
# Development Roadmap
# =========================

# Phase 1: Database Setup
# - [x] Set up database (SQLAlchemy)
# - [x] Create User model
# - [x] Create Request model
# - [x] Run db.create_all()

# Phase 2: Authentication
# - [x] User registration
# - [ ] User login (Flask-Login)
# - [x] Password hashing
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

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Password Hashing
from werkzeug.security import generate_password_hash 

# Flask Authentication
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)


# Initialize the Flask application
app = Flask(__name__)

# Flask DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initializing a secret key for authentication
app.config["SECRET_KEY"] = "dev-secret-key"

# Initialize Flask-Login for user session management and authentication
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Initializing db
db = SQLAlchemy(app)  

# User class
class User(UserMixin, db.Model): 
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

# Registration Page
@app.route("/register", methods=["GET","POST"])
def register():  
   if request.method == 'POST':
        # Handle form submission
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash password
        hashed_pw = generate_password_hash(password)

        # Add new user to User object
        new_user = User(username=username, email=email, password= hashed_pw)

        # Add new User object to db
        db.session.add(new_user)
        db.session.commit()

        # Route user back to login page
        return redirect(url_for("login"))

    return render_template("register.html")



# Run app only when executed directly
if __name__ == "__main__":
    app.run(debug=True)