"""
Documents routes - File upload and management
"""
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4

from ..database import get_db
from ..models.user import User
from ..models.document import Document, DocumentType
from ..schemas.document import DocumentResponse
from ..auth import get_current_user
from ..config.storage import get_storage
from ..utils.file_validator import validate_upload_file, get_file_extension

router = APIRouter()


@router.post("/documents/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    document_type: DocumentType = Form(DocumentType.OTHER),
    course_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document (PDF, image, etc.)
    """
    # Validate file
    is_valid, error_msg = validate_upload_file(file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Get storage provider
    storage = get_storage()
    
    # Generate file path
    file_ext = get_file_extension(file.filename)
    file_id = str(uuid4())
    
    if course_id:
        file_path = f"documents/{course_id}/{file_id}.{file_ext}"
    else:
        file_path = f"documents/general/{current_user.id}/{file_id}.{file_ext}"
    
    # Save file
    try:
        saved_path = await storage.save_file(file, file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar archivo: {str(e)}")
    
    # Get file size
    file_size = 0
    if hasattr(file.file, 'seek') and hasattr(file.file, 'tell'):
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset
    
    # Create document record
    document = Document(
        id=file_id,
        user_id=current_user.id,
        course_id=course_id,
        name=name,
        description=description,
        document_type=document_type,
        file_path=saved_path,
        file_type=file_ext,
        file_size=file_size,
        processed=False
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return document


@router.get("/documents", response_model=List[DocumentResponse])
async def get_my_documents(
    course_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all documents for current user, optionally filtered by course
    """
    query = db.query(Document).filter(Document.user_id == current_user.id)
    
    if course_id:
        query = query.filter(Document.course_id == course_id)
    
    documents = query.order_by(Document.created_at.desc()).all()
    return documents


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific document
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    return document


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a document
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    # Delete file from storage
    storage = get_storage()
    storage.delete_file(document.file_path)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Documento eliminado"}


@router.post("/documents/{document_id}/process")
async def process_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Process a document with AI to extract information
    """
    from ..services.document_processor import DocumentProcessor
    
    # Get document
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    if document.processed:
        return {"message": "Documento ya procesado", "data": document.extracted_text}
    
    # Process document
    processor = DocumentProcessor()
    result = await processor.process_document(
        document.file_path,
        document.document_type.value
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando documento: {result.get('error')}"
        )
    
    # Update document
    document.extracted_text = result.get("extracted_text", "")
    document.processed = True
    db.commit()
    
    return {
        "message": "Documento procesado exitosamente",
        "data": result
    }


@router.post("/documents/{document_id}/process-curriculum")
async def process_curriculum_document(
    document_id: str,
    curriculum_name: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Process a curriculum document and automatically create courses
    """
    from ..services.curriculum_processor import CurriculumProcessor
    
    # Get document
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id,
        Document.document_type == DocumentType.CURRICULUM
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Documento de retícula no encontrado")
    
    # Process curriculum
    processor = CurriculumProcessor(db)
    result = await processor.process_curriculum(
        document.file_path,
        current_user.id,
        curriculum_name
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando retícula: {result.get('error')}"
        )
    
    # Mark document as processed
    document.processed = True
    db.commit()
    
    return {
        "message": f"Retícula procesada. {result['courses_created']} materias creadas.",
        "data": result
    }


@router.post("/documents/{document_id}/process-syllabus")
async def process_syllabus_document(
    document_id: str,
    course_id: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Process a syllabus document and automatically create modules
    """
    from ..services.syllabus_processor import SyllabusProcessor
    from ..services.gemini_vision_service import GeminiVisionService
    from ..services.pdf_extractor import PDFExtractor
    
    # Get document
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id,
        Document.document_type == DocumentType.SYLLABUS
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Documento de programa no encontrado")
    
    # Check if it's a scanned PDF
    pdf_extractor = PDFExtractor()
    is_scanned = pdf_extractor.is_scanned_pdf(document.file_path)
    
    # If scanned, use Gemini Vision
    if is_scanned:
        vision_service = GeminiVisionService()
        extracted_text = vision_service.process_scanned_pdf(document.file_path)
        
        # Save extracted text
        document.extracted_text = extracted_text
        db.commit()
    
    # Process syllabus
    processor = SyllabusProcessor(db)
    result = await processor.process_syllabus_complete(
        document.file_path,
        course_id
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando programa: {result.get('error')}"
        )
    
    # Mark document as processed
    document.processed = True
    db.commit()
    
    return {
        "message": f"Programa procesado. {result['modules_created']} módulos creados.",
        "data": result,
        "used_ocr": is_scanned
    }
