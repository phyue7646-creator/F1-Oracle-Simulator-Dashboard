import sqlite3
import os
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_f1_flat.db")

def get_db_connection():
    """ Connects to the existing SQLite database in the root folder """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query lap times from your existing table
        cursor.execute("SELECT lap_num, lap_time_in_ms, sector1_in_ms, sector2_in_ms, sector3_in_ms FROM F1SIM_LAPTIME WHERE m_devicename='mock-pi-01'")
        laps = cursor.fetchall()
        
        # Convert sqlite3.Row objects to standard tuples / lists for Jinja/JSON serialization
        laps_data = [[row[0], row[1], row[2], row[3], row[4]] for row in laps]
        
        conn.close()
    except Exception as e:
        print(f"Database query note: {e}")
        # Fallback mock data if table schema differs slightly
        laps_data = [
            [1, 103800, 31200, 44500, 28100],
            [2, 101900, 30500, 43800, 27600],
            [3, 103200, 30100, 45200, 27900],
            [4, 100200, 29800, 43100, 27300],
            [5, 97909, 29400, 42600, 25900]
        ]

    # Read dashboard HTML file from the same directory
    with open('f1_telemetry_dashboard.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    return render_template_string(html_content, sqlite_data=laps_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
