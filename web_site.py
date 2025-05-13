import random

import flask_login
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.users import User
from data.blogs import Blog
from data.likes import Like

from sqlalchemy.sql.expression import func

db_session.global_init("db/blogs.db")

db_sess = db_session.create_session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def add_user(name, position, email, password):
    user1 = User()
    user1.name = name
    user1.about = position
    user1.email = email
    user1.set_password(password)
    db_sess.add(user1)
    db_sess.commit()
    bl = Blog()
    us = db_sess.query(User).filter(User.email == email).first()
    bl.tutle = us.id
    bl.content = "42"
    bl.user_id = us.id
    bl.user = us
    us.blogs.append(bl)
    db_sess.commit()


add_user("Ridley", "captain, research engineer", "scott_chief@mars.org", "qwe123")
add_user("Silent Den", "safety auditor, integrated safety auditor of the ship",
         "silent_den@mars.org", "kjreol02")
add_user("Green Mel", "doctor, therapist", "green_mel@mars.org", "uo)2l>Tq[")
add_user("Morgan Dexter", "engineer, engineer worker", "morgan_dexter@mars.org", "dexmor103")


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class UserForm(FlaskForm):
    blog = StringField('Название блога', validators=[DataRequired()])
    submit = SubmitField('Новый блог')


class BlogForm(FlaskForm):
    text = TextAreaField("Текст блога")
    submit = SubmitField('Изменить')


class OtherBlogForm(FlaskForm):
    submit = SubmitField('Понравилось')


@login_manager.user_loader
def load_user(user_id):
    db_sess1 = db_session.create_session()
    return db_sess1.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess1 = db_session.create_session()
        if (db_sess1.query(User).filter(User.email == form.email.data).first() or
                db_sess1.query(User).filter(User.name == form.name.data).first()):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user_ = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user_.set_password(form.password.data)
        db_sess.add(user_)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess1 = db_session.create_session()
        user2 = db_sess1.query(User).filter(User.email == form.email.data).first()
        if user2 and user2.check_password(form.password.data):
            login_user(user2, remember=form.remember_me.data)
            return redirect("/" + flask_login.current_user.name)
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/')
@app.route('/index')
def index():
    if flask_login.current_user:
        db_sess1 = db_session.create_session()
        blogs = []
        likes = flask_login.current_user.liked_blogs
        for i in range(10):
            if random.randint(0, 1):
                if likes:
                    blog_num = random.randint(0, len(likes))
                    if random.randint(0, 1):
                        blogs.append(random.choice(likes[blog_num].blog.user.blogs))
                    elif random.randint(0, 1):
                        a = random.choice(likes[blog_num].blog.user.liked_blogs)
                        blogs.append(a.blog)
                    else:
                        a = random.choice(likes[blog_num].blog.likes)
                        blogs.append(random.choice(a.user.liked_blogs))
                else:
                    blogs.append(random.choice(db_sess1.query.order_by(func.random()).first()))
            else:
                blogs.append(random.choice(db_sess1.query.order_by(func.random()).first()))
        return render_template('index.html', title='Блоги')
    else:
        return redirect("/login")


@app.route('/<path:n>', methods=['GET', 'POST'])
def user(n):
    n = n.split("/")
    db_sess1 = db_session.create_session()
    user3 = db_sess1.query(User).filter(User.name == n[0]).first()
    if user3:
        if len(n) == 1:
            form = UserForm()
            if form.validate_on_submit():
                if not db_sess1.query(Blog).filter(Blog.tutle == form.blog.data).first():
                    blog = Blog()
                    blog.title = form.blog.data
                    flask_login.current_user.blogs.append(blog)
                    db_sess1.merge(flask_login.current_user)
                    db_sess1.commit()
                    return redirect('/' + user3.name + '/' + form.blog.data)
                else:
                    return render_template('user.html', title=n[0], user=user3,
                                           your_page=flask_login.current_user == user3,
                                           message="Такой блог уже существует", form=form,
                                           cur_user=flask_login.current_user)
            return render_template('user.html', title=n[0], user=user3,
                                   form=form, cur_user=flask_login.current_user)
        else:
            blog = db_sess1.query(Blog).filter(Blog.tutle == n[1]).first()
            if blog and blog.user == user3:
                if flask_login.current_user == user3:
                    form = BlogForm()
                    if form.validate_on_submit():
                        blog.content = form.text.data
                        db_sess1.commit()
                        return redirect('/' + flask_login.current_user.name)
                    return render_template('blog.html', title=n[0], blog=blog,
                                           form=form, cur_user=flask_login.current_user)
                else:
                    form = OtherBlogForm()
                    like = db_sess1.query(Like).filter(Like.user == flask_login.current_user and Like.blog ==
                                                       blog).first()
                    if form.validate_on_submit():
                        if like:
                            db_sess1.delete(like)
                            db_sess1.commit()
                        else:
                            like = Like()
                            like.user_id = flask_login.current_user.id
                            like.user = flask_login.current_user
                            like.blog = blog
                            like.blog_id = blog.id
                            flask_login.current_user.liked_blogs.append(like)
                            blog.likes.append(like)
                            db_sess1.merge(flask_login.current_user)
                            db_sess1.merge(blog)
                            db_sess1.commit()
                    if like:
                        form.submit.label = "Не нравится"
                    else:
                        form.submit.label = "Нравится"
                    return render_template('blog.html', title=n[0], blog=blog,
                                           form=form, cur_user=flask_login.current_user)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)