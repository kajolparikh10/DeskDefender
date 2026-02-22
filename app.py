from flask import Flask, render_template
import sqlite3
import os
import glob

app = Flask(__name__)

current_folder = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(current_folder, "study_optimizer.db")
STATIC_FOLDER = os.path.join(current_folder, "static")

@app.route('/')
def home():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user_profile LIMIT 1")
    profile = cursor.fetchone()
    
    cursor.execute("SELECT * FROM study_logs ORDER BY id DESC LIMIT 5")
    recent_logs = cursor.fetchall()
    conn.close()

    video_files = glob.glob(os.path.join(STATIC_FOLDER, "*.mp4"))
    security_alerts = [os.path.basename(vid) for vid in video_files]

    graph_exists = os.path.exists(os.path.join(STATIC_FOLDER, "study_history.png"))

    return render_template('index.html', 
                           profile=profile, 
                           logs=recent_logs, 
                           alerts=security_alerts,
                           graph_exists=graph_exists)

if __name__ == '__main__':
    print("Web Server Online")
    app.run(debug=True, port=5000)