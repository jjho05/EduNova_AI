from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: str
    title: str
    message: str
    notification_type: str = "info"
    link: Optional[str] = None

class NotificationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    notification_type: str
    is_read: bool
    link: Optional[str]
    created_at: str
    
    class Config:
        from_attributes = True

class NotificationUpdate(BaseModel):
    is_read: bool
