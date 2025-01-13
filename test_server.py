import requests
import os

def test_classification():
    # URL of your Flask server
    url = 'http://localhost:5000/classify'
    
    # Path to your test music file
    # Replace this with the path to an actual music file you want to test
    test_file_path = 'path_to_your_music_file.mp3'
    
    if not os.path.exists(test_file_path):
        print(f"Please place a music file at {test_file_path}")
        return
    
    # Open the file and send it to the server
    with open(test_file_path, 'rb') as file:
        files = {'file': file}
        try:
            response = requests.post(url, files=files)
            
            if response.status_code == 200:
                result = response.json()
                print("Classification successful!")
                print(f"File: {result.get('file')}")
                print(f"Genre: {result.get('genre')}")
            else:
                print(f"Error: {response.status_code}")
                print(response.json())
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the server. Make sure it's running on http://localhost:5000")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_classification()
