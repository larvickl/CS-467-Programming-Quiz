from flask import render_template, flash, redirect, url_for, request
from programming_quiz_web_app.employer import bp
import datetime as dt
from programming_quiz_web_app.models import *
from programming_quiz_web_app.employer.forms import QuizDetailsForm, AddQuestionForm, QuizSettingsForm
from programming_quiz_web_app import db


@bp.route('/dashboard')
def dashboard():
    """This is the endpoint for the dashboard."""
     # Fetch latest 6 quizzes
    recent_quizzes = Quizzes.query.order_by(Quizzes.time_created.desc()).limit(6).all()

    # Recent activities list
    recent_activities = []
    for quiz in recent_quizzes:
        recent_activities.append({
            'description': f"Quiz '{quiz.name}' created...",
            'timestamp': quiz.time_created
        })

    # Fetch applicants
    recent_applicants = Applicants.query.order_by(Applicants.id.desc()).all()
    for applicant in recent_applicants:
        recent_activities.append({
            'description': f"Candidate {applicant.given_name} {applicant.surname} added...",
            'timestamp': applicant.id  # using ID as a proxy for time?
        })

    # Sort all recent activities by timestamp descending
    recent_activities_sorted = sorted(
        recent_activities,
        key=lambda x: x['timestamp'],
        reverse=True
    )

    # Fetch all quizzes
    quizzes = Quizzes.query.all()

    # Calculate takers
    for quiz in quizzes:
        quiz.takers = Assignments.query.filter_by(quiz_id=quiz.id).count()

    # Fetch all applicants (candidates)
    applicants = Applicants.query.all()
    # Calculate statistics
    total_quizzes = Quizzes.query.count()

    # Define 'active quizzes' as quizzes with at least one assignment not expired
    current_time = dt.datetime.now(dt.timezone.utc)
    active_quizzes = Quizzes.query.join(Assignments).filter(
        Assignments.expiry > current_time
    ).distinct().count()

    # Define 'pending quizzes' as quizzes with no assignments
    pending_quizzes = Quizzes.query.join(Assignments).filter(
        Assignments.submit_time.is_(None)
    ).distinct().count()

    # Total number of candidates added
    total_candidates = Applicants.query.count()

    stats = {
        'quizzes_created': total_quizzes,
        'active_quizzes': active_quizzes,
        'pending_quizzes': pending_quizzes,
        'candidates_added': total_candidates,
    }
    return render_template(
        'employer/dashboard.html',
        title="Employer Dashboard",
        recent_activities=recent_activities_sorted,
        quizzes=quizzes,
        applicants=applicants,
        stats=stats
    )

@bp.route('/quiz/details', methods=['GET', 'POST'])
# Login required here?
def quiz_details():
    """Route to display and handle the Quiz Details form."""
    form = QuizDetailsForm()
    if form.validate_on_submit():
        # Extract form data
        quiz_title = form.quiz_title.data
        job_title = form.job_title.data
        language = form.language.data
        
        # Create a new quiz instance
        new_quiz = Quizzes(
            name=quiz_title,
            job_title=job_title,
            language=language,
            time_created=dt.datetime.now(dt.timezone.utc)
        )
        db.session.add(new_quiz)
        db.session.commit()
        
        flash('Quiz details saved successfully!', 'success')
        return redirect(url_for('employer.dashboard'))  # Redirect to dashboard or next step
    
    return render_template('employer/quiz_settings1.html', form=form, current_year=dt.datetime.now(dt.timezone.utc).year)


@bp.route('/quiz/add_items/<int:quiz_id>', methods=['GET', 'POST'])
def add_items(quiz_id):
    """Route to add/edit items for a specific quiz"""

    form = AddQuestionForm()
    
    # Fetch quiz data
    quiz = Quizzes.query.get(quiz_id)

    if not quiz:
        flash('Quiz not found. Displaying dummy data.', 'warning')

        # dummy data
        quiz_title = 'Sample Quiz Title'
        questions = []

    
    # Minimal form handling
    if form.validate_on_submit():
        # Placeholder: Flash a success message
        flash('Form submitted successfully!', 'success')
        return redirect(url_for('employer.add_items', quiz_id=quiz_id))
    
    # Prepare context data with dummy or fetched data
    context = {
        'quiz_title': quiz_title,
        'questions': questions,
        'form': form,
        'progress_percentage': 58,  # Static value; adjust as needed
        'current_year': dt.datetime.now().year
    }
        
    return render_template('employer/quiz_settings2.html', **context)

@bp.route('/quiz/quiz_settings/<int:quiz_id>', methods=['GET', 'POST'])
def quiz_settings(quiz_id):
    quiz = Quizzes.query.get(quiz_id)

    if not quiz:
        flash('Quiz not found. Displaying dummy data.', 'warning')

    form = QuizSettingsForm()

    if form.validate_on_submit():
        # Update quiz settings with form data
        quiz.time_limit = form.time_limit.data
        quiz.start_date = form.start_date.data
        quiz.end_date = form.end_date.data
        quiz.randomize = form.randomize.data

    return render_template(
        'employer/quiz_settings3.html',
        form=form,
        quiz_id=quiz_id
    )