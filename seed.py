from app import app
from models import db, User, FavoriteVerse, Devotional, Category, Study
from datetime import datetime

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Creating users
        user1 = User.signup(username="john_doe", email="john@example.com", password="password123", image_url="/static/images/john.png")
        user2 = User.signup(username="jane_smith", email="jane@example.com", password="password456", image_url="/static/images/jane.png")
        
        db.session.commit()
        
        # Creating categories
        category1 = Category(name="Inspiration", user_id=user1.id)
        category2 = Category(name="Comfort", user_id=user2.id)
        
        db.session.add(category1)
        db.session.add(category2)
        db.session.commit()
        
        # Creating favorite verses
        favorite_verse1 = FavoriteVerse(user_id=user1.id, bible_id="KJV", verse_id="John 3:16", category=category1.id, note="For God so loved the world...")
        favorite_verse2 = FavoriteVerse(user_id=user2.id, bible_id="NIV", verse_id="Philippians 4:13", category=category2.id, note="I can do all this through him who gives me strength.")
        
        db.session.add(favorite_verse1)
        db.session.add(favorite_verse2)
        db.session.commit()
        
        # Creating devotionals
        devotional1 = Devotional(user_id=user1.id, title="Morning Inspiration", content="Start your day with faith and prayer.", date=datetime(2024, 7, 15))
        devotional2 = Devotional(user_id=user2.id, title="Evening Reflection", content="Reflect on the blessings of the day.", date=datetime(2024, 7, 14))
        
        db.session.add(devotional1)
        db.session.add(devotional2)
        db.session.commit()
        
        # Creating studies
        study1 = Study(user_id=user1.id, title="Book of John Study", content="In-depth study on the Book of John.", link_to_document="http://example.com/john_study.pdf")
        study2 = Study(user_id=user2.id, title="Philippians Study", content="Comprehensive guide on Philippians.", link_to_document="http://example.com/philippians_study.pdf")
        
        db.session.add(study1)
        db.session.add(study2)
        db.session.commit()
        
        print("Seed data created successfully.")

# Run the seed function
seed_data()

