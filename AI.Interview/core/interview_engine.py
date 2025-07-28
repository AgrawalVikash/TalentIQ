# import streamlit as st
# import pandas as pd
# import json
# import os
# from datetime import datetime, timedelta
# from utils import file_parser, experience_parser
# from core import llm_service

# QUESTION_LIMIT = 3
# DURATION_MIN = 45

# def get_session_log_file(interview_id):
#     os.makedirs("session_logs", exist_ok=True)
#     return f"session_logs/interview_{interview_id}.json"

# def log_session_update(interview_id, qa_entry):
#     log_file = get_session_log_file(interview_id)
#     logs = []
#     if os.path.exists(log_file):
#         with open(log_file, "r") as f:
#             try:
#                 logs = json.load(f)
#             except:
#                 logs = []
#     logs.append(qa_entry)
#     with open(log_file, "w") as f:
#         json.dump(logs, f, indent=4)

# def load_session_log(interview_id):
#     log_file = get_session_log_file(interview_id)
#     if os.path.exists(log_file):
#         with open(log_file, "r") as f:
#             return json.load(f)
#     return []

# # --- Session State Init ---
# def start_interview(interview_id, face_dir, report_dir):
#     if "step" not in st.session_state:
#         st.session_state.step = 0
#         # st.session_state.qa_log = []
#         # st.session_state.interview_id = INTERVIEW_ID
#         # st.session_state.start_time = SESSION_START_TIME
#         st.session_state.start_time = datetime.now()
#         # st.session_state.current_answer = ""
#         st.session_state.report_generated = False

#     # --- Upload Inputs ---
#     jd_file = st.file_uploader("Upload Job Description", type=["txt", "pdf", "docx"])
#     resume_file = st.file_uploader("Upload Resume", type=["txt", "pdf", "docx"])
#     project_file = st.file_uploader("Upload Project Requirements", type=["txt", "pdf", "docx"])

#     # --- Start Interview ---
#     if st.button("Start Interview") and jd_file and resume_file and project_file:
#         jd = file_parser.extract_text(jd_file)
#         resume = file_parser.extract_text(resume_file)
#         project = file_parser.extract_text(project_file)
#         experience = experience_parser.extract_experience(resume)
#         st.session_state.jd, st.session_state.resume, st.session_state.project, st.session_state.exp = jd, resume, project, experience
#         # st.session_state.jd_text = jd_text
#         # st.session_state.resume_text = resume_text
#         # st.session_state.project_text = project_text
#         # st.session_state.experience = experience
#         st.session_state.step = 1
#         # st.session_state.qa_log = []
#         st.session_state.start_time = datetime.now()
#         # st.session_state.current_answer = ""
#         # Reset session log
#         log_session_update(interview_id, {"event": "interview_started", "timestamp": datetime.now().isoformat()})

#     # --- Interview Flow ---
#     if st.session_state.step == 1:
#         # --- Timer check ---
#         elapsed = datetime.now() - st.session_state.start_time
#         remaining_time = timedelta(minutes=DURATION_MIN) - elapsed

#         if remaining_time.total_seconds() <= 0:
#             st.warning("Interview time is over.")
#             st.session_state.step = 2
#         else:
#             # st.info(f"⏳ Time Remaining: {str(remaining_time).split('.')[0]}")
#             st.info(f"⏳ Time Remaining: {remaining_time}")

#             qa_log = load_session_log(interview_id)
#             question_count = sum(1 for q in qa_log if "question" in q)

#             # --- Display previous QA ---
#             # if st.session_state.qa_log:
#             #     st.subheader("Interview Round 1")
#             #     for i, qa in enumerate(st.session_state.qa_log, start=1):
#             #         st.markdown(f"**Q{i}:** {qa['Question']}")
#             #         st.markdown(f"**A{i}:** {qa['Answer']}")
#             #         # st.markdown(f"**Score:** {qa['Score']}")
#             #         st.markdown("---")

#             # --- Ask next question ---
#             if question_count < QUESTION_LIMIT:
#             # if len(st.session_state.qa_log) < QUESTION_LIMIT:
#                 question = llm_service.generate_question(
#                     st.session_state.jd,
#                     st.session_state.resume,
#                     st.session_state.project,
#                     st.session_state.exp
#                 )
#                 st.write(f"**Question {question_count + 1}: {question}**")
#                 ans = st.text_area("Answer:")

#                 # st.session_state.current_question = question
#                 # st.session_state.current_answer = ""

#                 # st.subheader(f"Question {len(st.session_state.qa_log) + 1}")
#                 # st.markdown(f"**{question}**")
#                 # # remove value
#                 # answer = st.text_area("Your Answer", value=st.session_state.current_answer, key=f"answer_{len(st.session_state.qa_log)}")

#                 if st.button("Submit Answer"):
#                     entry = {
#                         "question": question,
#                         "answer": ans,
#                         "timestamp": datetime.now().isoformat()
#                     }
#                     log_session_update(interview_id, entry)
                    
#                     # st.session_state.qa_log.append({
#                     #     "Question": question,
#                     #     "Answer": answer
#                     # })

#                     # # --- Save progress to Excel --- 
#                     # df = pd.DataFrame(st.session_state.qa_log)
#                     # excel_path = f"interview_{st.session_state.interview_id}.xlsx"
#                     # df.to_excel(excel_path, index=False)

#                     # if len(st.session_state.qa_log) >= QUESTION_LIMIT:
#                     #     st.session_state.step = 2
#                     # else:
#                     st.rerun()
#                 else:
#                     st.session_state.step = 2

#     # --- Interview Report ---
#     if st.session_state.step == 2:
#         if not st.session_state.report_generated:
#             st.success("Interview Complete! Thank you for attending.")
#             st.markdown("Please wait a few moments while your session is being saved...")
            
#             qa_data = load_session_log(interview_id)
#             qa_entries = [q for q in qa_data if "question" in q]
#             if not qa_entries:
#                 st.warning("No valid Q&A found to evaluate.")
#                 st.stop()

#             df = pd.DataFrame(qa_entries)
#             df["score"] = [llm_service.evaluate_answer(q, a) for q, a in zip(df["question"], df["answer"])]
#             avg_score = df["score"].mean()
#             feedback = llm_service.generate_feedback(df)

#             decision = "✅ Promote to next round" if avg_score >= 6 else "❌ Reject"
#             report_name = f"{report_dir}/report_{interview_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

#             with open(report_name, "w") as f:
#                 f.write(f"Interview ID: {interview_id}\n")
#                 f.write(f"Average Score: {avg_score:.2f}\nDecision: {decision}\n\n")
#                 for idx, row in df.iterrows():
#                     f.write(f"Q{idx+1}: {row['question']}\n")
#                     f.write(f"A{idx+1}: {row['answer']}\n")
#                     f.write(f"Score: {row['score']}\n\n")
#                 f.write("Feedback Summary:\n")
#                 f.write(feedback)
#             # excel_path = f"interview_{st.session_state.interview_id}.xlsx"
#             # df = pd.read_excel(excel_path)

#             # scores = []
#             # for _, row in df.iterrows():
#             #     score = llm_service.evaluate_answer(row['Question'], row['Answer'])
#             #     scores.append(score)
#             # df['Score'] = scores

#             # avg_score = df['Score'].mean()
#             # feedback = llm_service.generate_feedback(df)
#             # decision = "Promote to next round" if avg_score >= 6 else "Reject"

#             # # --- Save feedback report with Q/A and scores ---
#             # report_lines = [
#             #     f"Interview ID: {st.session_state.interview_id}",
#             #     f"Average Score: {avg_score:.2f}",
#             #     f"Decision: {decision}\n",
#             #     "Detailed Answers and Scores:"
#             # ]
#             # for i, row in df.iterrows():
#             #     report_lines.append(f"Q{i+1}: {row['Question']}")
#             #     report_lines.append(f"A{i+1}: {row['Answer']}")
#             #     report_lines.append(f"Score: {row['Score']}\n")

#             # report_lines.append("Feedback:")
#             # report_lines.append(feedback)

#             # report_text = "\n".join(report_lines)
#             # report_path = f"interview_report_{st.session_state.interview_id}.txt"
#             # with open(report_path, "w") as report_file:
#             #     report_file.write(report_text)

#             # # Clean up Excel file
#             # if os.path.exists(excel_path):
#             #     try:
#             #         os.remove(excel_path)
#             #     except Exception as e:
#             #         pass

#             st.session_state.report_generated = True
#             st.success("### ✅ Your session is saved.")
#             st.write("You may now close this window.")

import json
import os
from datetime import datetime

def init_session(interview_id):
    os.makedirs("reports", exist_ok=True)
    path = f"reports/session_{interview_id}.json"
    with open(path, "w") as f: json.dump([], f)
    return path

def log_question_answer(interview_id, question, answer):
    path = f"reports/session_{interview_id}.json"
    entry = {"timestamp": datetime.now().isoformat(), "question": question, "answer": answer}
    logs = []
    if os.path.exists(path):
        with open(path) as f:
            try: logs = json.load(f)
            except: logs = []
    logs.append(entry)
    with open(path, "w") as f:
        json.dump(logs, f, indent=4)

