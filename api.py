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

import requests

API_BASE_URL = "https://api.scripture.api"

def get_translations():
    response = requests.get(f"{API_BASE_URL}/v1/bibles")
    if response.status_code == 200:
        return response.json()['data']
    return []

def get_books(bible_id):
    response = requests.get(f"{API_BASE_URL}/v1/bibles/{bible_id}/books")
    if response.status_code == 200:
        return response.json()['data']
    return []

def get_chapters(bible_id, book_id):
    response = requests.get(f"{API_BASE_URL}/v1/bibles/{bible_id}/books/{book_id}/chapters")
    if response.status_code == 200:
        return response.json()['data']
    return []

def get_verses(bible_id, chapter_id):
    response = requests.get(f"{API_BASE_URL}/v1/bibles/{bible_id}/chapters/{chapter_id}/verses")
    if response.status_code == 200:
        return response.json()['data']
    return []

