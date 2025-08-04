import cv2
import time
import os
import uuid
import json
from datetime import datetime
from threading import Thread

CAPTURE_INTERVAL = 5  # seconds

class FaceMonitor:
    def __init__(self, log_folder: str):
        self.running = False
        self.thread = None
        self.cap = None
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.snapshot_dir = os.path.join(log_folder, "snapshots")
        self.log_file = os.path.join(log_folder, "face_log.json")
        os.makedirs(self.snapshot_dir, exist_ok=True)
        os.makedirs(log_folder, exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                json.dump([], f)

    def _log_event(self, event: str, image: str = None, details: dict = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "image": image
        }
        if details:
            entry.update(details)
        with open(self.log_file, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)

    def _save_snapshot(self, frame):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uuid.uuid4().hex}.png"
        filepath = os.path.join(self.snapshot_dir, filename)
        cv2.imwrite(filepath, frame)
        return filename

    def _monitor(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                self._log_event("CameraReadFailed")
                time.sleep(CAPTURE_INTERVAL)
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            num_faces = len(faces)

            if num_faces == 0:
                self._log_event("NoFaceDetected", details={"num_faces": 0})
            elif num_faces == 1:
                filename = self._save_snapshot(frame)
                self._log_event("SingleFaceDetected", filename, {"num_faces": 1})
            else:
                filename = self._save_snapshot(frame)
                self._log_event("MultipleFacesDetected", filename, {"num_faces": num_faces})

            time.sleep(CAPTURE_INTERVAL)

    def start(self):
        if self.running:
            return  # Prevent multiple threads
        self.running = True
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self._log_event("CameraOpenFailed")
            self.running = False
            return
        self.thread = Thread(target=self._monitor, daemon=True)
        self.thread.start()
        self._log_event("CameraStarted")

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self._log_event("CameraStopped")

    def capture_initial_face(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self._log_event("InitialCameraOpenFailed")
            return None
        ret, frame = cap.read()
        cap.release()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            num_faces = len(faces)
            filename = self._save_snapshot(frame)
            if num_faces == 0:
                self._log_event("InitialNoFaceDetected", filename, {"num_faces": 0})
            elif num_faces == 1:
                self._log_event("InitialFaceCaptured", filename, {"num_faces": 1})
            else:
                self._log_event("InitialMultipleFacesDetected", filename, {"num_faces": num_faces})
            return filename
        else:
            self._log_event("InitialCameraReadFailed")
            return None