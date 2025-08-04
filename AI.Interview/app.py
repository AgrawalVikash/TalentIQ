import streamlit as st
import uuid
import os
import json
from PIL import Image
from datetime import datetime
from utils.file_parser import extract_text
from utils.experience_parser import extract_experience
from core.interview_engine import init_session, log_question_answer
from core.llm_service import generate_question, evaluate_answers
from proctoring.face_detection import FaceMonitor

# Constants
QUESTION_LIMIT = 3
INTERVIEW_DURATION_SECONDS = 30 * 60  # 30 minutes

# Setup
st.set_page_config(page_title="AI Interview", layout="wide")

# Session State
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.interview_id = str(uuid.uuid4())
    st.session_state.report_generated = False
    st.session_state.qa_log = []
    st.session_state.jd = None
    st.session_state.resume = None
    st.session_state.project = None
    st.session_state.experience = None
    st.session_state.start_time = None
    st.session_state.session_folder = None
    st.session_state.face_monitor = None

INTERVIEW_ID = st.session_state.interview_id

def show_file_uploads():
    st.title("Upload Files to Start Interview")
    jd_file = st.file_uploader("Job Description (txt/pdf/docx)")
    resume_file = st.file_uploader("Resume (txt/pdf/docx)")
    project_file = st.file_uploader("Project Requirements (txt/pdf/docx)")
    missing_files = not (jd_file and resume_file and project_file)

    if st.button("Next"):
        if missing_files:
            st.warning("Please upload all required files.")
        else:
            try:
                st.session_state.jd = extract_text(jd_file)
                st.session_state.resume = extract_text(resume_file)
                st.session_state.project = extract_text(project_file)
                st.session_state.experience = extract_experience(st.session_state.resume)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                session_folder = os.path.join("sessions", f"{timestamp}_{INTERVIEW_ID}")
                os.makedirs(session_folder, exist_ok=True)
                os.makedirs(os.path.join(session_folder, "snapshots"), exist_ok=True)
                st.session_state.session_folder = session_folder

                init_session(INTERVIEW_ID, session_folder)
                st.session_state.face_monitor = FaceMonitor(log_folder=session_folder)
                st.session_state.step = 1
                st.rerun()
            except Exception as e:
                st.error(f"Error processing files: {e}")

def show_face_capture():
    st.title("📸 Face Capture")
    st.info("This is how your picture will appear. Please center your face.")

    img_file = st.camera_input("Take Your Face Snapshot")

    if img_file:
        face_monitor = st.session_state.face_monitor
        # Save and process the image using FaceMonitor
        temp_path = os.path.join(face_monitor.snapshot_dir, "initial_temp.jpg")
        img = Image.open(img_file)
        img.save(temp_path)
        st.image(img, caption="Preview of your captured face")

        # Now run face detection and logging
        filename = face_monitor.capture_initial_face()
        if filename:
            st.success("✅ Face captured successfully!")
            st.session_state.start_time = datetime.now()
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Face capture failed. Please try again.")

def show_instructions():
    st.title("Interview Instructions")
    st.markdown("""
    <div style="background:#222;padding:20px;border-radius:8px;">
    <ul>
      <li>Please stay in front of the camera.</li>
      <li>Avoid switching tabs or using keyboard shortcuts.</li>
      <li>The interview will be auto-monitored for integrity.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Interview"):
        st.session_state.face_monitor.start()
        st.session_state.step = 3
        st.rerun()

def show_interview():
    st.title("🧠 AI Interview")
    elapsed = (datetime.now() - st.session_state.start_time).seconds
    remaining = INTERVIEW_DURATION_SECONDS - elapsed
    minutes = remaining // 60
    seconds = remaining % 60

    st.markdown(f"⏱️ Time Remaining: {minutes}:{seconds:02d}")

    if remaining <= 0:
        st.warning("Interview duration completed. Finalizing...")
        finalize_session()
        return

    st.header(f"Experience: {st.session_state.experience} years")
    previous_qa = st.session_state.qa_log

    for idx, qa in enumerate(previous_qa, start=1):
        st.subheader(f"Question {idx}: {qa['question']}")
        st.text(f"Answer: {qa['answer']}")

    if len(previous_qa) < QUESTION_LIMIT:
        question = generate_question(
            st.session_state.jd,
            st.session_state.resume,
            st.session_state.project,
            st.session_state.experience
        )
        st.subheader(f"Question {len(previous_qa)+1}")
        st.text(question)
        answer = st.text_area("Your Answer", key=f"answer_{len(previous_qa)}")

        if st.button("Submit Answer"):
            if not answer.strip():
                st.warning("Please enter your answer before submitting.")
            else:
                log_question_answer(INTERVIEW_ID, question, answer, st.session_state.session_folder)
                st.session_state.qa_log.append({"question": question, "answer": answer})
                st.rerun()
    else:
        finalize_session()


def finalize_session():
    if not st.session_state.report_generated:
        st.success("Interview Complete! Thank you for attending.\nPlease wait a few moments while your session is being saved...")
        st.session_state.face_monitor.stop()

        qa_list = st.session_state.qa_log
        qa_text = "\n".join([f"Q: {q['question']}\nA: {q['answer']}" for q in qa_list])
        feedback_json = evaluate_answers(qa_text)

        # Robust feedback parsing
        feedback = {}
        try:
            feedback = json.loads(feedback_json)
            # Ensure required keys exist
            if not isinstance(feedback, dict):
                raise ValueError("Feedback is not a dict")
            if "qas" not in feedback:
                # Try to extract scores if possible, else fallback
                feedback["qas"] = qa_list
            if "average_score" not in feedback:
                feedback["average_score"] = "N/A"
            if "decision" not in feedback:
                feedback["decision"] = "N/A"
            if "summary" not in feedback:
                feedback["summary"] = ""
        except Exception as e:
            # Fallback: show raw feedback and log error
            feedback = {
                "qas": qa_list,
                "average_score": "N/A",
                "decision": "N/A",
                "summary": f"Raw feedback:\n{feedback_json}\n\nError: {e}"
            }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join("reports", f"interview_report_{INTERVIEW_ID}_{timestamp}.txt")
        os.makedirs("reports", exist_ok=True)

        with open(report_path, "w") as f:
            f.write(f"InterviewID: {INTERVIEW_ID}\n")
            f.write(f"Date: {timestamp}\n\n")
            for idx, item in enumerate(feedback.get("qas", qa_list), 1):
                f.write(f"Q{idx}: {item['question']}\nA{idx}: {item['answer']}\nScore: {item.get('score', 'N/A')}\n\n")
            f.write(f"Average Score: {feedback.get('average_score', 'N/A')}\n")
            f.write(f"Decision: {feedback.get('decision', 'N/A')}\n")
            f.write(f"Summary: {feedback.get('summary', '')}\n")

        st.session_state.report_generated = True

    st.markdown("### ✅ Your session is saved.")
    st.markdown("You may now close this window.")

# Flow controller
if st.session_state.step == 0:
    show_file_uploads()
elif st.session_state.step == 1:
    show_face_capture()
elif st.session_state.step == 2:
    show_instructions()
elif st.session_state.step == 3:
    show_interview()