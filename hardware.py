import serial
import sqlite3
import time
from datetime import datetime
import os

ESP32_PORT = '/dev/cu.usbserial-1420' #Update to MY Mac's USB port
BAUD_RATE = 115200
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "study_optimizer.db")

#State Variables
current_mood = None
session_start_time = None
break_start_time = None
total_studied_seconds = 0
is_studying = False

def save_session(duration, mood):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    #current time
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_hour = now.hour
    
    cursor.execute("""
        INSERT INTO study_logs (study_date, start_hour, duration_minutes, mood)
        VALUES (?, ?, ?, ?)
    """, (current_date, current_hour, duration, mood))
    
    conn.commit()
    conn.close()
    print("Session logged to database! Updating graphs.")
    os.system('python analysis.py')

try:
    ser = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
    print("Connected to DeskDefender. Waiting for mood input.")

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            
            #Mood (Happy, Stressed, Tired)
            if "MOOD:" in line:
                current_mood = line.split(":")[1]
                print(f"Mood logged: {current_mood}. Place phone on sensor to begin.")
            
            #Phone placing (Distance < Threshold)
            elif line == "PHONE:ON":
                if current_mood is None:
                    print("Please select a mood button first")
                    continue
                
                if not is_studying:
                    print("Phone detected and study Session started.")
                    is_studying = True
                    session_start_time = time.time()
                    break_start_time = None #Cancel break
                else:
                    #Returning from break
                    if break_start_time:
                        break_duration = time.time() - break_start_time
                        print(f"Returned from break. Break lasted {int(break_duration)} seconds.")
                        break_start_time = None

            #Phone lifted (Distance > Threshold)
            elif line == "PHONE:OFF" and is_studying and not break_start_time:
                print("Phone removed. Break started. 30-minute countdown.")
                #add time to total studied
                total_studied_seconds += (time.time() - session_start_time)
                break_start_time = time.time()

        #30 minute break rule (5 seconds for demo)
        if break_start_time:
            time_on_break = time.time() - break_start_time
            if time_on_break > 5: #1800 seconds = 30 minutes
                print("30 minutes passed. Ending study session.")
                duration_minutes = max(1, int(total_studied_seconds / 60))
                save_session(duration_minutes, current_mood)
                
                #Reset all states
                current_mood = None
                session_start_time = None
                break_start_time = None
                total_studied_seconds = 0
                is_studying = False

except Exception as e:
    print(f"Error: {e}")