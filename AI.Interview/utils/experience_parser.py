import re

def extract_experience(resume_text):
    patterns = [
        r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience",           # 5 years of experience, 5+ years experience
        r"experience\s*(?:of|with)?\s*(\d+)\+?\s*(?:years?|yrs?)",      # experience of 5 years, experience with 5 years
        r"over\s*(\d+)\s*(?:years?|yrs?)\s*(?:of)?\s*experience",       # over 5 years of experience
        r"(\d+)\s*(?:years?|yrs?)['’]?\s*experience",                   # 5 years' experience
        r"(\d+)\s*(?:years?|yrs?)\s*in\s*\w+",                          # 5 years in software development
        r"worked\s*for\s*(\d+)\s*(?:years?|yrs?)",                      # worked for 5 years
        r"(\d+)\s*(?:years?|yrs?)\s*as\s*\w+",                          # 5 years as developer
    ]
    matches = set()
    for pattern in patterns:
        found = re.findall(pattern, resume_text, flags=re.IGNORECASE)
        for match in found:
            try:
                matches.add(int(match))
            except ValueError:
                continue
    return max(matches) if matches else None