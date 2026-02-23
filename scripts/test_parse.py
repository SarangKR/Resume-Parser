import requests
import json
import sys

URL = "http://localhost:8000/api/parse"

try:
    with open("Sample Resume/Resume.pdf", "rb") as f:
        files = {"file": ("Resume.pdf", f, "application/pdf")}
        response = requests.post(URL, files=files)

        print(f"Status Code: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
except FileNotFoundError:
    print("Could not find Sample Resume/Resume.pdf")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
