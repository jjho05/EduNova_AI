"""
File validation utilities
"""
from typing import List, Tuple
from fastapi import UploadFile, HTTPException


ALLOWED_EXTENSIONS = {
    'pdf': ['application/pdf'],
    'image': ['image/jpeg', 'image/jpg', 'image/png'],
    'document': [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_file_type(file: UploadFile, allowed_types: List[str]) -> bool:
    """Validate file MIME type"""
    if not file.content_type:
        return False
    
    for file_type in allowed_types:
        if file.content_type in ALLOWED_EXTENSIONS.get(file_type, []):
            return True
    
    return False


def validate_file_size(file: UploadFile, max_size: int = MAX_FILE_SIZE) -> bool:
    """Validate file size"""
    try:
        # Move to the end of file to get size
        file.file.seek(0, 2)
        file_size = file.file.tell()
        
        # Reset file pointer to beginning
        file.file.seek(0)
        
        if file_size > max_size:
            return False
            
        return True
    except Exception:
        # If we can't determine size, fail safe
        return False


def validate_upload_file(
    file: UploadFile,
    allowed_types: List[str] = ['pdf', 'image', 'document'],
    max_size: int = MAX_FILE_SIZE
) -> Tuple[bool, str]:
    """
    Validate uploaded file.
    Returns (is_valid, error_message)
    """
    # Check file type
    if not validate_file_type(file, allowed_types):
        return False, f"Tipo de archivo no permitido. Permitidos: {', '.join(allowed_types)}"
    
    # Check file size
    if not validate_file_size(file, max_size):
        return False, f"Archivo muy grande. Máximo: {max_size / 1024 / 1024}MB"
    
    return True, ""


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return filename.split('.')[-1].lower() if '.' in filename else ''
