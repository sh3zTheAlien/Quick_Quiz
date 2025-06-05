from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
import requests
#https://opentdb.com/api.php?amount=10&category=10&difficulty=medium&type=multiple


def generate_question():
    response = requests.get("https://opentdb.com/api.php?amount=1&category=9&difficulty=medium&type=boolean").json()
    question = response["results"][0]["question"]
    correct_answer = response["results"][0]["correct_answer"]
    return {"question":question,"answer":correct_answer}

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz_game")
def game():
    quiz = generate_question()
    return render_template("game.html",question=quiz["question"])


if __name__ == "__main__":
    app.run(debug=True,port=5001)
