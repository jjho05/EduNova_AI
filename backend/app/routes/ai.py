from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..models.user import User
from ..services.auth import get_current_user
from ..services.gemini_service import create_chat_session

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
def chat_with_ai(
    chat_data: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """Chat with Gemini AI"""
    chat_session = create_chat_session()
    
    try:
        response = chat_session.send_message(chat_data.message)
        return {"response": response.text}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
