from flask import render_template, send_from_directory, flash, redirect, url_for, request
from programming_quiz_web_app.main import bp
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
    
    print(quiz_start)

    if quiz_start == "yes":
        flash("Quiz has started. Good luck!", "success")
        return redirect(url_for('applicant/take_quiz.html', id=quiz.id))
    
    return render_template('applicant/confirm_start.html', quiz=quiz)

@bp.route('/quiz/submit', methods=['GET', 'POST'])
def confirm_submit_quiz():
    """Endpoint for Applicant to confirm submission of quiz."""
    quiz_id: int = request.args.get('id', type=int)
    quiz = Quizzes.query.get(quiz_id)
    if not quiz:
        flash("Quiz not found.", "danger")
        return redirect(url_for('main.index'))
    
    applicant = Applicants.query.get('id', type=int)
    
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
            return redirect(url_for('applicant/take_quiz.html', quiz_id=quiz_id))
    
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

