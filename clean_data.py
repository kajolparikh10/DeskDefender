import pandas as pd
import os

current_folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_folder, 'Sleep_health_and_lifestyle_dataset.csv')
df = pd.read_csv(csv_path)

#Fix None BMI, and Blood Pressure
df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')
df['BMI Category'] = df['BMI Category'].replace('Normal Weight', 'Normal')

df[['Blood Pressure (Systolic)', 'Blood Pressure (Diastolic)']] = df['Blood Pressure'].str.split('/', expand=True)
df['Blood Pressure (Systolic)'] = df['Blood Pressure (Systolic)'].astype(int)
df['Blood Pressure (Diastolic)'] = df['Blood Pressure (Diastolic)'].astype(int)
df = df.drop(columns=['Blood Pressure', 'Person ID'])

#Add mood assessment ranges
def categorize_mood(row):
    if row['Stress Level'] >= 7:
        return "Stressed"
    elif row['Quality of Sleep'] <= 5:
        return "Tired"
    else:
        return "Happy"

df['Mood'] = df.apply(categorize_mood, axis=1)

clean_filename = 'cleaned_sleep_data.csv'
clean_path = os.path.join(current_folder, clean_filename)
df.to_csv(clean_path, index=False)

print(f"'Mood' column added to match the physical robot buttons.")
print(f"Total people saved: {len(df)}")
print(f"Saved directly to: {clean_path}")