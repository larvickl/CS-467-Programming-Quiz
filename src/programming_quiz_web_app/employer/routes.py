from flask import render_template, flash, redirect, url_for, request, jsonify
from programming_quiz_web_app.employer import bp
import datetime as dt
from programming_quiz_web_app.models import *
from programming_quiz_web_app.employer.forms import QuizDetailsForm, AddQuestionForm, QuizSettingsForm
from programming_quiz_web_app import db


@bp.route('/dashboard')
def dashboard():
    """This is the endpoint for the dashboard."""
    # Recent activities
    recent_quizzes = Quizzes.query.order_by(Quizzes.time_created.desc()).limit(6).all()
    recent_activities = []
    
    for quiz in recent_quizzes:
        recent_activities.append({
            'description': f"Quiz '{quiz.name}' created...",
            'timestamp': quiz.time_created.isoformat() if quiz.time_created else None
        })

    recent_applicants = Applicants.query.order_by(Applicants.id.desc()).limit(8).all()
    for applicant in recent_applicants:
        recent_activities.append({
            'description': f"Candidate {applicant.given_name} {applicant.surname} added...",
            'timestamp': None  # Add timestamp if available in your model
        })

    # Quizzes
    quizzes = Quizzes.query.all()
    serialized_quizzes = []
    for quiz in quizzes:
        sent_count = Assignments.query.filter_by(quiz_id=quiz.id).count()
        takers_count = Assignments.query.filter_by(quiz_id=quiz.id).filter(
            Assignments.submit_time.isnot(None)
        ).count()
        
        serialized_quizzes.append({
            'id': quiz.id,
            'name': quiz.name,
            'sent': sent_count,
            'takers': takers_count
        })

    # Applicants
    applicants = Applicants.query.all()
    serialized_applicants = []
    for applicant in applicants:
        serialized_applicants.append({
            'id': applicant.id,
            'given_name': applicant.given_name,
            'surname': applicant.surname,
            'email': applicant.email,
            'assignments': [{
                'id': assignment.id,
                'quiz': {
                    'id': assignment.quiz.id,
                    'name': assignment.quiz.name
                }
            } for assignment in applicant.assignments]
        })

    # Stats
    current_time = dt.datetime.now(dt.timezone.utc)
    stats = {
        'quizzes_created': Quizzes.query.count(),
        'active_quizzes': Quizzes.query.join(Assignments).filter(
            Assignments.expiry > current_time
        ).distinct().count(),
        'pending_quizzes': Quizzes.query.join(Assignments).filter(
            Assignments.submit_time.is_(None)
        ).distinct().count(),
        'candidates_added': Applicants.query.count()
    }

    # Single data structure for React
    dashboard_data = {
        'recentActivities': recent_activities,
        'quizzes': serialized_quizzes,
        'applicants': serialized_applicants,
        'stats': stats
    }

    # Only pass dashboard_data to the template
    return render_template(
        'employer/dashboard.html',
        dashboard_data=dashboard_data,
        stats=stats,                    
        quizzes=serialized_quizzes,     
        applicants=serialized_applicants,
        recent_activities=recent_activities
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

@bp.route('/employer/quiz/<int:quiz_id>/results')
def quiz_results(quiz_id):
    try:
        # Get all assignments for this quiz that have been submitted
        assignments = Assignments.query.filter(
            Assignments.quiz_id == quiz_id,
            Assignments.submit_time.isnot(None)
        ).all()
        
        # Calculate statistics
        total_attempts = len(assignments)
        if total_attempts > 0:
            total_score = sum(assignment.score for assignment in assignments)
            average_score = round(total_score / total_attempts, 1)
            completion_rate = round((len(assignments) / Assignments.query.filter_by(quiz_id=quiz_id).count()) * 100, 1)
            
            total_minutes = sum(
                (assignment.submit_time - assignment.start_time).total_seconds() / 60 
                for assignment in assignments
            )
            avg_minutes = round(total_minutes / total_attempts)
            avg_time_taken = f"{avg_minutes // 60:02d}:{avg_minutes % 60:02d}" 
        else:
            average_score = 0
            completion_rate = 0
            avg_time_taken = "0:00"

        # Format results
        results = []
        for assignment in assignments:
            results.append({
                'id': assignment.id,
                'name': f"{assignment.applicants[0].given_name} {assignment.applicants[0].surname}",
                'score': assignment.score,
                'timeTaken': (assignment.submit_time - assignment.start_time).total_seconds() / 60,
                'completionDate': assignment.submit_time.strftime("%Y-%m-%d %H:%M")
            })
        
        # Sort by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'overview': {
                'averageScore': average_score,
                'completionRate': completion_rate,
                'totalAttempts': total_attempts,
                'averageTimeTaken': avg_time_taken
            },
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500