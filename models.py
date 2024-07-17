from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


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
        return f"<User id={user.id} username={user.username} email={user.email}>"
    
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    
    # favorite_verses = db.relationship('FavoriteVerse', backref='categoriy', cascade="all, delete")
    
    def __repr__(self):
        category = self
        return f"<Category id={category.id} name={category.name}>"

class FavoriteVerse(db.Model):
    """Favorite verse model"""
    
    __tablename__ = "favorite_verses"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bible_id = db.Column(db.String(50), nullable=False)
    book_id = db.Column(db.String(50), nullable=False)
    chapter_id = db.Column(db.String(50), nullable=False)
    verse_start_id = db.Column(db.String(50), nullable=False)
    verse_end_id = db.Column(db.String(50), nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
   
    # Creates relationship between user and favorite verses
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    
    users = db.relationship('User', backref='favoriteVerse', cascade="all, delete")
    
    # Creates relationship between favorite verses and categories
    categories = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="cascade"))
    
    categories = db.relationship('Category', backref='verse', cascade="all, delete")
    
    def __repr__(self):
        favorite_verse = self
        return f"<FavoriteVerse id={favorite_verse.id} user_id={favorite_verse.user_id} bible_id={favorite_verse.bible_id} verse_id={favorite_verse.verse_id}>" 

class Devotional(db.Model):
    """Devotional model"""
    
    __tablename__ = "devotionals"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Creates relationship between user and devotionals
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    
    users = db.relationship('User', backref='devotional', cascade="all, delete")
    
    # Creates relationship between devotionals and categories
    categories = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="cascade"))
    
    categories = db.relationship('Category', backref='devotional', cascade="all, delete")
    
    def __repr__(self):
        devotional = self
        return f"<Devotional id={devotional.id} title={devotional.title} date={devotional.date}>"

class Study(db.Model):
    """Study model"""
    
    __tablename__ = "studies"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    link_to_document = db.Column(db.String(200))  # Optional link to external document
    category = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="cascade"))
    
    def __repr__(self):
        
        
        return f"<Study id={self.id} user_id={self.user_id} title={self.title}>"