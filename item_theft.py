import cv2
import time
from datetime import datetime
import os
from ultralytics import YOLO

def run_object_protection():
    print("Loading AI Model YOLO (This takes a few seconds)")
    model = YOLO("yolov8m.pt")  
    
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
    
    VALUABLES = ["laptop", "cell phone", "backpack", "suitcase", "handbag"]
    
    items_present_last_frame = False
    last_known_x = None
    is_recording = False

    print("--- VALUABLES PROTECTION ---")
    print(f"Videos will be saved to: {static_folder}")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_center = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) / 2
        results = model(frame, conf=0.6, verbose=False)
        
        items_currently_present = False
        current_x_positions = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id]
                
                if label in VALUABLES:
                    items_currently_present = True
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    center_x = (x1 + x2) / 2
                    current_x_positions.append(center_x)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"PROTECTED: {label}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        current_time = time.time()

        if items_currently_present:
             last_known_x = sum(current_x_positions) / len(current_x_positions)
             items_present_last_frame = True

        #Trigger
        if items_present_last_frame and not items_currently_present and not is_recording and current_time > cooldown_end_time:
            direction = "LEFT" if last_known_x < frame_center else "RIGHT"
            print(f"VALUABLE STOLEN! Item moved towards the {direction}!")
            
            is_recording = True
            recording_end_time = current_time + 4.0
            
            height, width = frame.shape[:2]
            
            fourcc = cv2.VideoWriter_fourcc(*'avc1') 
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"stolen_item_{direction}_{timestamp}.mp4" 
            full_file_path = os.path.join(static_folder, filename) 
            
            out = cv2.VideoWriter(full_file_path, fourcc, 20.0, (width, height))
            
            if not out.isOpened():
                print("OpenCV refused to build video file")
            else:
                print(f"VALUABLE STOLEN! Recording started. Saving {filename}")
            items_present_last_frame = False 

        #Recording
        if is_recording:
            if current_time < recording_end_time:
                out.write(frame)
                cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)
                cv2.putText(frame, "RECORDING THEFT", (50, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                out.release()
                out = None
                is_recording = False
                cooldown_end_time = current_time + 3.0 
                print("Escape Clip saved to static folder")

        cv2.imshow("Valuables Protection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_object_protection()