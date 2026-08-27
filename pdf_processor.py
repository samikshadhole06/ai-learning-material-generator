import fitz
import re


def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded PDF file.
    
    Args:
        pdf_file: Streamlit UploadedFile object
        
    Returns:
        str: Extracted text from all pages
        
    Raises:
        Exception: If PDF cannot be opened or processed
    """
    try:
        document = fitz.open(
            stream=pdf_file.read(),
            filetype="pdf"
        )

        pages = []

        for page_num, page in enumerate(document):
            try:
                page_text = page.get_text()

                if page_text.strip():
                    pages.append(page_text)
            except Exception as e:
                print(f"Warning: Could not extract text from page {page_num + 1}: {str(e)}")
                continue

        document.close()

        if not pages:
            raise ValueError("No readable text found in PDF. The PDF may contain only images.")

        return "\n".join(pages)
        
    except Exception as e:
        raise Exception(f"Failed to process PDF: {str(e)}")


def clean_text(text):
    """
    Clean extracted PDF text.
    
    Args:
        text (str): Raw text from PDF
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Replace newlines with spaces
    text = text.replace("\n", " ")

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove special characters that might interfere
    text = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]", "", text)

    return text.strip()