from operator import or_
import os
import requests

from flask import Flask, jsonify, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

# from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
# from models import Like, db, connect_db, User, Message, Follow

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
API_KEY = os.getenv('API_KEY')

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
# app.app_context().push()

# # Get DB_URI from environ variable (useful for production/testing) or,
# # if not set there, use development local db.
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgresql:///bible-app'))

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
# toolbar = DebugToolbarExtension(app)

# connect_db(app)

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

@app.route('/')
def index():
    api_key = API_KEY
    versions = get_bible_versions(api_key)
    if versions:
        for version in versions:
            print(version)
    return "Check your console for Bible versions!"

if __name__ == '__main__':
    app.run(debug=True)