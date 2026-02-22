import cv2
import time
from datetime import datetime
import os

def run_demo_anti_theft():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Camera not found.")
        return

    current_folder = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(current_folder, "static")
    os.makedirs(static_folder, exist_ok=True)

    out = None
    recording_end_time = 0 
    cooldown_end_time = 0  
    
    DISTANCE_THRESHOLD = 150 
    is_recording = False

    print("--- PROXIMITY THEFT DEFENSE ---")
    print(f"Videos will be saved STRICTLY to: {static_folder}")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
        
        thief_detected = False

        for (x, y, w, h) in faces:
            if w > DISTANCE_THRESHOLD:
                thief_detected = True
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                cv2.putText(frame, "BACK AWAY!", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        current_time = time.time()

        #1.Trigger
        if thief_detected and not is_recording and current_time > cooldown_end_time:
            is_recording = True
            
            height, width = frame.shape[:2]
            
           #Connection to mac web
            fourcc = cv2.VideoWriter_fourcc(*'avc1') 
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"thief_face_{timestamp}.mp4" 
            full_file_path = os.path.join(static_folder, filename) 
            
            out = cv2.VideoWriter(full_file_path, fourcc, 20.0, (width, height))
            
            if not out.isOpened():
                print("OpenCV refused to build the video file!")
            else:
                print(f"PROXIMITY ALERT! Recording started... Saving {filename}")

        if thief_detected and is_recording:
             recording_end_time = current_time + 4.0

        #2.Record and cut-off
        if is_recording:
            if current_time < recording_end_time:
                out.write(frame)
                cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1) 
            else:
                out.release()
                out = None
                is_recording = False
                cooldown_end_time = current_time + 3.0 #Reduce several videos taken due to glitch
                print("Incident saved to static folder.")

        cv2.imshow("Proximity Defense", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #Cleanup
    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_demo_anti_theft()