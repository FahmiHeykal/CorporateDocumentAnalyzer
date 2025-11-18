import os
import tempfile
import uuid
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FileUtils:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.upload_dir = os.path.join(self.temp_dir, "corporate_docs")
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def save_uploaded_file(self, uploaded_file) -> str:
        try:
            file_extension = Path(uploaded_file.name).suffix
            file_name = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(self.upload_dir, file_name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            logger.info(f"File saved: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"File save failed: {str(e)}")
            raise
    
    def cleanup_file(self, file_path: str):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File cleaned up: {file_path}")
        except Exception as e:
            logger.error(f"File cleanup failed: {str(e)}")
    
    def get_file_size(self, file_path: str) -> int:
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            logger.error(f"File size check failed: {str(e)}")
            return 0
    
    def get_file_extension(self, file_path: str) -> str:
        return Path(file_path).suffix.lower()
    
    def is_valid_file_type(self, file_path: str) -> bool:
        valid_extensions = {'.pdf', '.docx'}
        file_ext = self.get_file_extension(file_path)
        return file_ext in valid_extensions
    
    def create_directory(self, directory_path: str):
        os.makedirs(directory_path, exist_ok=True)