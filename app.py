from flask import Flask, redirect, session, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

# what is zerkzug.exceptions?
from werkzeug.exceptions import Unauthorized

from forms import AddUserForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Mario-and-Luigi-188'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

debug = DebugToolbarExtension(app)

@app.route('/')
def homepage():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def add_user():

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()
        session['username'] = user.username

        return render_template('home.html')

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("{users/loggin.html", form=form)

    return render_template("users/login.html", form=form)

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/login")
    
@app.route('/users/<username>')
def show_user(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)

    return render_template("users/details.html", user=user)