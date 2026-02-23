from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from ..database import Base
from datetime import datetime
import enum

class NotificationType(str, enum.Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    ASSIGNMENT = "assignment"
    GRADE = "grade"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType), default=NotificationType.INFO)
    is_read = Column(Boolean, default=False)
    link = Column(String(500))
    created_at = Column(String(50), default=lambda: datetime.utcnow().isoformat())
