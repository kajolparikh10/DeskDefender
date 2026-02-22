import sqlite3
import os
current_folder = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(current_folder, "study_optimizer.db")

def setup_database():
    conn = sqlite3.connect('study_optimizer.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            occupation TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_date TEXT,
            start_hour INTEGER,
            duration_minutes INTEGER,
            mood TEXT
        )
    ''')

    cursor.execute('DELETE FROM profile')
    cursor.execute('DELETE FROM study_logs')

    cursor.execute('''
        INSERT INTO profile (age, occupation) 
        VALUES (20, 'Computer Science')
    ''')

    mock_logs = [
        ('2026-02-18', 14, 120, 'Happy'),
        ('2026-02-19', 10, 45, 'Tired'),
        ('2026-02-19', 16, 90, 'Stressed'),
        ('2026-02-20', 20, 150, 'Happy'),
        ('2026-02-21', 9, 60, 'Tired'),
        ('2026-02-21', 13, 110, 'Stressed')
    ]
    
    cursor.executemany('''
        INSERT INTO study_logs (study_date, start_hour, duration_minutes, mood) 
        VALUES (?, ?, ?, ?)
    ''', mock_logs)

    conn.commit()
    conn.close()
    print("Success, 'study_optimizer.db' is ready for ESP-32.")

if __name__ == '__main__':
    setup_database()