import os
import re
import sqlite3
import subprocess
from flask import Flask, request, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# FIX 1: Load secret key from environment variable
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(32))

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, role TEXT)")
    # FIX 2: Store salted password hashes instead of plaintext
    admin_hash = generate_password_hash("admin123", method="pbkdf2:sha256")
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username, password_hash, role) VALUES (?, ?, ?, ?)",
        (1, "admin", admin_hash, "admin")
    )
    conn.commit()
    conn.close()

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # FIX 3: Use parameterized queries to prevent SQL Injection
    cursor.execute("SELECT id, username, password_hash, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[2], password):
        return render_template_string("Welcome back, {{ username }}! Role: {{ role }}", username=user[1], role=user[3])
    return "Invalid credentials", 401

@app.route("/search")
def search():
    q = request.args.get("q", "")
    # FIX 4: Pass user input as template context so Jinja2 auto-escapes HTML characters
    template = """
    <html>
        <body>
            <h2>Search Results for: {{ query }}</h2>
            <p>No matching records found.</p>
        </body>
    </html>
    """
    return render_template_string(template, query=q)

@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # FIX 5: Strict allowlist validation + subprocess.run without shell=True
    if not re.match(r"^[a-zA-Z0-9.-]+$", host) or len(host) > 253:
        return "Invalid hostname", 400
    
    result = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True, timeout=5)
    return render_template_string("<pre>{{ output }}</pre>", output=result.stdout)

if __name__ == "__main__":
    init_db()
    # FIX 6: Disable debug mode in production
    app.run(host="127.0.0.1", port=5000, debug=False)
