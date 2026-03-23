import io

from pypdf import PdfReader


def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()


def extract_text(file_bytes, file_type=None):
    if file_type == "application/pdf" or file_type is None:
        return extract_text_from_pdf(file_bytes)

    if file_type.startswith("text/"):
        return file_bytes.decode("utf-8", errors="ignore").strip()

    raise ValueError(f"Unsupported file type: {file_type}")
