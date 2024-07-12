import requests

BASE_URL = "https://api.scripture.api.bible/v1"

def get_bible_versions(api_key):
    url = f"{BASE_URL}/bibles"
    headers = {
        "api-key": api_key
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()["data"]
        versions = [
            {
                "name": item["name"],
                "id": item["id"],
                "abbreviation": item["abbreviation"],
                "description": item["description"],
                "language": item["language"]["name"],
            }
            for item in data
        ]
        return versions
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
