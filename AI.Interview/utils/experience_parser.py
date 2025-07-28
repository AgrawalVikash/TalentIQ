import re

def extract_experience(resume_text):
    patterns = [
        r"(\d+)\+?\s*(years|yrs)\s*(of)?\s*experience",
        r"experience\s*of\s*(\d+)\s*(years|yrs)",
        r"(\d+)\s*(years|yrs)\s*experience"
    ]
    matches = []
    for pattern in patterns:
        found = re.findall(pattern, resume_text, flags=re.IGNORECASE)
        for match in found:
            matches.append(int(match[0]))
    return max(matches) if matches else 2
