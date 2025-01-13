import os
import shutil
from typing import List, Dict

class FileHandler:
    def __init__(self, upload_dir: str, classified_dir: str):
        self.upload_dir = upload_dir
        self.classified_dir = classified_dir
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure that upload and classified directories exist."""
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.classified_dir, exist_ok=True)

    def get_uploaded_files(self) -> List[str]:
        """Get list of all music files in upload directory."""
        if not os.path.exists(self.upload_dir):
            return []
        return [f for f in os.listdir(self.upload_dir) 
                if f.endswith(('.mp3', '.wav'))]

    def move_to_genre_folder(self, filename: str, genre: str) -> str:
        """Move a file to its genre folder and return the destination path."""
        genre_folder = os.path.join(self.classified_dir, genre)
        os.makedirs(genre_folder, exist_ok=True)
        
        source_path = os.path.join(self.upload_dir, filename)
        dest_path = os.path.join(genre_folder, filename)
        
        shutil.move(source_path, dest_path)
        return dest_path

    def clean_empty_folders(self):
        """Remove empty folders in classified directory."""
        for root, dirs, files in os.walk(self.classified_dir, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
