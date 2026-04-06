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