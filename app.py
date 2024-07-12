from operator import or_
import os
import requests

from flask import Flask, jsonify, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from api import get_bible_versions

# from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
from models import User, FavoriteVerse, Devotional, SharedVerse, Category 

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

@app.route('/')
def index():
    versions = get_bible_versions(API_KEY)
    if versions:
        for version in versions:
            print(version)
    return "Check your console for Bible versions!"

if __name__ == '__main__':
    app.run(debug=True)