import pdfplumber
import re

def process_pdf(file_path: str) -> str:
    """
    Extract text from PDF file using pdfplumber
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")
    
    # Clean text
    text = re.sub(r'\s+', ' ', text)
    return text