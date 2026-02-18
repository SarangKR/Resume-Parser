import requests
import os

# Ensure file exists
file_path = "../Resume.pdf"
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit(1)

url = "http://localhost:8000/parse"
try:
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
        
    if response.status_code == 200:
        print("Success!")
        print(response.json())
    else:
        print(f"Failed: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
