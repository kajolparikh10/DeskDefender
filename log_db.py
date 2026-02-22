import sqlite3
import pandas as pd
import os

print("Building study optimizer database")

current_folder = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(current_folder, "study_optimizer.db")
csv_path = os.path.join(current_folder, "cleaned_sleep_data.csv")

def build_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Hardware study logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_date TEXT NOT NULL,
            start_hour INTEGER NOT NULL,
            duration_minutes INTEGER NOT NULL,
            mood TEXT NOT NULL
        )
    ''')

    #User sleep logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sleep_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sleep_date TEXT NOT NULL,
            bedtime_hour INTEGER NOT NULL,
            wake_hour INTEGER NOT NULL,
            total_hours REAL NOT NULL
        )
    ''')

    #Self-Reflection for future mood pattern analysis (unused)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reflection_date TEXT NOT NULL,
            followed_schedule TEXT NOT NULL,
            mood_improved TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Empty tables created (Waiting for robot input)")

def import_clean_kaggle_data():
    """Directly imports the cleaned Kaggle dataset as Table 4"""
    if not os.path.exists(csv_path):
        print(f"Cannot find '{csv_path}'. Make sure cleaned file is here")
        return

    #Read clean CSV and put into SQLite
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('global_sleep_data', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Cleaned Kaggle Dataset Imported. ({len(df)} profiles loaded into 'global_sleep_data')")

if __name__ == "__main__":
    build_tables()
    import_clean_kaggle_data()
    print("\nSleep Health Database can be used with live data")