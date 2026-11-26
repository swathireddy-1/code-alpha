# Secure Coding Review Report

## Executive Summary
A manual and static source code audit was performed on `vulnerable_app.py` (a Python Flask web application). The review identified **6 security vulnerabilities**, including **3 Critical** flaws (SQL Injection, OS Command Injection, Reflected XSS/SSTI) that allow full database compromise, arbitrary code execution, and session hijacking.

| ID | Vulnerability | CWE | Severity | Location |
|---|---|---|---|---|
| VULN-01 | SQL Injection (SQLi) | CWE-89 | Critical | `login()` (`vulnerable_app.py:25`) |
| VULN-02 | OS Command Injection | CWE-78 | Critical | `ping()` (`vulnerable_app.py:51`) |
| VULN-03 | Reflected XSS & SSTI | CWE-79 / CWE-1336 | Critical | `search()` (`vulnerable_app.py:37`) |
| VULN-04 | Plaintext Password Storage | CWE-256 | High | `init_db()` (`vulnerable_app.py:14`) |
| VULN-05 | Hardcoded Secret Key | CWE-798 | High | Global config (`vulnerable_app.py:7`) |
| VULN-06 | Debug Mode Enabled | CWE-489 | Medium | `__main__` (`vulnerable_app.py:56`) |

---

## Detailed Findings & Remediations

### 1. [CRITICAL] SQL Injection in `/login` (CWE-89)
* **Description:** User-supplied `username` and `password` values are interpolated directly into an SQL query string using an f-string. An attacker can bypass authentication using payloads such as `' OR '1'='1' --`.
* **Vulnerable Code:**
  ```python
  query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
  cursor.execute(query)
  ```
* **Remediation:** Use parameterized queries (`?` placeholders) so the database engine treats input strictly as data rather than executable SQL syntax.

### 2. [CRITICAL] OS Command Injection in `/ping` (CWE-78)
* **Description:** The `host` query parameter is concatenated into a shell command executed via `os.popen()`. Supplying `127.0.0.1; cat /etc/passwd` executes arbitrary OS commands.
* **Vulnerable Code:**
  ```python
  output = os.popen(f"ping -c 1 {host}").read()
  ```
* **Remediation:** Validate input against a strict allowlist regex (`^[a-zA-Z0-9.-]+$`) and execute commands via `subprocess.run([...], shell=False)`.

### 3. [CRITICAL] Reflected XSS & Server-Side Template Injection in `/search` (CWE-79 / CWE-1336)
* **Description:** User input `q` is formatted directly into the template string prior to `render_template_string()`, bypassing Jinja2's auto-escaping and enabling both JavaScript execution (`<script>alert(1)</script>`) and Jinja2 template injection (`{{7*7}}`).
* **Vulnerable Code:**
  ```python
  template = f"<h2>Search Results for: {q}</h2>"
  return render_template_string(template)
  ```
* **Remediation:** Pass untrusted variables as named context arguments (`render_template_string(template, query=q)`) so Jinja2 automatically escapes special HTML characters.

### 4. [HIGH] Plaintext Password Storage (CWE-256)
* **Description:** User passwords are stored in cleartext inside `users.db`. Any read access to the database exposes user credentials.
* **Remediation:** Hash passwords using a strong, salted cryptographic algorithm (`werkzeug.security.generate_password_hash` with PBKDF2-SHA256 or Argon2/bcrypt).

### 5. [HIGH] Hardcoded Cryptographic Secret Key (CWE-798)
* **Description:** `app.secret_key` is hardcoded in source control, allowing attackers with repository access to forge signed session cookies.
* **Remediation:** Load secrets from environment variables (`os.environ.get("FLASK_SECRET_KEY")`) or a secrets manager.

### 6. [MEDIUM] Flask Debug Mode Enabled (CWE-489)
* **Description:** Running with `debug=True` exposes stack traces and the interactive Werkzeug debugger on unhandled exceptions, which can lead to Remote Code Execution (RCE).
* **Remediation:** Set `debug=False` in production deployments and bind to `127.0.0.1` behind a reverse proxy.
