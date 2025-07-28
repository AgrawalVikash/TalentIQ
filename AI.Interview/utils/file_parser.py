import fitz
import docx2txt

def extract_text(file):
    if file.name.endswith('.pdf'):
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            return "\n".join(page.get_text() for page in doc)
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    else:
        return file.read().decode("utf-8")