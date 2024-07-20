import requests
API_BASE_URL = "https://api.scripture.api.bible/v1"

POPULAR_TRANSLATIONS = [
    "de4e12af7f28f599-02",
    "06125adad2d5898a-01",
    "de4e12af7f28f599-01",
    "de4e12af7f28f599-02",
    "de4e12af7f28f599-03",
    "de4e12af7f28f599-04",
    "de4e12af7f28f599-05",
    "de4e12af7f28f599-06",
    "de4e12af7f28f599-07",
    "de4e12af7f28f599-08"
]

def get_translations(api_key):
    headers = {"api-key": api_key}
    try:
        response = requests.get(f"{API_BASE_URL}/bibles", headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (status code >= 400)
        data = response.json()["data"]
        versions = [
            {
                "name": item["name"],
                "abbreviation": item["abbreviation"],
            }
            for item in data if item['id'] in POPULAR_TRANSLATIONS
        ]
        return versions
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

# def get_translations(api_key):
#     headers = {"api-key": api_key}
#     try:
#         response = requests.get(f"{API_BASE_URL}/bibles", headers=headers)
#         response.raise_for_status()  # Raise an exception for HTTP errors (status code >= 400)
#         data = response.json()["data"]
#         versions = [
#             {
#                 "name": item["name"],
#                 "abbreviation": item["abbreviation"],
#             }
#             for item in data if item['id'] in POPULAR_TRANSLATIONS
#         ]
#         return versions
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
#         return []

def get_books(bible_id, api_key):
    headers = {"api-key": api_key}
    try:
        response = requests.get(f"{API_BASE_URL}/bibles/{bible_id}/books", headers=headers)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def get_chapters(bible_id, book_id, api_key):
    headers = {"api-key": api_key}
    try:
        response = requests.get(f"{API_BASE_URL}/bibles/{bible_id}/books/{book_id}/chapters", headers=headers)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def get_verses(bible_id, chapter_id, api_key):
    headers = {"api-key": api_key}
    try:
        response = requests.get(f"{API_BASE_URL}/bibles/{bible_id}/chapters/{chapter_id}/verses", headers=headers)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


