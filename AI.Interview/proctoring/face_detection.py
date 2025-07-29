import streamlit as st
import os
from PIL import Image
from datetime import datetime
import json
import cv2
import numpy as np

def capture_initial_face(face_dir, interview_id):
    st.title("📸 Face Capture")
    st.info("This is how your picture will appear. Please center your face.")

    img_file = st.camera_input("Take Your Face Snapshot")

    if img_file:
        os.makedirs(face_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"{face_dir}/initial_{timestamp}.jpg"
        img = Image.open(img_file)
        img.save(path)

        log_event(face_dir, interview_id, "initial_face_capture", "Initial face captured", path)

        st.success("✅ Face captured successfully!")
        return True
    return False

def log_event(face_dir, interview_id, event_type, message, snapshot_file=None):
    log_path = os.path.join(face_dir, "face_events.json")
    log = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "message": message,
        "snapshot_file": snapshot_file
    }
    logs = []
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try: logs = json.load(f)
            except: logs = []
    logs.append(log)
    with open(log_path, "w") as f:
        json.dump(logs, f, indent=4)
        
def detect_faces(pil_img):
    try:
        img = np.array(pil_img.convert('RGB'))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if face_cascade.empty():
            print(f"Error: Haar cascade not loaded from {cascade_path}")
            return 0
        faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
        return len(faces)
    except Exception as e:
        print(f"Face detection error: {e}")
        return 0
        
def capture_frequent_face(face_dir, interview_id):
    img_file = st.camera_input("Take Snapshot")
    if img_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"{face_dir}/snapshot_{timestamp}.jpg"
        img = Image.open(img_file)
        img.save(path)
        face_count = detect_faces(img)
        if face_count == 0:
            log_event(face_dir, interview_id, "face_capture", "No face detected", path)
        elif face_count > 1:
            log_event(face_dir, interview_id, "face_capture", "Multiple faces detected", path)
        else:
            log_event(face_dir, interview_id, "face_capture", "Face captured", path)
