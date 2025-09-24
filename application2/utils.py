# utils.py
from PyPDF2 import PdfReader
import docx2txt
import streamlit as st

def get_text_from_file(uploaded_file):
    """Extracts raw text from an uploaded file (PDF or DOCX)."""
    text_content = ""
    try:
        if uploaded_file.name.endswith('.pdf'):
            pdf_reader = PdfReader(uploaded_file)
            text_content = "".join(page.extract_text() for page in pdf_reader.pages)
        elif uploaded_file.name.endswith('.docx'):
            text_content = docx2txt.process(uploaded_file)
        return text_content
    except Exception as e:
        st.error(f"Error reading file content: {e}")
        return None