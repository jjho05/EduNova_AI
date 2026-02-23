"""
Storage provider abstraction for file handling.
Supports local storage (development) and S3 (production).
"""
import os
import aiofiles
from abc import ABC, abstractmethod
from typing import BinaryIO, Union
from fastapi import UploadFile
import logging

logger = logging.getLogger(__name__)

class StorageProvider(ABC):
    """Abstract base class for storage providers"""
    
    @abstractmethod
    async def save_file(self, file: Union[UploadFile, BinaryIO], path: str) -> str:
        """Save file and return the saved path"""
        pass
    
    @abstractmethod
    def get_file_path(self, path: str) -> str:
        """Get full path to file"""
        pass
    
    @abstractmethod
    def delete_file(self, path: str) -> bool:
        """Delete file"""
        pass
    
    @abstractmethod
    def file_exists(self, path: str) -> bool:
        """Check if file exists"""
        pass


class LocalStorage(StorageProvider):
    """Local filesystem storage for development"""
    
    def __init__(self, base_path: str = "uploads"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)
    
    async def save_file(self, file: Union[UploadFile, BinaryIO], path: str) -> str:
        """Save file to local filesystem asynchronously"""
        full_path = os.path.join(self.base_path, path)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write file
        try:
            async with aiofiles.open(full_path, "wb") as f:
                if isinstance(file, UploadFile):
                    while content := await file.read(1024 * 1024):  # 1MB chunks
                        await f.write(content)
                else:
                    # Fallback for sync BinaryIO (should be avoided in async context)
                    await f.write(file.read())
            return full_path
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise e
    
    def get_file_path(self, path: str) -> str:
        """Get full path to file"""
        return os.path.join(self.base_path, path)
    
    def delete_file(self, path: str) -> bool:
        """Delete file from filesystem"""
        try:
            full_path = self.get_file_path(path)
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
            return False
        except Exception:
            return False
    
    def file_exists(self, path: str) -> bool:
        """Check if file exists"""
        full_path = self.get_file_path(path)
        return os.path.exists(full_path)


def get_storage() -> StorageProvider:
    """
    Factory function to get storage provider based on environment.
    Returns LocalStorage for development, S3Storage for production.
    """
    env = os.getenv('ENVIRONMENT', 'local')
    
    if env == 'production':
        # TODO: Implement S3Storage when deploying
        # from .s3_storage import S3Storage
        # return S3Storage()
        pass
    
    return LocalStorage()

