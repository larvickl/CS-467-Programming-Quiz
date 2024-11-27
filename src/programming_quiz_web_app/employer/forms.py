from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, RadioField, DateField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError
from programming_quiz_web_app.models import Quizzes 


class QuizDetailsForm(FlaskForm):
    """Validate the Quiz Details form submission.
    
    Attributes
    ----------
    quiz_title : StringField
        The title of the quiz.
    job_title : SelectField
        The associated job title for which the quiz is being created.
    language : SelectField
        The programming language relevant to the quiz.
    submit : SubmitField
        Form submission button labeled 'Next'.
    """
    quiz_title = StringField(
        'Quiz Title',
        validators=[
            DataRequired(message="Quiz title is required."),
            Length(min=3, max=299, message="Quiz title must be between %(min)d  and %(max)d  characters.")],
        render_kw={"placeholder": "Enter quiz title"})
    quiz_description = TextAreaField(
        'Quiz Description', 
        validators=[
            Length(min=0, max=4194302, message="Quiz title must be between %(min)d  and %(max)d  characters.")])
    default_time_limit_seconds = SelectField(
        'Time limit', 
        choices=[
            ('', 'Select the time limit'),
            ('1800', '30 minutes'),
            ('3600', '1 hour'),
            ('5400', '1.5 hours'),
            ('7200', '2 hours'),
            ('-1', 'Unlimited')], 
        validators=[DataRequired()])
    submit = SubmitField('Next')

    def validate_quiz_title(self, quiz_title):
        """Ensure the quiz title is unique in the database.
        
        Parameters
        ----------
        quiz_title : StringField
            The quiz title field to validate.
        
        Raises
        ------
        ValidationError
            If the quiz title already exists in the database.
        """
        existing_quiz = Quizzes.query.filter_by(name=quiz_title.data).first()
        if existing_quiz:
            raise ValidationError('A quiz with this title already exists. Please choose a different title.')

class AddQuestionForm(FlaskForm):
    """Form for adding a new question to a quiz.
    
    Attributes
    ----------
    question_type: StringField
        The type of question being added.
    question_body : TextAreaField
        The content of the question.
    submit : SubmitField
        Form submission button labeled 'Add Question'.
    """
    question_type = SelectField(
        'Question Type',
        choices=[
            ('true-false', 'True/False'),
            ('free-form', 'Free-Form'),
            ('multiple-choice', 'Multiple Choice'),
            ('code-snippet', 'Code Snippet')
        ],
        validators=[DataRequired()],
    )
    question_body = TextAreaField(
        'Question Body',
        validators=[
            DataRequired(), 
            Length(
                min=10, 
                max=4194302,
                message="Question body must be between 10 and 3000 characters.")],
        render_kw={"placeholder": "Enter your question"}
    )
    submit = SubmitField('Add Question')


class QuizSettingsForm(FlaskForm):
    """
    Form for configuring quiz settings.
    
    Attributes
    ----------
    time_limit : SelectField
        The time limit for the quiz.
    start_date : DateField
        The start date when the quiz becomes available.
    end_date : DateField
        The end date when the quiz is no longer available.
    randomize : RadioField
        Option to randomize the order of questions.
    submit : SubmitField
        Form submission button labeled 'Publish'.
    """
    time_limit = SelectField('Time limit', choices=[
        ('', 'Select the time limit'),
        ('30', '30 minutes'),
        ('60', '1 hour'),
        ('90', '1.5 hours'),
        ('120', '2 hours'),
        ('unlimited', 'Unlimited')
        ], 
        validators=[DataRequired()])

    start_date = DateField('Start date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End date', format='%Y-%m-%d', validators=[DataRequired()])

    randomize = RadioField('Randomize questions?', choices=[
        ('yes', 'Yes'),
        ('no', 'No')
        ], 
        default='no', 
        validators=[DataRequired()])

    submit = SubmitField('Publish')