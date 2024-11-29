from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, DecimalField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, NumberRange, Email
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


class AddQuestion(FlaskForm):
    """This class represent a form to add a generic question to the database."""
    question_title = StringField(
        'Question Title',
        validators=[
            DataRequired(message="Question title is required."),
            Length(min=3, max=299, message="Question title must be between %(min)d  and %(max)d  characters.")],
        render_kw={"placeholder": "Enter question title"})
    question_body = TextAreaField(
        'Question Body', 
        validators=[
            DataRequired(message="Question body is required."),
            Length(min=0, max=4194302, message="Question body must be between %(min)d  and %(max)d  characters.")],
            render_kw={"placeholder": "Enter the Question Body"})
    possible_points = DecimalField(
        "Possible Points",
        validators = [
            NumberRange(min=0, message="Possible Points must be greater than %(min)s.")])
    submit = SubmitField('Add Question')


class AddFreeResponseQuestion(AddQuestion):
    """This class represents a form to add a free response question.  This class extends AddQuestion"""
    question_solution = TextAreaField(
        'Question Solution', 
        validators=[
            DataRequired(message="Question solution is required."),
            Length(min=0, max=4194302, message="Question solution must be between %(min)d  and %(max)d  characters.")],
            render_kw={"placeholder": "Enter the question solution to be referenced by graders."})


class AddTrueFalseQuestion(AddQuestion):
    """This class represents a form to add a True/ False question.  This class extends AddQuestion"""
    true_option_weight = IntegerField(
        "True Option Weight",
        validators = [
            NumberRange(min=0, max=100, message="True Option Weight must be between %(min)s and %(max)d.")])
    false_option_weight = IntegerField(
        "False Option Weight",
        validators = [
            NumberRange(min=0, max=100, message="False Option Weight must be between %(min)s and %(max)d.")])
    

class AddChoiceQuestion(AddQuestion):
    """This class represents a form to add a multiple choice/ multiple selection question.  This class extends AddQuestion"""
    option_one_text = TextAreaField(
        'Option One Text', 
        validators=[
            DataRequired(message="Option One Text is required."),
            Length(min=0, max=4194302, message="Option One Text must be between %(min)d  and %(max)d  characters.")],
            render_kw={"placeholder": "Enter the option text"})
    option_one_weight = IntegerField(
        "Option One Weight",
        validators = [
            DataRequired(message="Option One Weight is required."),
            NumberRange(min=0, max=100, message="Option One Weight must be between %(min)s and %(max)d.")])
    option_two_text = TextAreaField(
        'Option Two Text', 
        validators=[
            DataRequired(message="Option Two Text is required."),
            Length(min=0, max=4194302, message="Option Two Text must be between %(min)d  and %(max)d  characters.")],
            render_kw={"placeholder": "Enter the option text"})
    option_two_weight = IntegerField(
        "Option Two Weight",
        validators = [
            DataRequired(message="Option Two Weight is required."),
            NumberRange(min=0, max=100, message="Option Two Weight must be between %(min)s and %(max)d.")])
    option_three_text = TextAreaField(
        'Option Three Text', 
        validators=[
            DataRequired(message="Option Three Text is required."),
            Length(min=0, max=4194302, message="Option Three Text must be between %(min)d  and %(max)d  characters.")],
            render_kw={"placeholder": "Enter the option text"})
    option_three_weight = IntegerField(
        "Option Three Weight",
        validators = [
            DataRequired(message="Option Three Weight is required."),
            NumberRange(min=0, max=100, message="Option Three Weight must be between %(min)s and %(max)d.")])
    option_four_text = TextAreaField(
        'Option Four Text', 
        validators=[
            DataRequired(message="Option Four Text is required."),
            Length(min=0, max=4194302, message="Option Four Text must be between %(min)d  and %(max)d  characters.")],
            render_kw={"placeholder": "Enter the option text"})
    option_four_weight = IntegerField(
        "Option Four Weight",
        validators = [
            DataRequired(message="Option Four Weight is required."),
            NumberRange(min=0, max=100, message="Option Four Weight must be between %(min)s and %(max)d.")])
    
class AddApplicant(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=299, message='Email must be less than %(max)d characters')],
        render_kw={"placeholder": "Applicant's Email Address"})
    surname = StringField(
        'Surname',
        validators=[
            DataRequired(message="Surname is required."),
            Length(min=3, max=99, message="Surname must be between %(min)d  and %(max)d  characters.")],
        render_kw={"placeholder": "Surname"})
    given_name = StringField(
        'Given Name',
        validators=[
            DataRequired(message="Given name is required."),
            Length(min=3, max=99, message="Given name must be between %(min)d  and %(max)d  characters.")],
        render_kw={"placeholder": "Given Name"})
    timezone = SelectField('Timezone', choices=[('', 'Select a timezone')], validators=[DataRequired()])
    submit = SubmitField('Add Applicant')

class AssignQuiz(FlaskForm):
    applicant = SelectField('Applicant', choices=[('', 'Select an applicant')], validators=[DataRequired()])
    quiz = SelectField('Quiz', choices=[('', 'Select a quiz')], validators=[DataRequired()])
    expiry = DateTimeLocalField("Expiry", validators=[DataRequired()])
    submit = SubmitField('Assign Quiz!')