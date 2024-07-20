from os import environ

from flask import Flask, jsonify, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests

from sqlalchemy.exc import IntegrityError

from api import API_BASE_URL, get_translations, get_books, get_chapters, get_verses

from forms import SearchForm

# from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
from models import db, connect_db, User, Favorite, Message, Category 

# Access the environment variables
API_KEY = environ.get('API_KEY')

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.app_context().push()

# # Get DB_URI from environ variable (useful for production/testing) or,
# # if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    environ.get('DATABASE_URL', 'postgresql:///bible-app'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def index():
    versions = get_translations(API_KEY)
    return render_template('home.html', versions=versions)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    translations = get_translations(API_KEY)
    form.translation.choices = [(t['id'], f"{t['abbreviation']} - {t['name']}") for t in translations]

    if form.validate_on_submit():
        bible_id = form.translation.data
        book_id = form.book.data
        chapter_id = form.chapter.data
        start_verse = form.start_verse.data
        end_verse = form.end_verse.data
        results = search_verses(bible_id, chapter_id, start_verse, end_verse)
        return render_template('search.html', form=form, results=results)

    return render_template('search.html', form=form)

def search_verses(bible_id, chapter_id, start_verse, end_verse):
    response = requests.get(f"{API_BASE_URL}/v1/bibles/{bible_id}/chapters/{chapter_id}/verses")
    if response.status_code == 200:
        all_verses = response.json()['data']
        return [verse for verse in all_verses if int(start_verse) <= int(verse['id'].split('.')[-1]) <= int(end_verse)]
    return []

@app.route('/api/books/<bible_id>', methods=['GET'])
def api_books(bible_id):
    books = get_books(bible_id)
    return jsonify(books)

@app.route('/api/chapters/<bible_id>/<book_id>', methods=['GET'])
def api_chapters(bible_id, book_id):
    chapters = get_chapters(bible_id, book_id)
    return jsonify(chapters)

@app.route('/api/verses/<bible_id>/<chapter_id>', methods=['GET'])
def api_verses(bible_id, chapter_id):
    verses = get_verses(bible_id, chapter_id)
    return jsonify(verses)

if __name__ == '__main__':
    app.run(debug=True)