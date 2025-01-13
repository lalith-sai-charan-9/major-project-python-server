from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import logging
import os
import sys
import threading
import time
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.classifier import MusicGenreClassifier
from src.utils.file_handler import FileHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
api = Blueprint('api', __name__)

# Initialize classifier and file handler
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Trained_model.h5')
classifier = MusicGenreClassifier(model_path)
file_handler = FileHandler('uploads', 'classified')

def cleanup_file(file_path, delay=180):  # 3 minutes delay
    """Delete a file after a specified delay."""
    def delete():
        time.sleep(delay)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up file {file_path}: {str(e)}")
    
    thread = threading.Thread(target=delete)
    thread.start()

@api.route('/')
def home():
    """Home endpoint."""
    return jsonify({
        "message": "Welcome to the Music Genre Classification API!",
        "endpoints": {
            "/classify": "POST - Classify a single music file",
            "/classify-all": "GET - Classify all files in uploads folder",
            "/classify-batch": "POST - Classify multiple files in a single request"
        }
    })

@api.route('/classify', methods=['POST'])
def classify_single():
    """Classify a single uploaded file."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and (file.filename.endswith(".mp3") or file.filename.endswith(".wav")):
        filename = secure_filename(file.filename)
        file_path = os.path.join(file_handler.upload_dir, filename)
        
        try:
            # Ensure upload directory exists
            os.makedirs(file_handler.upload_dir, exist_ok=True)
            
            file.save(file_path)
            genre = classifier.predict_genre(file_path)
            
            # Schedule file cleanup
            cleanup_file(file_path)
            
            return jsonify({
                "success": True,
                "file": filename,
                "genre": genre
            }), 200
            
        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            return jsonify({
                "success": False,
                "error": "Error processing file",
                "details": str(e)
            }), 500
    else:
        return jsonify({"error": "Unsupported file format"}), 400

@api.route('/classify-batch', methods=['POST'])
def classify_batch():
    """Classify multiple files in a single request."""
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400

    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({"error": "No selected files"}), 400

    results = []
    for file in files:
        if file and (file.filename.endswith(".mp3") or file.filename.endswith(".wav")):
            filename = secure_filename(file.filename)
            file_path = os.path.join(file_handler.upload_dir, filename)
            
            try:
                # Ensure upload directory exists
                os.makedirs(file_handler.upload_dir, exist_ok=True)
                
                file.save(file_path)
                genre = classifier.predict_genre(file_path)
                
                # Schedule file cleanup
                cleanup_file(file_path)
                
                results.append({
                    "file": filename,
                    "genre": genre,
                    "status": "success"
                })
                
            except Exception as e:
                logger.error(f"Error processing {filename}: {str(e)}")
                results.append({
                    "file": filename,
                    "error": str(e),
                    "status": "error"
                })
        else:
            results.append({
                "file": file.filename,
                "error": "Unsupported file format",
                "status": "error"
            })

    return jsonify({
        "success": True,
        "results": results
    }), 200

@api.route('/classify-all', methods=['GET'])
def classify_all():
    """Classify all files in the uploads folder."""
    try:
        results = []
        for filename in file_handler.get_uploaded_files():
            file_path = os.path.join(file_handler.upload_dir, filename)
            try:
                genre = classifier.predict_genre(file_path)
                dest_path = file_handler.move_to_genre_folder(filename, genre)
                
                results.append({
                    "file": filename,
                    "genre": genre,
                    "status": "success",
                    "location": dest_path
                })
                logger.info(f"Classified {filename} as {genre}")
                
            except Exception as e:
                logger.error(f"Error processing {filename}: {str(e)}")
                results.append({
                    "file": filename,
                    "error": str(e),
                    "status": "error"
                })
        
        file_handler.clean_empty_folders()
        return jsonify({
            "success": True,
            "results": results
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Error processing files",
            "details": str(e)
        }), 500
