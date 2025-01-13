# Music Genre Classification API

An AI-powered web application that automatically classifies music files into genres using deep learning.

## Features

- Automatic music genre classification
- Support for MP3 and WAV files
- Batch processing of multiple files
- Organized file storage by genre
- RESTful API endpoints

## Project Structure

```
major_project/
├── src/
│   ├── api/
│   │   └── routes.py      # API endpoints
│   ├── models/
│   │   └── classifier.py  # Music genre classifier
│   └── utils/
│       └── file_handler.py # File management utilities
├── uploads/               # Temporary storage for uploaded files
├── classified/           # Organized music files by genre
├── Trained_model.h5      # Pre-trained model
├── app.py               # Main application file
└── requirements.txt     # Project dependencies
```

## Installation

1. Create a Python 3.10 virtual environment:
   ```bash
   python -m venv venv310
   source venv310/bin/activate  # On Windows: venv310\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:
   ```bash
   python app.py
   ```

2. The server provides two main endpoints:
   - `POST /classify`: Classify a single music file
   - `GET /classify-all`: Process all files in the uploads folder

3. Files will be automatically organized into genre-specific folders in the `classified` directory.

## API Endpoints

### POST /classify
Upload and classify a single music file.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (mp3 or wav)

**Response:**
```json
{
    "success": true,
    "file": "song.mp3",
    "genre": "rock",
    "location": "classified/rock/song.mp3"
}
```

### GET /classify-all
Process all files in the uploads directory.

**Response:**
```json
{
    "success": true,
    "results": [
        {
            "file": "song1.mp3",
            "genre": "jazz",
            "status": "success",
            "location": "classified/jazz/song1.mp3"
        }
    ]
}
```

## Development

The project is organized into modules:
- `src/models/classifier.py`: Handles music classification logic
- `src/utils/file_handler.py`: Manages file operations
- `src/api/routes.py`: Defines API endpoints

## License

MIT License
