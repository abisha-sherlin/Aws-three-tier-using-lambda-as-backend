from flask import Flask, request, jsonify
from mysql.connector import pooling
import boto3

app = Flask(__name__)

# --- SSM Client ---
ssm = boto3.client("ssm")

# --- Fetch and cache DB credentials ---
def get_parameter(name, decrypt=False):
    response = ssm.get_parameter(Name=name, WithDecryption=decrypt)
    return response["Parameter"]["Value"]

DB_HOST = get_parameter("/three-tier/db_host")
DB_USER = get_parameter("/three-tier/db_user")
DB_PASS = get_parameter("/three-tier/db_pass", decrypt=True)
DB_NAME = get_parameter("/three-tier/db_name")
DB_PORT = int(get_parameter("/three-tier/db_port"))

# --- MySQL Connection Pool ---
db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    pool_reset_session=True,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    port=DB_PORT
)

def get_conn():
    """Get a connection from the pool"""
    return db_pool.get_connection()

# --- API Routes ---
@app.route("/api/items", methods=["GET"])
def list_items():
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM items")
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route("/api/items", methods=["POST"])
def add_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' field"}), 400

    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name) VALUES (%s)", (data["name"],))
        conn.commit()
        return jsonify({"status": "created", "id": cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200
