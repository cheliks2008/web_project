from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from data import db_session
from data.users import User

db_session.global_init("db/blogs.db")

db_sess = db_session.create_session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web_secret_key'



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)