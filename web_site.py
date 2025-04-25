from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.users import User

db_session.global_init("db/blogs.db")

db_sess = db_session.create_session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def add_user(name, position, email, password):
    user = User()
    user.name = name
    user.about = position
    user.email = email
    user.set_password(password)
    db_sess.add(user)
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
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess1 = db_session.create_session()
        user = db_sess1.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/logout")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)