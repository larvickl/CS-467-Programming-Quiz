from flask import render_template, send_from_directory, flash, redirect, url_for, request, session
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
    
@bp.route('/quiz/start', methods=['GET'])
def confirm_start_quiz():
    """Endpoint for the Applicant confirmation prior to starting quiz."""
    quiz_id: int = request.args.get('id', type=int)
    quiz_start: int = request.args.get('start', "no", type=str)
    if quiz_id is None:
        flash("Quiz ID is missing.", "danger")
        return redirect(url_for('main.index'))

    quiz = Quizzes.query.get(quiz_id)
    if quiz is None:
        flash("Quiz not found.", "danger")
        return redirect(url_for('main.index'))
    
    if quiz_start == "yes":
        flash("Quiz has started. Good luck!", "success")
        return redirect(url_for('main.take_quiz', quiz_id=quiz.id))
    
    return render_template('applicant/confirm_start.html', quiz=quiz)

@bp.route('/quiz/session/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    """Main quiz-taking interface endpoint."""
    quiz = Quizzes.query.get_or_404(quiz_id)
    action = request.args.get('action', '')
    current = request.args.get('current', type=int)
    answer = request.args.get('answer')
    question_id = request.args.get('question_id')

    # # Debug prints
    # print("Choice Questions:", quiz.choice_questions)
    # print("Free Response Questions:", quiz.free_response_questions)

    # Get all questions and put them in order
    questions = []
    questions.extend(quiz.choice_questions)
    questions.extend(quiz.free_response_questions)
    # print("Combined Questions:", questions)
    questions.sort(key=lambda q: q.order)
    # print("Sorted Questions:", questions)

    if not questions:
        flash("No questions found for this quiz.", "warning")
        return redirect(url_for('main.index'))

    if 'quiz_session' not in session:
        session['quiz_session'] = {
            'quiz_id': quiz_id,
            'current_question': 0,
            'start_time': dt.datetime.now(dt.timezone.utc).isoformat(),
            'answers': {}
        }

    question_number = session['quiz_session']['current_question']

    # # save answers
    if request.method == 'POST':
        answer = request.form.get('answer')
        current_question_id = request.form.get('question_id')
    
    if answer and current_question_id:
        session['quiz_session']['answers'][current_question_id] = answer
        session.modified = True

    if action and current:
        current_index = current - 1 
        if action == 'next' and current_index < len(questions) - 1:
            session['quiz_session']['current_question'] = current_index + 1
            session.modified = True
        elif action == 'previous' and current_index > 0:
            session['quiz_session']['current_question'] = current_index - 1
            session.modified = True
        
    question_number = session['quiz_session']['current_question']
    current_question = questions[question_number]
    question_type = 'choice' if isinstance(current_question, ChoiceQuestions) else 'free_response'
    
    # time limit
    start_time = dt.datetime.fromisoformat(session['quiz_session']['start_time'])
    elapsed_time = dt.datetime.now(dt.timezone.utc) - start_time
    remaining_time = quiz.default_time_limit_seconds - int(elapsed_time.total_seconds())
    
    if remaining_time <= 0:
        return redirect(url_for('main.confirm_submit_quiz', id=quiz_id))
    
    return render_template(
        'applicant/quiz_interface.html',
        quiz=quiz,
        current_question=current_question,
        question_type=question_type,
        current_question_number=question_number + 1,
        total_questions=len(questions),
        has_previous=question_number > 0,
        has_next=question_number < len(questions) - 1,
        remaining_time=int(remaining_time / 60),
        selected_answer=session['quiz_session']['answers'].get(str(current_question.id), {}).get('answer'),
        instructions=quiz.description
)



@bp.route('/quiz/submit', methods=['GET', 'POST'])
def confirm_submit_quiz():
    """Endpoint for Applicant to confirm submission of quiz."""
    quiz_id: int = request.args.get('id', type=int)
    quiz = Quizzes.query.get(quiz_id)
    if not quiz:
        flash("Quiz not found.", "danger")
        return redirect(url_for('main.index'))
    
    applicant_id = request.args.get('id', type=int)
    applicant = Applicants.query.get(applicant_id)
    
    if request.method == 'POST':
        confirm: str = request.form.get('confirm', type=str)
        if confirm == 'yes':
            quiz_instance = Quizzes.query.filter_by(id=quiz_id, created_by_id=applicant).first()
            if quiz_instance:
                quiz_instance.submitted = True  
                quiz_instance.end_time = dt.datetime(dt.timezone.utc)
                db.session.commit()
            
            flash("Quiz submitted successfully.", "success")
            return redirect(url_for('applicant/quiz_summary.html', quiz_id=quiz_id))
        else:
            return redirect(url_for('main.take_quiz', quiz_id=quiz_id))
    
    return render_template('applicant/confirm_submit.html', quiz=quiz)

@bp.route('/quiz/available')
def available_quizzes():
    """This is the endpoint for the available quizzes."""
    quizzes = Quizzes.query.all()
    return render_template('applicant/landing.html', title="Quizzes")

@bp.route('/quiz/test')
def test_quiz():
    """Test route to render quiz_interface.html with static data for front-end testing."""
    
    # Static/mock data for testing
    instructions = "Please read the following question carefully and select the best answer."
    remaining_time = 45  # in minutes
    current_question_number = 1
    total_questions = 3  # example number
    
    current_question = {
        'id': 1,
        'content': 'What language is the app "Software Programming Quiz" programmed in?',
        'answers': [
            {'id': 'A', 'text': 'Java'},
            {'id': 'B', 'text': 'Python'},
            {'id': 'C', 'text': 'C++'},
            {'id': 'D', 'text': 'C#'},
        ]
    }
    
    selected_answer = None  # No answer selected initially
    
    has_previous = False  # First question, no previous
    has_next = True       # There are more questions
    
    pagination_pages = [1, 2, 3]
    
    return render_template(
        'applicant/quiz_interface.html',
        title="Quiz in Progress",
        instructions=instructions,
        remaining_time=remaining_time,
        current_question_number=current_question_number,
        total_questions=total_questions,
        current_question=current_question,
        selected_answer=selected_answer,
        has_previous=has_previous,
        has_next=has_next,
        pagination_pages=pagination_pages
    )

@bp.route('/quiz/begin/<url_id>', methods=['GET', 'POST'])
def start_quiz(url_id):
    # Instantiate form.
    form = StartQuizForm()
    # Locate the assignment.
    assignment = Assignments.query.filter_by(url = url_id).first()
    # PIN entered.
    if assignment is not None and form.validate_on_submit():
        if form.quiz_pin.data == assignment.url_pin:
            flash("Good Luck!  Your quiz has now started!", "success")
            return redirect(url_for("main.do_quiz", url_id=url_id, pin=assignment.url_pin))
        else:
            flash("The entered PIN was invalid.  Please try again!", "danger")
    return render_template("applicant/start_quiz.html", assignment=assignment, form=form)

@bp.route('/quiz/take/<url_id>', methods=['GET', 'POST'])
def do_quiz(url_id):
    quiz_pin: str = request.args.get('pin', None, type=str)
    current_question_ix = request.args.get('ix', 0, type=int)
    # Lookup the assignment.
    assignment = Assignments.query.filter_by(url = url_id).first()
    if assignment is None:
        flash("Invalid quiz!", "danger")
        redirect(url_for('main.index'))
    # Confirm that the pin is correct.
    if quiz_pin != assignment.url_pin:
        flash("Invalid PIN!", "danger")
        redirect(url_for('main.index'))
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
    return render_template(
        'applicant/quiz_interface.html',
        quiz=assignment.quiz,
        current_question=questions[current_question_ix],
        current_question_number=current_question_ix + 1,
        total_questions=len(questions),
        has_previous=current_question_ix > 0,
        has_next=current_question_ix < len(questions) - 1,
        remaining_time=10,
        selected_answer=None,
        instructions=assignment.quiz.description,
        form=form,
        quiz_pin=quiz_pin,
        url_id=url_id,
)


