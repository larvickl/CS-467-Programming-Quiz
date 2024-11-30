from flask import render_template, send_from_directory, flash, redirect, url_for, request, session, current_app
from flask_wtf import FlaskForm
from programming_quiz_web_app.main import bp
from programming_quiz_web_app.main.forms import StartQuizForm, QuizQuestionForm
from programming_quiz_web_app.models import *

@bp.route('/index')
@bp.route('/')
def index():
    """This is the endpoint for the index."""
    return render_template('main/index.html', title="Home")

@bp.route('/robots.txt')
def robots():
    """Return a robots.txt file from the application root directory."""
    return send_from_directory("static", "robots.txt")

@bp.route('/vite')
def vite_example():
    """This is the endpoint for the vite example."""
    return render_template('main/vite_example.html', title="Vite Example")


@bp.route('/quiz/available')
def available_quizzes():
    """This is the endpoint for the available quizzes."""
    quizzes = Quizzes.query.all()
    return render_template('applicant/landing.html', title="Quizzes")

@bp.route('/quiz/begin/<url_id>', methods=['GET', 'POST'])
def start_quiz(url_id):
    """Endpoint to start a quiz"""
    # Instantiate form.
    form = StartQuizForm()
    # Locate the assignment.
    assignment = Assignments.query.filter_by(url = url_id).first()
    # PIN entered.
    if assignment is not None and form.validate_on_submit():
        if form.quiz_pin.data == assignment.url_pin:
            if assignment.start_time is None:
                assignment.start_time = dt.datetime.now(dt.timezone.utc)
                db.session.commit()
            flash("Good Luck!  Your quiz has now started!", "success")
            return redirect(url_for("main.do_quiz", url_id=url_id, pin=assignment.url_pin))
        else:
            flash("The entered PIN was invalid.  Please try again!", "danger")
    return render_template("applicant/start_quiz.html", assignment=assignment, form=form)

@bp.route('/quiz/take/<url_id>', methods=['GET', 'POST'])
def do_quiz(url_id):
    """Endpoint to manage taking a quiz."""
    quiz_pin: str = request.args.get('pin', None, type=str)
    current_question_ix = request.args.get('ix', 0, type=int)
    # Lookup the assignment.
    assignment = Assignments.query.filter_by(url = url_id).first()
    if assignment is None:
        flash("Invalid quiz!", "danger")
        return redirect(url_for('main.index'))
    # Confirm that the quiz has not been submitted.
    if assignment.submit_time is not None:
        flash("This quiz has already been submitted!", "danger")
        return redirect(url_for('main.index'))
    # Confirm that the pin is correct.
    if quiz_pin != assignment.url_pin:
        flash("Invalid PIN!", "danger")
        return redirect(url_for('main.index'))
    # Instantiate the form.
    form = QuizQuestionForm()
    # Get all questions.
    questions = assignment.quiz.get_ordered_questions()
    if len(questions) == 0:
        flash("Your quiz had no questions.  I guess you're done?", "danger")
        return redirect(url_for('main.index'))
    # Check that the given question index is valid.
    if current_question_ix > len(questions):
        flash("Invalid question number", "danger")
        current_question_ix = 0
    # if the form was submitted, save answer and redirect.
    if request.method == "POST":
        # Save question
        save_answer(questions[current_question_ix], assignment, current_question_ix, form)
        # Submit quiz if "submit" is clicked or time expired.
        if form.submit.data is True or get_assignment_remaining_time(assignment) <=0:
            # Calculate the submission time.
            if assignment.time_limit_seconds < 0:
                submit_time = min(dt.datetime.now(dt.timezone.utc), assignment.expiry)
            else:
                submit_time = min(dt.datetime.now(dt.timezone.utc), assignment.expiry, assignment.start_time + dt.timedelta(seconds=assignment.time_limit_seconds))
           # Save changes to database.
            try:
                assignment.submit_time = submit_time
                db.session.commit()
                flash("Your quiz has been submitted.", "success")
            except Exception as the_exception:
                current_app.logger.exception(the_exception)
                db.session.rollback()
                flash("There was an error submitting your quiz.", "danger")
            return redirect(url_for("main.index"))
        # Next question
        if form.next.data is True:
            return redirect(url_for("main.do_quiz", url_id=url_id, pin=assignment.url_pin, ix=current_question_ix+1))
    return render_template(
        'applicant/quiz_interface.html',
        quiz=assignment.quiz,
        current_question_ix=current_question_ix,
        current_question=questions[current_question_ix],
        current_question_number=current_question_ix + 1,
        total_questions=len(questions),
        has_previous=current_question_ix > 0,
        has_next=current_question_ix < len(questions) - 1,
        remaining_time=get_assignment_remaining_time(assignment),
        selected_answer=None,
        instructions=assignment.quiz.description,
        form=form,
        quiz_pin=quiz_pin,
        url_id=url_id,
        url_pin=assignment.url_pin
)

def save_answer(question: ChoiceQuestions | FreeResponseQuestions, assignment: Assignments, current_question_ix: int, form: FlaskForm):
    """Save a question to the database.

    Parameters
    ----------
    question : ChoiceQuestions | FreeResponseQuestions
        The question that has been answered.
    assignment : Assignments
        The assignment that is having a question saved.
    current_question_ix : int
        The index of the current question.
    form : FlaskForm
        The question's form.
    """
    score = None
    # If choice question, grade.
    if question.__tablename__ == "ChoiceQuestions":
        # Score multiple choice question.
        if question.question_type == "multiple-selection":
            score = 0
            answer_options = ""
            answer_text = ""
            # First multi_select option selected.
            if form.multi_select_answer_one.data is True:
                score += (question.options[0].option_weight / 100) * question.possible_points
                answer_options += "0, "
                answer_text += f"{question.options[0].option_text}\n"
            if form.multi_select_answer_two.data is True:
                score += (question.options[1].option_weight / 100) * question.possible_points
                answer_options += "1, "
                answer_text += f"{question.options[1].option_text}\n"
            if form.multi_select_answer_three.data is True:
                score += (question.options[2].option_weight / 100) * question.possible_points
                answer_options += "2, "
                answer_text += f"{question.options[2].option_text}\n"
            if form.multi_select_answer_four.data is True:
                score += (question.options[3].option_weight / 100) * question.possible_points
                answer_options += "3, "
                answer_text += f"{question.options[3].option_text}\n"
            answer = f"{answer_options} # {answer_text}"
            score = max(0, score)
        else:  # Score true/ false or multiple choice questions.
            option = question.options[int(form.multi_choice_answer.data)]
            score = (option.option_weight / 100) * question.possible_points
            answer = f"{form.multi_choice_answer.data} # {option.option_text}"
    else:  # Free response.
        answer = form.free_response_answer.data
        score = None
    new_answer = Answers(
        question_type = 'free-response' if question.__tablename__ == "FreeResponseQuestions" else question.question_type,
        question_title = question.title,
        question = question.body,
        question_solution= question.solution if question.__tablename__ == "FreeResponseQuestions" else "choice",
        answer = answer,
        possible_points = question.possible_points,
        awarded_points = score,
        question_id = current_question_ix,
        assignment_id = assignment.id
    )
    try:
        db.session.add(new_answer)
        db.session.commit()
    except Exception as the_exception:
        current_app.logger.exception(the_exception)
        db.session.rollback()
    
def get_assignment_remaining_time(assignment: Assignments) -> float | int:
    """Get the amount of time remaining for a specific assignment.  Find the 
    minimum time before either the expiry or the time limit has elapsed.

    Parameters
    ----------
    assignment : Assignments
        The assignment to find the remaining time for.

    Returns
    -------
    float | int
        The remaining time, in seconds.
    """
    if assignment.time_limit_seconds < 0:
        return (expiry - dt.datetime.now(dt.timezone.utc)).total_seconds()
    now = dt.datetime.now(dt.timezone.utc)
    expiry = assignment.expiry
    start_time = assignment.start_time
    time_limit_seconds = assignment.time_limit_seconds
    due_time = min((start_time + dt.timedelta(seconds=time_limit_seconds)), expiry)
    remaining_time = (due_time - now).total_seconds()
    return remaining_time