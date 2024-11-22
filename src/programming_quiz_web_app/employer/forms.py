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
                max=4194303,
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