from app import app
from models import db, User

db.drop_all()
db.create_all()

u1 = User(
    username = "Bobo",
    password = "Jokerbob",
    email = 'bobsmith@gmail.com',
    first_name = 'Bob',
    last_name = 'Smith'
)

u2 = User(
    username = "Jillygal",
    password = "girlperson",
    email = "jillgall312@gmail.com",
    first_name = "Jill",
    last_name = "Smith"
)

db.session.add_all([u1, u2])
db.session.commit()