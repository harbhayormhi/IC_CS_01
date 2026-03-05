#app.py
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db
from crypto_utils import generate_rsa_keys, encrypt_file, encrypt_key_rsa
import sqlite3
import os

app = Flask(__name__)
init_db()

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = generate_password_hash(data["password"])

    private_key, public_key = generate_rsa_keys()

    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    conn = sqlite3.connect("instance/database.db")
    c = conn.cursor()

    c.execute("INSERT INTO users (username, password, public_key) VALUES (?, ?, ?)",
              (username, password, pub_pem))

    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"})

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    username = request.form["username"]

    conn = sqlite3.connect("instance/database.db")
    c = conn.cursor()

    c.execute("SELECT id, public_key FROM users WHERE username=?", (username,))
    user = c.fetchone()

    if not user:
        return jsonify({"error": "User not found"})

    user_id, pub_key = user
    public_key = serialization.load_pem_public_key(pub_key)

    data = file.read()
    encrypted_data, aes_key, iv = encrypt_file(data)
    encrypted_key = encrypt_key_rsa(aes_key, public_key)

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    with open(filepath, "wb") as f:
        f.write(iv + encrypted_data)

    c.execute("INSERT INTO files (filename, owner_id, encrypted_key) VALUES (?, ?, ?)",
              (file.filename, user_id, encrypted_key))

    conn.commit()
    conn.close()

    return jsonify({"message": "File uploaded securely"})
    
@app.route("/")
def home():
 return"secure File Sharing System Running"

if __name__=="__main__":
 app.run(ssl_context=("cert.pem",
"key.pem"))
