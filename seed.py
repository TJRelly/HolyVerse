from models import db, User, Category, Favorite, Message, FavoriteCategory, MessageCategory, MessageFavorite

from app import app
app.app_context()

# Clear all existing data
db.drop_all()
db.create_all()

# Create users
user1 = User.signup('john', 'user1@example.com', 'password1', '/static/images/user1.png')
user2 = User.signup('mary', 'user2@example.com', 'password2', '/static/images/user2.png')

db.session.add(user1)
db.session.add(user2)
db.session.commit()

# Create categories
category1 = Category(name='Love')
category2 = Category(name='Faith')
category3 = Category(name='Hope')

db.session.add(category1)
db.session.add(category2)
db.session.add(category3)
db.session.commit()

# Create favorite verses
verse1 = Favorite(bible_id='KJV', book_id='John', chapter_id='3', verse_start=16, verse_end=17, note='For God so loved the world...', user_id=user1.id)
verse2 = Favorite(bible_id='ESV', book_id='Romans', chapter_id='5', verse_start=1, verse_end=2, note='Therefore, since we have been justified...', user_id=user1.id)
verse3 = Favorite(bible_id='NIV', book_id='1 Corinthians', chapter_id='13', verse_start=4, verse_end=7, note='Love is patient, love is kind...', user_id=user2.id)

db.session.add(verse1)
db.session.add(verse2)
db.session.add(verse3)
db.session.commit()

# Create messages
message1 = Message(title='God\'s Love', content='A message about God\'s unconditional love for humanity.', link_to_document='https://example.com/gods-love.pdf', user_id=user1.id)
message2 = Message(title='Faith and Works', content='Exploring the relationship between faith and works in Christian life.', user_id=user2.id)
message3 = Message(title='Living in Hope', content='A message about living with hope in difficult times.', user_id=user1.id)

db.session.add(message1)
db.session.add(message2)
db.session.add(message3)
db.session.commit()

# Associate favorite verses with categories
favorite_category1 = FavoriteCategory(favorite_id=verse1.id, category_id=category1.id)
favorite_category2 = FavoriteCategory(favorite_id=verse1.id, category_id=category2.id)
favorite_category3 = FavoriteCategory(favorite_id=verse2.id, category_id=category2.id)
favorite_category4 = FavoriteCategory(favorite_id=verse3.id, category_id=category1.id)
favorite_category5 = FavoriteCategory(favorite_id=verse3.id, category_id=category3.id)

db.session.add(favorite_category1)
db.session.add(favorite_category2)
db.session.add(favorite_category3)
db.session.add(favorite_category4)
db.session.add(favorite_category5)
db.session.commit()

# Associate messages with categories and favorite verses
message_category1 = MessageCategory(message_id=message1.id, category_id=category1.id)
message_category2 = MessageCategory(message_id=message2.id, category_id=category2.id)
message_category3 = MessageCategory(message_id=message3.id, category_id=category3.id)

message_favorite1 = MessageFavorite(message_id=message1.id, favorite_id=verse1.id)
message_favorite2 = MessageFavorite(message_id=message2.id, favorite_id=verse2.id)
message_favorite3 = MessageFavorite(message_id=message3.id, favorite_id=verse3.id)
message_favorite4 = MessageFavorite(message_id=message1.id, favorite_id=verse3.id)

db.session.add(message_category1)
db.session.add(message_category2)
db.session.add(message_category3)
db.session.add(message_favorite1)
db.session.add(message_favorite2)
db.session.add(message_favorite3)
db.session.add(message_favorite4)
db.session.commit()




