from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
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
            Length(
                min=3, 
                max=255, 
                message="Quiz title must be between 3 and 255 characters."
            )
        ],
        render_kw={"placeholder": "Enter quiz title"}
    )
    
    job_title = SelectField(
        'Job Title',
        choices=[
            ('', 'Select the job title'),
            ('Developer', 'Developer'),
            ('Manager', 'Manager'),
            ('Analyst', 'Analyst')
        ],
        validators=[DataRequired()],
    )
    
    language = SelectField(
        'Programming Language',
        choices=[
            ('', 'Select the quiz language'),
            ('Python', 'Python'),
            ('Java', 'Java'),
            ('JavaScript', 'JavaScript')
        ],
        validators=[DataRequired()]
    )
    
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
