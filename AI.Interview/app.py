import streamlit as st
import uuid
import os
from utils.file_parser import extract_text
from utils.experience_parser import extract_experience
from core.interview_engine import init_session, log_question_answer
from core.llm_service import generate_question, evaluate_answers
from proctoring.face_detection import capture_initial_face
from datetime import datetime
import json

# --- Constants ---
QUESTION_LIMIT = 3
INTERVIEW_ID = str(uuid.uuid4())

# --- Setup ---
st.set_page_config(page_title="AI Interview", layout="wide")

# --- Session State Init ---
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.interview_id = INTERVIEW_ID
    st.session_state.report_generated = False
    st.session_state.qa_log = []
    st.session_state.jd = None
    st.session_state.resume = None
    st.session_state.project = None
    st.session_state.experience = None
    st.session_state.start_time = None

INTERVIEW_ID = st.session_state.interview_id

# --- Init directories ---
face_dir = f"face_snapshots/{INTERVIEW_ID}"
report_dir = "reports"
os.makedirs(face_dir, exist_ok=True)
os.makedirs(report_dir, exist_ok=True)
session_file = init_session(INTERVIEW_ID)

def show_file_uploads():
    st.title("Upload Files to Start Interview")
    jd_file = st.file_uploader("Job Description (txt/pdf/docx)")
    resume_file = st.file_uploader("Resume (txt/pdf/docx)")
    project_file = st.file_uploader("Project Requirements (txt/pdf/docx)")
    missing_files = not (jd_file and resume_file and project_file)
    if st.button("Start Interview"):
        if missing_files:
            st.warning("Please upload all required files.")
        else:
            try:
                st.session_state.jd = extract_text(jd_file)
                st.session_state.resume = extract_text(resume_file)
                st.session_state.project = extract_text(project_file)
                st.session_state.experience = extract_experience(st.session_state.resume)
                st.session_state.step = 1
                st.rerun()
            except Exception as e:
                st.error(f"Error processing files: {e}")

def show_face_capture():
    if capture_initial_face(face_dir, INTERVIEW_ID):
        st.session_state.start_time = datetime.now()
        st.session_state.step = 2
        st.rerun()
    else:
        st.warning("Face capture failed. Please try again.")

def show_interview():
    st.title("🧠 AI Interview")
    elapsed = (datetime.now() - st.session_state.start_time).seconds
    st.markdown(f"⏱️ Time: {elapsed//60}:{elapsed%60:02d}", unsafe_allow_html=True)
    st.header(f"Experience: {st.session_state.experience} years")

    previous_qa = st.session_state.qa_log
    for idx, qa in enumerate(previous_qa, start=1):
        st.subheader(f"Question {idx}: {qa['question']}")
        st.text(f"Answer: {qa['answer']}")

    if len(previous_qa) < QUESTION_LIMIT:
        try:
            question = generate_question(
                st.session_state.jd,
                st.session_state.resume,
                st.session_state.project,
                st.session_state.experience
            )
        except Exception as e:
            st.error(f"Error generating question: {e}")
            return
        st.subheader(f"Question {len(previous_qa)+1}")
        st.text(question)
        answer = st.text_area("Your Answer", key=f"answer_{len(previous_qa)}")
        if st.button("Submit Answer"):
            if not answer.strip():
                st.warning("Please enter your answer before submitting.")
            else:
                log_question_answer(INTERVIEW_ID, question, answer)
                st.session_state.qa_log.append({"question": question, "answer": answer})
                st.rerun()
    else:
        if not st.session_state.report_generated:
            st.success("Interview Complete! Thank you for attending.")
            st.markdown("Please wait a few moments while your session is being saved...")
            qa_text = "\n".join([f"Q: {q['question']}\nA: {q['answer']}" for q in previous_qa])
            try:
                feedback = evaluate_answers(qa_text)
                report_path = os.path.join(report_dir, f"interview_report_{INTERVIEW_ID}.txt")
                with open(report_path, "w") as f:
                    f.write(feedback)
                st.session_state.report_generated = True
            except Exception as e:
                st.error(f"Error generating report: {e}")
        if st.session_state.report_generated:
            st.markdown("### ✅ Your session is saved.")
            st.markdown("You may now close this window.")

def generate_final_report(interview_id, qa_log, report_dir):
    # Evaluate all answers at once and get scores
    prompt = "Evaluate each Q&A below. Give a score (1-10) for each answer and a final decision.\n\n"
    for idx, qa in enumerate(qa_log, 1):
        prompt += f"Q{idx}: {qa['question']}\nA{idx}: {qa['answer']}\n\n"
    prompt += "Return JSON: [{'question':..., 'answer':..., 'score':...}, ...], average_score, decision, summary"

    # Call LLM (pseudo-code, adapt to your actual API)
    response = evaluate_answers(prompt)
    try:
        result = json.loads(response)
    except Exception:
        # fallback: just write raw response
        result = {"raw": response}

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f"interview_report_{interview_id}_{timestamp}.txt")
    with open(report_path, "w") as f:
        f.write(f"InterviewID: {interview_id}\n")
        f.write(f"Date: {timestamp}\n\n")
        for item in result.get("qas", []):
            f.write(f"Q: {item['question']}\nA: {item['answer']}\nScore: {item['score']}\n\n")
        f.write(f"Average Score: {result.get('average_score', 'N/A')}\n")
        f.write(f"Decision: {result.get('decision', 'N/A')}\n")
        f.write(f"Summary: {result.get('summary', '')}\n")
    return report_path

# --- Main Flow ---
if st.session_state.step == 0:
    show_file_uploads()
elif st.session_state.step == 1:
    show_face_capture()
elif st.session_state.step == 2:
    show_interview()