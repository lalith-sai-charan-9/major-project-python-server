import os
import librosa
import numpy as np
import tensorflow as tf
from tensorflow.image import resize
import requests
import tempfile

class MusicGenreClassifier:
    def __init__(self, model_path):
        # Google Drive direct download link
        model_url = "https://drive.google.com/uc?export=download&id=1iBu-jwUSmNSZaWzQcqhOiCXlU6zNLJu4"
        
        # Create a temporary directory if it doesn't exist
        os.makedirs('tmp', exist_ok=True)
        local_model_path = os.path.join('tmp', 'model.h5')
        
        # Download the model if it doesn't exist
        if not os.path.exists(local_model_path):
            print("Downloading model...")
            response = requests.get(model_url)
            with open(local_model_path, 'wb') as f:
                f.write(response.content)
            print("Model downloaded successfully!")
        
        self.model = tf.keras.models.load_model(local_model_path)
        self.classes = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

    def load_and_preprocess_data(self, file_path, target_shape=(150, 150)):
        data = []
        audio_data, sample_rate = librosa.load(file_path, sr=None)

        chunk_duration = 4  # seconds
        overlap_duration = 2  # seconds
        chunk_samples = chunk_duration * sample_rate
        overlap_samples = overlap_duration * sample_rate

        num_chunks = int(np.ceil((len(audio_data) - chunk_samples) / (chunk_samples - overlap_samples))) + 1

        for i in range(num_chunks):
            start = i * (chunk_samples - overlap_samples)
            end = start + chunk_samples
            chunk = audio_data[start:end]
            mel_spectrogram = librosa.feature.melspectrogram(y=chunk, sr=sample_rate)
            mel_spectrogram = resize(np.expand_dims(mel_spectrogram, axis=-1), target_shape)
            data.append(mel_spectrogram)

        return np.array(data)

    def predict_genre(self, file_path):
        """Predict the genre of a music file."""
        X_test = self.load_and_preprocess_data(file_path)
        y_pred = self.model.predict(X_test)
        predicted_categories = np.argmax(y_pred, axis=1)
        unique_elements, counts = np.unique(predicted_categories, return_counts=True)
        max_count = np.max(counts)
        max_elements = unique_elements[counts == max_count]
        return self.classes[max_elements[0]]
