from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import PrimaryKeyConstraint


bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """HolyVerse user model"""
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    image_url = db.Column(db.String(500),default="/static/images/default-pic.png")
    password = db.Column(db.String(128), nullable=False)
    
    def __repr__(self):
        user = self
        return f"<User id={user.id} username={user.username} email={user.email} image_url={user.image_url}>"
    
    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
class Category(db.Model):
    """Category model"""
    
    __tablename__ = "categories"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        category = self
        return f"<Category id={category.id} name={category.name}>"

class Favorite(db.Model):
    """Favorite verse model"""
    
    __tablename__ = "favorites"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bible_id = db.Column(db.String(50), nullable=False)
    book_id = db.Column(db.String(50), nullable=False)
    chapter_id = db.Column(db.String(50), nullable=False)
    verse_start = db.Column(db.Integer, nullable=False)
    verse_end = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())
   
    # Creates relationship between user and favorite verses
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    
    users = db.relationship('User', backref='favorites', cascade="all, delete")
    
    # Creates relationship between favorite verses and categories
    
    categories = db.relationship('Category', secondary='favorite_categories', backref='verses', cascade="all, delete")
    
    def __repr__(self):
        favorite = self
        return f"<Favorite id={favorite.id} user_id={favorite.user_id} bible_id={favorite.bible_id} book_id={favorite.book_id} verse_start={favorite.verse_start} verse_end={favorite.verse_end} note={favorite.note} created_at={favorite.created_at}>" 

# A section to save messages, sermons, lessons, devotionals
# Message - saved documents, related verses, audio bible links
class Message(db.Model):
    """Message model"""
    
    __tablename__ = "messages"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    link_to_document = db.Column(db.String(200))  # Optional link to external document
    
    # Creates relationship between user and devotionals
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    
    users = db.relationship('User', backref='messages', cascade="all, delete")
    
    # Creates relationship between messages and categories
    categories = db.relationship('Category', secondary='message_categories', backref='messages', cascade="all, delete")
    
    # Creates relationship between messages and favorite verses
    verses = db.relationship('Favorite', secondary='message_favorites', backref='messages', cascade="all, delete")
    
    def __repr__(self):
        message = self
        return f"<Message id={message.id} title={message.title} created_at={message.created_at} updated_at={message.updated_at} link_to_document={message.link_to_document} user_id={message.user_id}>"

class FavoriteCategory(db.Model):
    """Association table for Favorite and Category"""
    
    __tablename__ = "favorite_categories"
    
    favorite_id = db.Column(db.Integer, db.ForeignKey('favorites.id', ondelete="cascade"), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="cascade"), primary_key=True)
    
    __table_args__ = (
        PrimaryKeyConstraint('favorite_id', 'category_id'),
    )
    
    def __repr__(self):
        favorite_category = self
        return f"<FavoriteCategory favorite_id={favorite_category.favorite_id} category_id={favorite_category.category_id}>"

class MessageCategory(db.Model):
    """Association table for Message and Category"""
    
    __tablename__ = "message_categories"
    
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete="cascade"), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="cascade"), primary_key=True)
    
    __table_args__ = (
        PrimaryKeyConstraint('message_id', 'category_id'),
    )
    
    def __repr__(self):
        message_category = self
        return f"<MessageCategory message_id={message_category.message_id} category_id={message_category.category_id}>"

class MessageFavorite(db.Model):
    """Association table for Message and Favorite"""
    
    __tablename__ = "message_favorites"
    
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete="cascade"), primary_key=True)
    favorite_id = db.Column(db.Integer, db.ForeignKey('favorites.id', ondelete="cascade"), primary_key=True)
    
    __table_args__ = (
        PrimaryKeyConstraint('message_id', 'favorite_id'),
    )
    
    def __repr__(self):
        message_favorite = self
        return f"<MessageFavorite message_id={message_favorite.message_id} favorite_id={message_favorite.favorite_id}>"
