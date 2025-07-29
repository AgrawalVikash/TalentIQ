from openai import OpenAI
import random

client = OpenAI(api_key="")

def generate_question(jd, resume, project, experience):
    """
    Generate a smart interview question based on candidate's experience and provided documents.
    """
    if experience is None:
        level = "basic"
    elif experience <= 2:
        level = "basic"
    elif experience <= 5:
        level = "intermediate"
    else:
        level = "advanced"

    question_types = [
        "technical",
        "behavioral",
        "situational",
        "problem-solving"
    ]
    chosen_type = random.choice(question_types)

    prompt = f"""
    You are an expert interviewer. Based on the following:
    - Job Description: {jd}
    - Resume: {resume}
    - Project Requirements: {project}
    - Candidate experience: {experience} years

    Ask a {level} {chosen_type} interview question that is relevant to the candidate's background and the job requirements.
    Make sure the question is clear, concise, and challenging for the candidate's experience level.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating question: {e}"

def evaluate_answers(qa_log):
    """
    Evaluate the candidate's answers and provide a detailed hiring recommendation.
    """
    prompt = f"""
    You are a senior technical interviewer.
    Evaluate the following Q&A session:

    {qa_log}

    Please provide:
    - A summary of the candidate's strengths
    - Weaknesses or gaps observed
    - Areas for improvement
    - A fair and detailed hiring recommendation (hire/no hire and why)
    Format your response in clear bullet points.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error evaluating answers: {e}"

def generate_feedback(df):
    """
    Generate a detailed feedback report based on the interview Q&A.
    """
    questions = "\n".join(df["Question"])
    answers = "\n".join(df["Answer"])
    prompt = f"""
    Based on the following interview questions and candidate answers, provide a detailed performance feedback report.

    Questions:
    {questions}

    Answers:
    {answers}

    Please include:
    - Strengths
    - Weaknesses
    - Areas of improvement
    - Overall impression
    - Recommendation for hiring (with justification)
    Format your feedback in clear sections.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating feedback: {e}"