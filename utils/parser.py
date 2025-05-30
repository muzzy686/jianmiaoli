import os
import pdfplumber
from docx import Document

def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.pdf':
        return extract_from_pdf(filepath)
    elif ext == '.docx':
        return extract_from_docx(filepath)
    else:
        raise ValueError("Unsupported file format")

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

