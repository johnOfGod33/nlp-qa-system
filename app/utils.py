import io

from pypdf import PdfReader


def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()


def extract_text(file_bytes, file_type=None, filename=None):
    name = (filename or "").lower()

    if name.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore").strip()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if file_type == "application/pdf":
        return extract_text_from_pdf(file_bytes)
    if file_type and file_type.startswith("text/"):
        return file_bytes.decode("utf-8", errors="ignore").strip()

    # Streamlit / browsers sometimes send octet-stream or empty type for .txt
    if file_type in (None, "", "application/octet-stream"):
        if file_bytes[:4] == b"%PDF":
            return extract_text_from_pdf(file_bytes)
        return file_bytes.decode("utf-8", errors="ignore").strip()

    raise ValueError(f"Unsupported file type: {file_type}")
