import os
import docx2txt
import PyPDF2

def extract_text_from_file(file_path):
    if file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    elif file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join([page.extract_text() for page in reader.pages])
    else:
        return "Unsupported file type"

def extract_from_pdf(filepath):
    text = ''
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text.strip()

import docx2txt
def extract_from_docx(filepath):
    try:
        raw_text = docx2txt.process(filepath)
        # 按行去重（保留顺序）
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        seen = set()
        deduplicated = []
        for line in lines:
            if line not in seen:
                deduplicated.append(line)
                seen.add(line)
        return '\n'.join(deduplicated)
    except Exception as e:
        print("❌ docx2txt 提取失败：", e)
        return ""

