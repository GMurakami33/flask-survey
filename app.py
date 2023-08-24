from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "surveys"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start():
    """Starting page that provides title, instructions and start button"""
    responses.clear()
    return render_template('home.html', survey=survey)

@app.route('/questions/<int:question_index>', methods=['GET', 'POST'])
def show_questions(question_index):
    """Start providing questions"""
    if question_index >= len(survey.questions):
        flash('You are trying to access an invalid question.')
        return redirect('/thank_you')
    
    question = survey.questions[question_index]
    return render_template('questions.html', question=question)

@app.route('/answer', methods=['POST'])
def save_answers():
    selection = request.form.get('answer')
    responses.append(selection)

    question_index = len(responses)
    if question_index < len(survey.questions):
        return redirect (f'/questions/{question_index}')
    else:
        return redirect('/thank_you')

@app.route('/thank_you')
def say_thanks():
    return render_template('thank_you.html')