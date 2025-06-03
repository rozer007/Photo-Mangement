import os
from uuid import uuid4

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_photo(file) -> str:
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    file_content=file.file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    size= round(file.size / (1024 * 1024), 2)
    return file_path,size

# def get_photo_url(file_path: str) -> str:
#     return f"{file_path}" 