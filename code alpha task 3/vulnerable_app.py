import os
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)
# FLAW 1: Hardcoded Secret Key (CWE-798)
app.secret_key = "super-secret-hardcoded-key-12345"

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
    # FLAW 2: Plaintext Password Storage (CWE-256)
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, role) VALUES (1, 'admin', 'admin123', 'admin')")
    conn.commit()
    conn.close()

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # FLAW 3: SQL Injection via String Formatting (CWE-89)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return f"Welcome back, {user[1]}! Role: {user[3]}"
    return "Invalid credentials", 401

@app.route("/search")
def search():
    q = request.args.get("q", "")
    # FLAW 4: Reflected Cross-Site Scripting (XSS) via SSTI/Raw HTML (CWE-79)
    template = f"""
    <html>
        <body>
            <h2>Search Results for: {q}</h2>
            <p>No matching records found.</p>
        </body>
    </html>
    """
    return render_template_string(template)

@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # FLAW 5: OS Command Injection (CWE-78)
    output = os.popen(f"ping -c 1 {host}").read()
    return f"<pre>{output}</pre>"

if __name__ == "__main__":
    init_db()
    # FLAW 6: Debug Mode Enabled in Production (CWE-489)
    app.run(host="0.0.0.0", port=5000, debug=True)
