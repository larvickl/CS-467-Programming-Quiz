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
    
@bp.route('/quiz/start', methods=['GET', 'POST'])
def confirm_start_quiz():
    """Endpoint for the Applicant confirmation prior to starting quiz."""
    quiz_id: int = request.args.get('id', type=int)
    if quiz_id is None:
        flash("Quiz ID is missing.", "danger")
        return redirect(url_for('main.index'))

    quiz = Quizzes.query.get(quiz_id)
    if quiz is None:
        flash("Quiz not found.", "danger")
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        confirm: str = request.form.get('confirm', type=str)
        if confirm == 'yes':
            flash("Quiz has started. Good luck!", "success")
            return redirect(url_for('applicant/take_quiz.html', id=quiz.id))
        else:
            return redirect(url_for('main.index'))
    
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
