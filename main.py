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
from quiz import Questions,Score
import html
import requests
#https://opentdb.com/api.php?amount=5&category=9&difficulty=medium&type=boolean

query_manager = Questions(amount=5,difficulty='medium',question_type='boolean',category=9)
quiz_score = Score()

#FLASK QUESTIONS
app = Flask(__name__)
app.jinja_env.filters['unescape'] = lambda text: html.unescape(text)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz_game",methods=['GET','POST'])
def game():
    quiz = query_manager.get_questions()
    if quiz["status"] == "success":
        if request.method == 'POST':
            user_answers = [request.form.get(f'answer{i}') for i in range(len(quiz["questions"]))]
            correct_answers = [x["correct_answer"] for x in quiz["questions"]]
            print(quiz_score.check_answers(user_answers,correct_answers))
            return redirect(url_for('home'))
        return render_template("game.html",questions=quiz["questions"])
    return render_template("error.html",error=quiz["error"])

if __name__ == "__main__":
    app.run(debug=True,port=5009)
