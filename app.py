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
# - [x] User login (Flask-Login)
# - [x] Password hashing
# - [x] Protect routes

# Phase 3: Core Features
# - [x] Create request/ticket system
# - [ ] View requests
# - [ ] Edit requests
# - [ ] Assign requests (admin/operator)

# Phase 4: Dashboard
# - [ ] Status tracking (pending, in progress, resolved)
# - [ ] Basic analytics (counts)

# Notes:
# Keep everything in app.py for now.
# Refactor into folders (models, routes) later.

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Password Hashing
from werkzeug.security import generate_password_hash, check_password_hash

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

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Request Class
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) # Foreign key linking request to a specific user
    user = db.relationship("User", backref="requests") # forming a relationship between User model and Requests
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
@login_required
def home():
    return render_template("home.html")

# Login Page Route
@app.route("/login", methods=["GET", "POST"])
def login():   
    # Login flow:
    # 1. If POST → get form data (email, password) x 
    # 2. Find user in database by email x
    # 3. If user exists AND password is correct:
    #       → log them in (login_user)
    #       → redirect to home/dashboard
    # 4. Else:
    #       → show error (invalid credentials)
    # 5. If GET → just render login page

    if request.method == 'POST': 
        # Get form data (email, password)
        email = request.form['email']
        password = request.form['password']

        # Find user in database by email x
        user = User.query.filter_by(email=email).first()

        # If user exists AND password is correct:
        # → log them in (login_user)
        # → redirect to home/dashboard        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))

        else:
            # Validation: if incorrect password
            flash("Incorrect password, please try again.")
            return redirect(url_for("login"))

    return render_template("login.html")

# Logout User Route
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Successfully logged out.")
    return redirect(url_for("login"))


# Registration Page
@app.route("/register", methods=["GET","POST"])
def register():  
    if request.method == 'POST':
        # Handle form submission
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        # Confirm password logic
        if password != confirm:
            flash("Passwords do not match")
            return redirect(url_for("register"))

        # Hash password
        hashed_pw = generate_password_hash(password)

        # Add new user to User object
        new_user = User(username=username, email=email, password=hashed_pw)

        # Add new User object to db
        db.session.add(new_user)
        db.session.commit()

        # Route user back to login page
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/create", methods=["GET","POST"])
@login_required
def create_ticket():
    # Check if form was submitted
    # Get title, body, and other ticket fields from form ()
    # Create a new ticket/request object
    # Set the ticket's user to the currently logged-in user
    # Save the ticket to the database
    # Redirect user or show success message
    if request.method == 'POST':
        # get form data
        # user = current_user
        # user_id = user.id
        # create ticket using that id
        user = current_user
        user_id = user.id
        title = request.form['title']
        body = request.form['body']
        priority = request.form['priority']

        new_ticket = Request(user=user, user_id=user_id, title=title, body=body, priority=priority)

        db.session.add(new_ticket)
        db.session.commit()

        return redirect(url_for("dashboard"))


    return render_template("create_ticket.html")


# Run app only when executed directly
if __name__ == "__main__":
    app.run(debug=True)