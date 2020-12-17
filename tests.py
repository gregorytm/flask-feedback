from unittest import TestCase

from app import app
from models import db, User, Feedback


# pick test database andclean sql  need fix seed
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_test'
app.config['SQLALCHEMY_ECHO'] = False

#show erros, not html
app.config['TESTING'] = True

#work around for FLASK Debugtoolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

#dont require csrf for testing
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for creating users"""

    def setUp(self):
        #demo data
        user=User(username='Test_Username',
            password='testpassword',
            email='testuser@gmail.com', 
            first_name='test',
            last_name='user')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        def tearDown(self):
            # clean up missed transactions
            db.session.rollback()