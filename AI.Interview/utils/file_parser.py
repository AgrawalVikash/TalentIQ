import fitz
import docx2txt
import tempfile

def extract_text(file):
    try:
        filename = file.name.lower()
        if filename.endswith('.pdf'):
            file.seek(0)
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                return "\n".join(page.get_text() for page in doc)
        elif filename.endswith(".docx"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name
            text = docx2txt.process(tmp_path)
            return text
        elif filename.endswith(".txt"):
            file.seek(0)
            return file.read().decode("utf-8")
        else:
            raise ValueError("Unsupported file format. Please upload a PDF, DOCX, or TXT file.")
    except Exception as e:
        return f"Error extracting text: {e}"