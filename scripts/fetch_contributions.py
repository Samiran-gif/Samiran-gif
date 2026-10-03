import json
import requests

USERNAME = "Samiran-gif"
OUTPUT_FILE = "data/contributions.json"

url = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(url, timeout=30)
response.raise_for_status()

data = {
    "username": USERNAME,
    "html": response.text,
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(f"Contribution data saved to {OUTPUT_FILE}")