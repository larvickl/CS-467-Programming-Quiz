from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, TextAreaField, RadioField, BooleanField, SubmitField
from wtforms import widgets

class StartQuizForm(FlaskForm):
    quiz_pin = StringField(
        'PIN',
        validators=[
            DataRequired(message="PIN is required."),
            Length(min=1, max=10, message="Quiz PIN must be between %(min)d  and %(max)d  characters.")],
        render_kw={"placeholder": "Enter PIN"})
    submit = SubmitField('Start Quiz')

class QuizQuestionForm(FlaskForm):
    multi_choice_answer = RadioField(choices=[("0", "Option 1"), ("1", "Option 2"), ("2", "Option 3"), ("3", "Option 4")])
    multi_select_answer_one = BooleanField("Option 1")
    multi_select_answer_two = BooleanField("Option 2")
    multi_select_answer_three = BooleanField("Option 3")
    multi_select_answer_four = BooleanField("Option 4")
    tf_answer = RadioField(choices=[("0", "Option 1"), ("1", "Option 2")])
    free_response_answer = TextAreaField(
        "Free Response",
        render_kw={"placeholder": "Enter your answer."}
    )
    previous = SubmitField('Previous')
    next = SubmitField('Next')
    submit = SubmitField('Submit')