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
import html
import requests
#https://opentdb.com/api.php?amount=10&category=10&difficulty=medium&type=multiple

def generate_questions():
    response = requests.get("https://opentdb.com/api.php?amount=10&category=9&difficulty=medium&type=boolean")
    if response.status_code == 200:
        questions = response.json()["results"]
        #correct_answer = bool(response.json()["results"][0]["correct_answer"])
        return {"status":"success","questions":questions}
    return {"status":"fail","error":f"STATUS:{response.status_code} JSON:{response.json()}"}

def unescape_html(text:str):
    return html.unescape(text)

#FLASK QUESTIONS
app = Flask(__name__)
app.jinja_env.filters['unescape'] = unescape_html

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz_game",methods=['GET','POST'])
def game():
    quiz = generate_questions()
    if quiz["status"] == "success":
        if request.method == 'POST':
            print(request.form.get('answer'))
        return render_template("game.html",questions=quiz["questions"])
    return render_template("error.html",error=quiz["error"])

if __name__ == "__main__":
    app.run(debug=True,port=5001)
