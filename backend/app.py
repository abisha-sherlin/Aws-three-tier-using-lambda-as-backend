from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

# MySQL connection configuration
db_config = {
    "host": "10.0.1.139",  # DB private IP
    "user": "appuser",
    "password": "YourStrongPassword",
    "database": "itemsdb"
}

# Health check endpoint
@app.route('/')
def health():
    return "Backend is running!", 200

# GET and POST for items
@app.route('/api/items', methods=['GET', 'POST'])
def manage_items():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT id, name FROM items")
        rows = cursor.fetchall()
        conn.close()
        return jsonify([{"id": r[0], "name": r[1]} for r in rows])

    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        if not name:
            conn.close()
            return jsonify({"error": "Name required"}), 400

        cursor.execute("INSERT INTO items (name) VALUES (%s)", (name,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"{name} added!"}), 201

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
