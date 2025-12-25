from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Request
from forms import SignupForm, LoginForm, RequestForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@login_required
def dashboard():
    if current_user.role == "admin":
        requests = Request.query.all()
    else:
        requests = Request.query.filter_by(user_id=current_user.id)
    return render_template("dashboard.html", requests=requests)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please login.")
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid email or password")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit_request():
    form = RequestForm()
    if form.validate_on_submit():
        req = Request(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(req)
        db.session.commit()
        flash("Request submitted")
        return redirect(url_for("dashboard"))
    return render_template("submit_request.html", form=form)


@app.route("/approve/<int:req_id>")
@login_required
def approve(req_id):
    if current_user.role != "admin":
        flash("Not authorized")
        return redirect(url_for("dashboard"))
    req = Request.query.get(req_id)
    req.status = "Approved"
    db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/reject/<int:req_id>")
@login_required
def reject(req_id):
    if current_user.role != "admin":
        flash("Not authorized")
        return redirect(url_for("dashboard"))
    req = Request.query.get(req_id)
    req.status = "Rejected"
    db.session.commit()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
