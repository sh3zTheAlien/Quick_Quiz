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

def check_answers(user_answers,correct_answers):
    user_correct = 0
    user_average_score = 0
    answered_questions = 0
    user_false = 0
    for i in range(len(correct_answers)):
        if user_answers[i] == correct_answers[i]:
            user_correct += 1
    answered_questions = len(user_answers) # Doesnt matter if it is correct or user answers cuz we take the length.
    user_average_score = (user_correct/answered_questions) * 100
    user_false = answered_questions - user_correct
    print(f"ANSWERED QUESTIONS:{answered_questions}\nAVERAGE SCORE: {user_average_score}%\n CORRECT ANSWERS:{user_correct}")

def generate_questions():
    response = requests.get("https://opentdb.com/api.php?amount=5&category=9&difficulty=medium&type=boolean")
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
            user_answers = [request.form.get(f'answer{i}') for i in range(len(quiz["questions"]))]
            correct_answers = [x["correct_answer"] for x in quiz["questions"]]
            print(f"User Answers: {user_answers}")
            print(f"Correct Answers: {correct_answers}")
            print(check_answers(user_answers,correct_answers))
            return redirect(url_for('home'))
        return render_template("game.html",questions=quiz["questions"])
    return render_template("error.html",error=quiz["error"])

if __name__ == "__main__":
    app.run(debug=True,port=5009)
