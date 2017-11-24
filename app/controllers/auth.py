from flask import render_template, redirect, url_for, flash, request
from app import app, bcrypt, db, login_manager
from app.forms.user import CreateForm
from app.models.user import User, Room
from flask_login import login_user, logout_user, login_required, current_user
import secrets
import random


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@app.route("/", methods=["GET", "POST"])
def create():
    origin="CRIAÇÃO"
    form = CreateForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        token = secrets.token_hex(nbytes=random.randint(50, 150))
        user = User(username, password, token)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("create.html", form=form, origin=origin)


@app.route("/login", methods=["GET", "POST"])
def login():
    origin="LOGIN"
    form = CreateForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        print(user)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('users'))
        else:
            flash("ERRO AO FAZER LOGIN")

    return render_template("create.html", form=form, origin=origin)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/users")
@login_required
def users():
    users = User.query.all()
    roons = Room.query.filter_by(user_id=current_user.id).all()
    return render_template('users.html', users=users, roons=roons)