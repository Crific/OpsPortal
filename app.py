from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Home route (returns health check)
@app.route("/")
def home():
    return "Portal is running"

# Run app only when executed directly
if __name__ == "__main__":
    app.run(debug=True)