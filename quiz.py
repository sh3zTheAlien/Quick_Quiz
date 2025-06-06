import requests

class Questions:

    def __init__(self,amount,difficulty,question_type,category):
        """ type: 'bool' or 'multiple'
            difficulty: 'easy' or 'medium' or 'hard'
            amount: a number between 1 - 40
            (questions)category: a number (video-games:15,sports:21,computers:18,general:9)"""
        self.amount = amount
        self.difficulty = difficulty
        self.question_type = question_type
        self.category = category

    def get_questions(self):
        response = requests.get(f"https://opentdb.com/api.php?amount={self.amount}&category={self.category}&difficulty={self.difficulty}&type={self.question_type}")
        if response.status_code == 200:
            return {"status":"success","questions":response.json()["results"]}
        return {"status": "fail", "error": f"STATUS:{response.status_code} JSON:{response.json()}"}


class Score:

    def __init__(self):
        self.score = 0
        self.correct_answers = 0
        self.answered_questions = 0
        self.false_answers = 0
        self.average_score = 0

    def check_answers(self,user_answers,correct_answers):
        for i in range(len(correct_answers)):
            if user_answers[i] == correct_answers[i]:
                self.correct_answers += 1

        self.answered_questions = len(user_answers)
        self.average_score = (self.correct_answers/self.answered_questions) * 100
        self.false_answers = self.answered_questions - self.false_answers
        return (f"ANSWERED QUESTIONS:{self.answered_questions}\n"
                f"CORRECT ANSWERS:{self.correct_answers}\n"
                f"FALSE ANSWERS:{self.false_answers}\n"
                f"AVERAGE SCORE:{self.average_score}%")