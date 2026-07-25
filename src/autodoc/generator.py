from docx import Document
from .config import TEMPLATES_PATH


def generate_document(data: dict):
    input_path = TEMPLATES_PATH / "example.docx"

    if not input_path.exists():
        raise FileExistsError(f"FILE DOES NOT EXISTS: {input_path}")

    document = Document(input_path)

    for paragraph in document.paragraphs:
        for old, new in data.items():
            if old in paragraph.text:
                paragraph.text = paragraph.text.replace(old, new)

    output_path = TEMPLATES_PATH / "document.docx"
    document.save(output_path)

    return output_path
