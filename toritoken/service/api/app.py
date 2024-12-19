from flask import Flask, request, jsonify
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os

app = Flask(__name__)
SECRET_KEY = "supersecretkey"  # Placeholder, gets overridden
FLAG_FILE_PATH = "/tmp/flag.txt"  # Path to the flag file

@app.route("/", methods=["GET"])
def get_index():
    return jsonify({"ok": "ongi"})

@app.route("/data", methods=["GET"])
def get_data():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing token"}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if "role" not in decoded:
            return jsonify({"error": "Missing role param in payload"})
        if decoded.get("role") == "admin":
                  
             # Read the flag from the file
            try:
                with open(FLAG_FILE_PATH, "r") as flag_file:
                    flag = flag_file.read().strip()
            except Exception as e:

                return jsonify({"error": f"Could not read flag: {e}"})
            return jsonify({"flag": flag})
        else:
            return jsonify({"error": "Invalid role"}), 403
    except (ExpiredSignatureError, InvalidTokenError):
        return jsonify({"error": "Invalid token"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)