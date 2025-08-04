import json
import os
from datetime import datetime

def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def get_session_path(interview_id, session_folder="reports"):
    ensure_dir_exists(session_folder)
    return os.path.join(session_folder, f"session_{interview_id}.json")

def get_report_path(interview_id, session_folder="reports"):
    ensure_dir_exists(session_folder)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(session_folder, f"interview_report_{interview_id}_{timestamp}.txt")

def init_session(interview_id, session_folder="reports"):
    path = get_session_path(interview_id, session_folder)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
    return path

def log_question_answer(interview_id, question, answer, session_folder="reports"):
    path = get_session_path(interview_id, session_folder)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": "question_answer",
        "question": question,
        "answer": answer
    }
    logs = []
    if os.path.exists(path):
        with open(path) as f:
            try:
                logs = json.load(f)
            except Exception:
                logs = []
    logs.append(entry)
    with open(path, "w") as f:
        json.dump(logs, f, indent=4)

def log_event(interview_id, event_type, message, extra=None, session_folder="reports"):
    path = get_session_path(interview_id, session_folder)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "message": message
    }
    if extra:
        entry.update(extra)
    logs = []
    if os.path.exists(path):
        with open(path) as f:
            try:
                logs = json.load(f)
            except Exception:
                logs = []
    logs.append(entry)
    with open(path, "w") as f:
        json.dump(logs, f, indent=4)

def load_session_log(interview_id, session_folder="reports"):
    path = get_session_path(interview_id, session_folder)
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_report(interview_id, report_text, session_folder="reports"):
    report_path = get_report_path(interview_id, session_folder)
    with open(report_path, "w") as f:
        f.write(report_text)
    return report_path