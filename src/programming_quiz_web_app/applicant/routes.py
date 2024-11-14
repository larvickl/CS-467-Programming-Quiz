from flask import render_template, flash, redirect, url_for, request
from programming_quiz_web_app.applicant import bp
from programming_quiz_web_app.main import bp
from programming_quiz_web_app.models import *
from programming_quiz_web_app.models import Quizzes
from programming_quiz_web_app.models import Applicants


@bp.route('/quiz/start', methods=['GET', 'POST'])
def confirm_start_quiz():
    """Endpoint for the Applicant confirmation prior to starting quiz."""
    quiz_id: int = request.args.get('id', type=int)
    if quiz_id is None:
        flash("Quiz ID is missing.", "error")
        return redirect(url_for('main.index'))

    quiz = Quizzes.query.get(quiz_id)
    if quiz is None:
        flash("Quiz not found.", "error")
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        confirm: str = request.form.get('confirm', type=str)
        if confirm == 'yes':
            flash("Quiz has started. Good luck!")
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
        flash("Quiz not found.", "error")
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
            
            flash("Quiz submitted successfully.")
            return redirect(url_for('applicant/quiz_summary.html', quiz_id=quiz_id))
        else:
            return redirect(url_for('applicant/take_quiz.html', quiz_id=quiz_id))
    
    return render_template('applicant/confirm_submit.html', quiz=quiz)