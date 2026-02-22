import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

print("Getting the Study Session Analytics...\n")

current_folder = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(current_folder, "study_optimizer.db")

def run_analytics():
    conn = sqlite3.connect(DB_PATH)

    #1.Loading Databases
    try:
        df_profile = pd.read_sql_query("SELECT * FROM user_profile LIMIT 1", conn)
        df_logs = pd.read_sql_query("SELECT * FROM study_logs", conn)
        df_global = pd.read_sql_query("SELECT * FROM global_sleep_data", conn)
    except Exception as e:
        print("Error reading databases.")
        return

    if df_profile.empty:
        print("No user profile found. Run user_profile.py first.")
        return

    user_occupation = df_profile['occupation'].iloc[0]
    user_age = df_profile['age'].iloc[0]
    print(f"User: {user_age} year old {user_occupation}.")

    #Study pattern analysis
    if df_logs.empty:
        print("\nWaiting for physical robot data!")
    else:
        hourly_stats = df_logs.groupby('start_hour')['duration_minutes'].mean().reset_index()
        best_hour_row = hourly_stats.loc[hourly_stats['duration_minutes'].idxmax()]
        best_study_hour = int(best_hour_row['start_hour'])

        #save code to db
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        #Add column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE user_profile ADD COLUMN optimal_hour INTEGER")
        except:
            pass 
        
        cursor.execute("UPDATE user_profile SET optimal_hour = ?", (best_study_hour,))
        conn.commit()
        conn.close()
        
        print(f"Optimal focus time: You enter a flow state when starting around {best_study_hour}:00.")

        #Updated graph of last 5 sessions
        #Get last 5 rows of the dataframe
        recent_sessions = df_logs.tail(5).copy()
        
        #Date and hour for the X-axis
        recent_sessions['Session Label'] = recent_sessions['study_date'] + '\n(' + recent_sessions['start_hour'].astype(str) + ':00)'

        plt.figure(figsize=(10, 5))
        plt.bar(recent_sessions['Session Label'], recent_sessions['duration_minutes'], color='#6b9ac4')
        
        plt.title('Duration of Last 5 Study Sessions', fontsize=16)
        plt.xlabel('Session (Date & Time)', fontsize=12)
        plt.ylabel('Duration (Minutes)', fontsize=12)
        plt.xticks(rotation=0) #readability
        plt.tight_layout()
        
        #Save to static folder
        static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        os.makedirs(static_folder, exist_ok=True)
        plt.savefig(os.path.join(static_folder, "study_history.png"))
        print(f"Saved last 5 sessions to study_history.png")


#Sleep recommendation with sleep health statistics CSV
    print("\nUSING SLEEP HEALTH CSV...")
    
    if 'Mood' not in df_global.columns:
        happy_peers = pd.DataFrame() 
    else:
        #find happy/healthy people matching profile in the CSV
        happy_peers = df_global[(df_global['Occupation'] == user_occupation) & (df_global['Mood'] == 'Happy')]
        if happy_peers.empty:
            happy_peers = df_global[df_global['Mood'] == 'Happy']

    if happy_peers.empty:
        recommended_sleep_hours = 8.0
    else:
        recommended_sleep_hours = round(happy_peers['Sleep Duration'].mean(), 1)
        if pd.isna(recommended_sleep_hours):
            recommended_sleep_hours = 8.0
            
    print(f"{len(happy_peers)} 'Happy' people in the Sleep Health CSV matching your profile.")
    #Sleep recommendation (Inside analysis.py)
    #save to db
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Check if the column exists, if not, add it
    try:
        cursor.execute("ALTER TABLE user_profile ADD COLUMN sleep_recommendation REAL")
    except:
        pass

    #Update the profile with the new calculation
    cursor.execute("UPDATE user_profile SET sleep_recommendation = ?", (recommended_sleep_hours,))
    conn.commit()
    conn.close()

    print(f"Target Sleep Duration: {recommended_sleep_hours} Hours")
    print(f"(Calculated from the Sleep Health Dataset!)\n")

    conn.close()

if __name__ == "__main__":
    run_analytics()