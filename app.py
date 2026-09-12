import os

from flask import Flask, request, session, redirect, url_for, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from functools import wraps
import time

app = Flask(__name__)

# Secret key for signing sessions
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-secret-key")

# Secure session configuration
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = False  # True when using HTTPS
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)

# Demo user database
users = {
    "admin": generate_password_hash("StrongPassword123!")
}

# Simple in-memory rate limiter
login_attempts = {}
MAX_ATTEMPTS = 5
BLOCK_TIME = 60


def validate_input(username, password):
    """Server-side validation."""
    if not username or not password:
        return False

    if len(username) > 50 or len(password) > 128:
        return False

    return True


def rate_limit(ip_address):
    """Allow only 5 failed attempts per minute."""
    current_time = time.time()

    attempts = login_attempts.get(ip_address, [])

    # Keep attempts from the last minute
    attempts = [
        attempt for attempt in attempts
        if current_time - attempt < BLOCK_TIME
    ]

    login_attempts[ip_address] = attempts

    return len(attempts) >= MAX_ATTEMPTS


def record_failed_attempt(ip_address):
    login_attempts.setdefault(ip_address, []).append(time.time())


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return function(*args, **kwargs)

    return wrapper


@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))

    return """
    <h1>Secure Authentication Lab</h1>
    <a href="/login">Login</a>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        ip_address = request.remote_addr

        if rate_limit(ip_address):
            error = "Login temporarily unavailable. Please try again later."
        elif not validate_input(username, password):
            error = "Invalid username or password."
        elif username not in users or not check_password_hash(
            users[username], password
        ):
            record_failed_attempt(ip_address)
            error = "Invalid username or password."
        else:
            session.clear()
            session.permanent = True
            session["username"] = username

            return redirect(url_for("dashboard"))

    return render_template_string("""
    <h1>Login</h1>

    {% if error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}

    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username" required maxlength="50">
        <br><br>

        <label>Password:</label>
        <input type="password" name="password" required maxlength="128">
        <br><br>

        <button type="submit">Login</button>
    </form>
    """, error=error)


@app.route("/dashboard")
@login_required
def dashboard():
    username = session["username"]

    return f"""
    <h1>Welcome, {username}!</h1>
    <p>You are successfully authenticated.</p>
    <a href="/logout">Logout</a>
    """


@app.route("/logout")
def logout():
    session.clear()

    return """
    <h1>You have been logged out.</h1>
    <a href="/login">Login again</a>
    """


if __name__ == "__main__":
    app.run(debug=False)
