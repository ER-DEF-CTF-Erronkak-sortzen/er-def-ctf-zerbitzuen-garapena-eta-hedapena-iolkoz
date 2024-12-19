from flask import Flask, request, render_template
import hashlib
import mysql.connector

app = Flask(__name__)

# Database connection settings
DB_CONFIG = {
    "host": "db",
    "user": "root",
    "password": "root",
    "database": "ctf"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Vulnerable SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if user:
        return f"Ongi etorri {user['username']}! Gure APIan erabiltzeko giltza: {user['secret_key']}, zure rola: {user['role']}"
    return "Erabiltzaile/pasahitza ez dira zuzenak!", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
