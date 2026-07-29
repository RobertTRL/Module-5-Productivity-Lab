from random import choice
 
from faker import Faker
 
from config import app
from models import db, User, Note
 
fake = Faker()
 
USER_COUNT = 15
NOTE_COUNT = 40
DEFAULT_PASSWORD = "password123"
 
 
def seed_users(count=USER_COUNT):
    usernames = set()
    while len(usernames) < count:
        usernames.add(fake.unique.user_name())
 
    users = []
    for username in usernames:
        user = User(username=username)
        user.password_hash = DEFAULT_PASSWORD
        users.append(user)
 
    db.session.add_all(users)
    db.session.commit()
    return users
 
 
def seed_notes(users, count=NOTE_COUNT):
    print(f"Seeding {count} notes...")
 
    notes = []
    for _ in range(count):
        note = Note(
            title=fake.sentence(nb_words=6).rstrip("."),
            content=fake.paragraph(nb_sentences=4),
            user_id=choice(users).id,
            created_at=fake.date_between(start_date="-1y", end_date="today"),
        )
        notes.append(note)
 
    db.session.add_all(notes)
    db.session.commit()
    return notes
 
 
if __name__ == "__main__":
    with app.app_context():
        Note.query.delete()
        User.query.delete()
        db.session.commit()
 
        users = seed_users()
        notes = seed_notes(users)