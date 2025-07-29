import json
import os
from datetime import datetime

def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def init_session(interview_id):
    ensure_dir_exists("reports")
    path = f"reports/session_{interview_id}.json"
    with open(path, "w") as f:
        json.dump([], f)
    return path

def log_question_answer(interview_id, question, answer):
    path = f"reports/session_{interview_id}.json"
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

def log_event(interview_id, event_type, message, extra=None):
    path = f"reports/session_{interview_id}.json"
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

def load_session_log(interview_id):
    path = f"reports/session_{interview_id}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_report(interview_id, report_text):
    ensure_dir_exists("reports")
    report_path = f"reports/interview_report_{interview_id}.txt"
    with open(report_path, "w") as f:
        f.write(report_text)
    return report_path