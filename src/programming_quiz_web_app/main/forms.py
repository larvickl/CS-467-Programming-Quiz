from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, TextAreaField, RadioField, SelectMultipleField, SubmitField
from wtforms import widgets

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ol', prefix_label=False)
    option_widget = widgets.CheckboxInput()

class StartQuizForm(FlaskForm):
    quiz_pin = StringField(
        'PIN',
        validators=[
            DataRequired(message="PIN is required."),
            Length(min=1, max=10, message="Quiz PIN must be between %(min)d  and %(max)d  characters.")],
        render_kw={"placeholder": "Enter PIN"})
    submit = SubmitField('Start Quiz')

class QuizQuestionForm(FlaskForm):
    multi_choice_answer = RadioField(choices=[("1", "Option 1"), ("2", "Option 2"), ("3", "Option 3"), ("4", "Option 4")])
    multi_select_answer = MultiCheckboxField(choices=[("1", "Option 1"), ("2", "Option 2"), ("3", "Option 3"), ("4", "Option 4")])
    tf_answer = RadioField(choices=[("1", "Option 1"), ("2", "Option 2"), ("3", "Option 3"), ("4", "Option 4")])
    free_response_answer = TextAreaField(
        "Free Response",
        render_kw={"placeholder": "Enter your answer."}
    )