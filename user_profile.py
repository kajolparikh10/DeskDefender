import sqlite3
import os

current_folder = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(current_folder, "study_optimizer.db")

def create_and_save_profile():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Create the user profile table (if it doesn't exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            occupation TEXT,
            sleep_duration REAL,
            quality_of_sleep INTEGER,
            physical_activity INTEGER,
            stress_level INTEGER,
            bmi_category TEXT,
            heart_rate INTEGER,
            daily_steps INTEGER,
            sleep_disorder TEXT,
            bp_systolic INTEGER,
            bp_diastolic INTEGER
        )
    ''')

    #Delete any old profile
    cursor.execute('DELETE FROM user_profile')

    #User stats
    user_data = {
        "age": 21,
        "occupation": "Software Engineer",
        "sleep_duration": 6.5,
        "quality_of_sleep": 6,
        "physical_activity": 45,
        "stress_level": 7,
        "bmi_category": "Normal",
        "heart_rate": 72,
        "daily_steps": 5000,
        "sleep_disorder": "None",
        "bp_systolic": 120,
        "bp_diastolic": 80
    }

    cursor.execute('''
        INSERT INTO user_profile (age, occupation, sleep_duration, quality_of_sleep, 
                                  physical_activity, stress_level, bmi_category, 
                                  heart_rate, daily_steps, sleep_disorder, bp_systolic, bp_diastolic)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(user_data.values()))

    conn.commit()
    conn.close()
    print("User Profile saved to database successfully")

if __name__ == "__main__":
    create_and_save_profile()