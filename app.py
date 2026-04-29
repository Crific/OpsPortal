from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy

# Password hashing utilities
from werkzeug.security import generate_password_hash, check_password_hash

# Flask-Login utilities for session management and route protection
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

# =========================
# App Configuration
# =========================

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Secret key for sessions and flash messages
app.config["SECRET_KEY"] = "dev-secret-key"

db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# =========================
# Models
# =========================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # stores hashed password
    role = db.Column(db.String(20), default="user")

    # One user can have many tickets/requests
    requests = db.relationship("Request", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Link each ticket to the user who created it
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)

    # Ticket workflow status
    status = db.Column(db.String(30), default="pending", nullable=False)

    # Ticket priority level
    priority = db.Column(db.String(10), default="low", nullable=False)

    def __repr__(self):
        return f"<Request {self.title}>"


# =========================
# Login Manager
# =========================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =========================
# General Routes
# =========================

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


# =========================
# Authentication Routes
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle login form submission and start user session
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Successfully logged out.", "success")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        # Make sure password and confirmation match
        if password != confirm:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        # Prevent duplicate accounts
        existing_username = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_username:
            flash("Username already exists.", "error")
            return redirect(url_for("register"))

        if existing_email:
            flash("Email already exists.", "error")
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(
            username=username,
            email=email,
            password=hashed_pw,
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# User Dashboard Routes
# =========================

@app.route("/dashboard")
@login_required
def dashboard():
    # Redirect admins to the admin dashboard
    if current_user.role == "admin":
        return redirect(url_for("admin_dashboard"))

    # Regular users only see their own tickets
    tickets = current_user.requests
    return render_template("dashboard.html", tickets=tickets)


# =========================
# Ticket Routes
# =========================

@app.route("/create", methods=["GET", "POST"])
@login_required
def create_ticket():
    if request.method == "POST":
        new_ticket = Request(
            user_id=current_user.id,
            title=request.form["title"],
            body=request.form["body"],
            priority=request.form["priority"],
        )

        db.session.add(new_ticket)
        db.session.commit()

        flash("Ticket created successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("create_ticket.html")


@app.route("/edit/<int:ticket_id>", methods=["GET", "POST"])
@login_required
def edit_ticket(ticket_id):
    current_ticket = Request.query.get_or_404(ticket_id)

    # Only the ticket owner or an admin can edit a ticket
    if current_ticket.user_id != current_user.id and current_user.role != "admin":
        abort(403)

    if request.method == "POST":
        current_ticket.title = request.form["title"]
        current_ticket.body = request.form["body"]
        current_ticket.priority = request.form["priority"]

        db.session.commit()
        flash("Ticket successfully edited.", "success")
        return redirect(url_for("dashboard"))

    return render_template("edit_ticket.html", current_ticket=current_ticket)


# =========================
# Admin Routes
# =========================

@app.route("/admin")
@login_required
def admin_dashboard():
    # Restrict admin dashboard access to admins only
    if current_user.role != "admin":
        abort(403)

    tickets = Request.query.order_by(Request.id.desc()).all()
    return render_template("admin_dash.html", tickets=tickets)


@app.route("/view/<int:ticket_id>")
@login_required
def admin_view(ticket_id):
    if current_user.role != "admin":
        abort(403)

    current_ticket = Request.query.get_or_404(ticket_id)
    return render_template("admin_ticket.html", current_ticket=current_ticket)


@app.route("/update_status/<int:ticket_id>", methods=["POST"])
@login_required
def update_status(ticket_id):
    if current_user.role != "admin":
        abort(403)

    # Admin can update the workflow status of a ticket
    current_ticket = Request.query.get_or_404(ticket_id)
    current_ticket.status = request.form["status"]

    db.session.commit()

    flash("Ticket status updated successfully.", "success")
    return redirect(url_for("admin_view", ticket_id=ticket_id))


# =========================
# Run App
# =========================

if __name__ == "__main__":
    app.run(debug=True)