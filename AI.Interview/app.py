import streamlit as st
import uuid
from utils.file_parser import extract_text
from utils.experience_parser import extract_experience
from core.interview_engine import init_session, log_question_answer
from core.llm_service import generate_question, evaluate_answers
from proctoring.face_detection import capture_initial_face
from datetime import datetime, timedelta

# --- Constants ---
QUESTION_LIMIT = 3
# INTERVIEW_DURATION_MINUTES = 45
INTERVIEW_ID = str(uuid.uuid4())
# SESSION_START_TIME = datetime.now()

# --- Setup ---
st.set_page_config(page_title="AI Interview", layout="wide")

# --- Session State Init ---
if "step" not in st.session_state:
# if "interview_id" not in st.session_state:
    st.session_state.step = 0
    st.session_state.interview_id = INTERVIEW_ID
    st.session_state.report_generated = False

# interview_id = st.session_state.interview_id
# --- Init directories ---
face_dir = f"face_snapshots/{INTERVIEW_ID}"
session_file = init_session(INTERVIEW_ID)

if st.session_state.step == 0:
    # --- Upload Inputs ---
    st.title("Upload Files to Start Interview")
    jd_file = st.file_uploader("Job Description (txt/pdf/docx)")
    resume_file = st.file_uploader("Resume (txt/pdf/docx)")
    project_file = st.file_uploader("Project Requirements (txt/pdf/docx)")

    # --- Start Interview ---
    if st.button("Start Interview") and jd_file and resume_file and project_file:
        st.session_state.jd = extract_text(jd_file)
        st.session_state.resume = extract_text(resume_file)
        st.session_state.project = extract_text(project_file)
        st.session_state.experience = extract_experience(st.session_state.resume)
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    # --- Initial Face Snapshot ---
    if capture_initial_face(face_dir, INTERVIEW_ID):
        st.session_state.start_time = datetime.now()
        st.session_state.step = 2
        st.session_state.qa_log = []
        st.rerun()

# --- Interview Flow ---
elif st.session_state.step == 2:
    st.title("🧠 AI Interview")
    # --- Timer check ---
    elapsed = (datetime.now() - st.session_state.start_time).seconds
    st.markdown(f"⏱️ Time: {elapsed//60}:{elapsed%60:02d}", unsafe_allow_html=True)
    st.header(f"Experience: {st.session_state.experience} years")

    # --- Display previous QA ---
    previous_qa = st.session_state.qa_log
    for idx, qa in enumerate(previous_qa, start=1):
        st.subheader(f"Question {idx}: {qa['question']}")
        st.text(f"Answer: {qa['answer']}")

    # --- Ask next question ---
    if len(previous_qa) < QUESTION_LIMIT:
        question = generate_question(st.session_state.jd, st.session_state.resume, st.session_state.project, st.session_state.experience)
        st.subheader(f"Question {len(previous_qa)+1}")
        st.text(question)
        answer = st.text_area("Your Answer", key=f"answer_{len(previous_qa)}")
        if st.button("Submit Answer"):
            log_question_answer(INTERVIEW_ID, question, answer)
            st.session_state.qa_log.append({"question": question, "answer": answer})
            st.rerun()
    else:
        # --- Interview Report ---
        if not st.session_state.report_generated:
            # st.success("Interview complete. Generating report...")
            st.success("Interview Complete! Thank you for attending.")
            st.markdown("Please wait a few moments while your session is being saved...")
        qa_text = "\n".join([f"Q: {q['question']}\nA: {q['answer']}" for q in previous_qa])
        feedback = evaluate_answers(qa_text)
        report_path = f"reports/interview_report_{INTERVIEW_ID}.txt"
        with open(report_path, "w") as f: f.write(feedback)
        st.session_state.report_generated = True
        st.markdown("### ✅ Your session is saved.")
        st.markdown("You may now close this window.")
