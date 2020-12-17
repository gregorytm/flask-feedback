from flask import Flask, redirect, session, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback

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

    if 'id' in session:
        return redirect(f"/users/{session['id']}")

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()
        session['id'] = user.id

        return render_template('home.html')

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if "id" in session:
        return redirect(f"/users/{session['id']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['id'] = user.id
            return redirect(f"/users/{user.id}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("{users/login.html", form=form)

    return render_template("users/login.html", form=form)

@app.route("/logout")
def logout():
    session.pop('id')
    return redirect("/login")
    
@app.route('/users/<id>')
def show_user(id):

    # if "id" not in session or id != session['id']:
    #     raise Unauthorized()

    user = User.query.get(id)

    return render_template("users/details.html", user=user)

@app.route('/secret')
def show_secret():
    if 'id' not in session:
        flash("Not logged in")
        return redirect ('/login')
    else:
        return render_template('secret.html')

@app.route('/users/<id>/delete', methods=["POST"])
def delete_current_user(id):
    if "id" not in session or id != session["id"]:
        raise Unauthorized()

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    session.pop("id")

    return redirect("/login")

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "id" not in session or feedback.id != session['id']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit

        return redirect(f"/users/{feedback.id}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route("/users/<id>/feedback/new", methods=["GET", "POST"])
def new_feedback(id):

    if "id" not in session:
        raise Unauthorized()

    form = Feedback()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            user_id=id
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.user_id}")

    else:
        return render_template("feedback/new", form=form)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)
    if 'id' not in session or feedback.id != session['id']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.id}")