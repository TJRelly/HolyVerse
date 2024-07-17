from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

# Your models definitions go here...

# Seed data creation
def create_seed_data():
    # Create users
    user1 = User.signup('user1', 'user1@example.com', 'password1', '/static/images/user1.png')
    user2 = User.signup('user2', 'user2@example.com', 'password2', '/static/images/user2.png')
    
    # Commit users to the database
    db.session.add_all([user1, user2])
    db.session.commit()
    
    # Create categories
    category1 = Category(name='Love')
    category2 = Category(name='Faith')
    category3 = Category(name='Hope')
    
    # Commit categories to the database
    db.session.add_all([category1, category2, category3])
    db.session.commit()
    
    # Create favorite verses with categories
    verse1 = FavoriteVerse(bible_id='KJV', book_id='John', chapter_id='3', verse_start=16, verse_end=17, note='Famous verse', user_id=user1.id)
    verse2 = FavoriteVerse(bible_id='ESV', book_id='Romans', chapter_id='8', verse_start=28, verse_end=30, note='Encouraging verse', user_id=user1.id)
    verse3 = FavoriteVerse(bible_id='NIV', book_id='Galatians', chapter_id='2', verse_start=20, verse_end=21, note='Grace verse', user_id=user2.id)
    
    # Assign categories to verses
    verse1.categories.append(category1)
    verse1.categories.append(category2)
    verse2.categories.append(category2)
    verse2.categories.append(category3)
    verse3.categories.append(category1)
    
    # Commit verses to the database
    db.session.add_all([verse1, verse2, verse3])
    db.session.commit()
    
    # Create messages with verses and categories
    message1 = Message(title='Sermon on Love', content='Preaching about the importance of love.', user_id=user1.id, link_to_document='https://example.com/sermon1')
    message2 = Message(title='Devotional on Faith', content='Encouraging devotion on faith.', user_id=user2.id, link_to_document='https://example.com/devotional1')
    
    # Assign verses and categories to messages
    message1.verses.append(verse1)
    message1.verses.append(verse2)
    message1.categories.append(category1)
    message1.categories.append(category2)
    
    message2.verses.append(verse3)
    message2.categories.append(category1)
    
    # Commit messages to the database
    db.session.add_all([message1, message2])
    db.session.commit()

# Run the seed data creation
create_seed_data()


