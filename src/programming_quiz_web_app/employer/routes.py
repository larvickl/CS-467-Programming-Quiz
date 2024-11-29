from flask import render_template, flash, redirect, url_for, request, jsonify, current_app
from programming_quiz_web_app.employer import bp
import datetime as dt
from programming_quiz_web_app.models import *
from programming_quiz_web_app.employer.forms import QuizDetailsForm, AddFreeResponseQuestion, AddTrueFalseQuestion, AddChoiceQuestion
from programming_quiz_web_app.employer.forms import AddApplicant, AssignQuiz
from programming_quiz_web_app.main.urls import generate_quiz_url_and_pin
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

@bp.route('/quiz/create', methods=['GET', 'POST'])
# Login required here?
def quiz_details():
    """Route to display and handle the Quiz Details form."""
    form = QuizDetailsForm()
    if form.validate_on_submit():
        # Create a new quiz instance
        #TODO:  Add the actual user id to created_by_id.
        new_quiz = Quizzes(
            name = form.quiz_title.data,
            description = form.quiz_description.data,
            default_time_limit_seconds = int(form.default_time_limit_seconds.data),
            created_by_id = 1)
        # Commit new quiz to the database.
        try:
            db.session.add(new_quiz)
            db.session.commit()
            flash('Quiz saved successfully!', 'success')
            return redirect(url_for('employer.add_items', quiz_id=new_quiz.id))
        except Exception as the_exception:
            current_app.logger.exception(the_exception)
            db.session.rollback()
            flash('Error creating new quiz!', 'danger')
    return render_template('employer/add_quiz.html', form=form, current_year=dt.datetime.now(dt.timezone.utc).year)

@bp.route('/quiz/add_items/<int:quiz_id>', methods=['GET', 'POST'])
def add_items(quiz_id):
    """Route to add items for a specific quiz"""
    # Determine which form, if any, was submitted.
    form_submitted = request.args.get("form", default=None, type=str)
    # Fetch quiz data
    quiz = Quizzes.query.get(quiz_id)
    if not quiz:
        flash('The requested quiz was not found.', 'danger')
        return redirect(url_for('employer.dashboard'))
    # Instantiate the forms.
    form_free = AddFreeResponseQuestion()
    form_tf = AddTrueFalseQuestion()
    form_multi_choice = AddChoiceQuestion()
    form_multi_select = AddChoiceQuestion()
    # Multiple choice form submitted.
    if form_submitted == "form_mc" and form_multi_choice.validate_on_submit():
        new_question = ChoiceQuestions(
            question_type = "multiple-choice",
            title = form_multi_choice.question_title.data,
            body = form_multi_choice.question_body.data,
            auto_grade = True,
            possible_points = form_multi_choice.possible_points.data,
            order = len(quiz.get_ordered_questions()) + 1,
            quiz_id = quiz.id)
        option_one = Options(option_text=form_multi_choice.option_one_text.data, option_weight=form_multi_choice.option_one_weight.data, order=1)
        option_two = Options(option_text=form_multi_choice.option_two_text.data, option_weight=form_multi_choice.option_two_weight.data, order=2)
        option_three = Options(option_text=form_multi_choice.option_three_text.data, option_weight=form_multi_choice.option_three_weight.data, order=3)
        option_four = Options(option_text=form_multi_choice.option_four_text.data, option_weight=form_multi_choice.option_four_weight.data, order=4)
        try:
            db.session.add(new_question)
            # Flush the new question to the database and refresh to get id.
            db.session.flush()
            db.session.refresh(new_question)
            # Add the question ID to the options.
            option_one.question_id = new_question.id
            option_two.question_id = new_question.id
            option_three.question_id = new_question.id
            option_four.question_id = new_question.id
            # Add options to sessions.
            db.session.add_all([option_one, option_two, option_three, option_four])
            # Commit changes to database.
            db.session.commit()
            flash('Multiple Choice question added!', 'success')
            return redirect(url_for('employer.add_items', quiz_id=quiz_id))
        except Exception as the_exception:
            db.session.rollback()
            current_app.logger.exception(the_exception)
            flash('Unable to save the question.  Please try again!', 'danger')
    # Multiple selection submitted.
    elif form_submitted == "form_ms" and form_multi_select.validate_on_submit():
        new_question = ChoiceQuestions(
            question_type = "multiple-selection",
            title = form_multi_select.question_title.data,
            body = form_multi_select.question_body.data,
            auto_grade = True,
            possible_points = form_multi_select.possible_points.data,
            order = len(quiz.get_ordered_questions()) + 1,
            quiz_id = quiz.id
        )
        option_one = Options(option_text=form_multi_select.option_one_text.data, option_weight=form_multi_select.option_one_weight.data, order=1)
        option_two = Options(option_text=form_multi_select.option_two_text.data, option_weight=form_multi_select.option_two_weight.data, order=2)
        option_three = Options(option_text=form_multi_select.option_three_text.data, option_weight=form_multi_select.option_three_weight.data, order=3)
        option_four = Options(option_text=form_multi_select.option_four_text.data, option_weight=form_multi_select.option_four_weight.data, order=4)
        try:
            db.session.add(new_question)
            # Flush the new question to the database and refresh to get id.
            db.session.flush()
            db.session.refresh(new_question)
            # Add the question ID to the options.
            option_one.question_id = new_question.id
            option_two.question_id = new_question.id
            option_three.question_id = new_question.id
            option_four.question_id = new_question.id
            # Add options to sessions.
            db.session.add_all([option_one, option_two, option_three, option_four])
            # Commit changes to database.
            db.session.commit()
            flash('Multiple Selection question added!', 'success')
            return redirect(url_for('employer.add_items', quiz_id=quiz_id))
        except Exception as the_exception:
            db.session.rollback()
            current_app.logger.exception(the_exception)
            flash('Unable to save the question.  Please try again!', 'danger')
    # True/ False choice submitted.
    elif form_submitted == "form_tf" and form_tf.validate_on_submit():
        new_question = ChoiceQuestions(
            question_type = "true-false",
            title = form_tf.question_title.data,
            body = form_tf.question_body.data,
            auto_grade = True,
            possible_points = form_tf.possible_points.data,
            order = len(quiz.get_ordered_questions()) + 1,
            quiz_id = quiz.id)
        # True and False options.
        new_true_option = Options(option_text = "True", option_weight = form_tf.true_option_weight.data, order = 1)
        new_false_option = Options(option_text = "False", option_weight = form_tf.false_option_weight.data, order = 2)
        try:
            db.session.add(new_question)
            # Flush the new question to the database and refresh to get id.
            db.session.flush()
            db.session.refresh(new_question)
            # Add the question ID to the options.
            new_true_option.question_id = new_question.id
            new_false_option.question_id = new_question.id
            # Add questions to session.
            db.session.add(new_true_option)
            db.session.add(new_false_option)
            # Commit change to database.
            db.session.commit()
            flash('True/False question successfully added!', 'success')
            return redirect(url_for('employer.add_items', quiz_id=quiz_id))
        except Exception as the_exception:
            db.session.rollback()
            current_app.logger.exception(the_exception)
            flash('Unable to save the question.  Please try again!', 'danger')
    # Free response submitted.
    elif form_submitted == "form_free" and form_free.validate_on_submit():
        new_question = FreeResponseQuestions(
            title = form_free.question_title.data,
            body = form_free.question_body.data,
            solution = form_free.question_solution.data,
            possible_points = form_free.possible_points.data,
            order = len(quiz.get_ordered_questions()) + 1,
            quiz_id = quiz.id)
        try:
            db.session.add(new_question)
            db.session.commit()
            flash('Free response question successfully added!', 'success')
            return redirect(url_for('employer.add_items', quiz_id=quiz_id))
        except Exception as the_exception:
            db.session.rollback()
            current_app.logger.exception(the_exception)
            flash('Unable to save the question.  Please review errors and try again!', 'danger')
    # Prepare context data with dummy or fetched data
    context = {
        'quiz_id': quiz_id,
        'quiz_title': quiz.name,
        'questions': quiz.get_ordered_questions(),
        'free_response_questions': quiz.free_response_questions,
        'form': form_submitted,
        'form_free': form_free,
        'form_tf': form_tf,
        'form_mc': form_multi_choice,
        'form_ms': form_multi_select,
        'progress_percentage': 58,  # Static value; adjust as needed
        'current_year': dt.datetime.now().year}  
    return render_template('employer/add_question.html', **context)

@bp.route('/applicant/add', methods=['GET', 'POST'])
def add_applicant():
    """Route to add an applicant."""
    # Instantiate Form.
    form = AddApplicant()
    form.timezone.choices = form.timezone.choices + current_app.config["APP_ALL_TIMEZONES"]
    # Validate form.
    if form.validate_on_submit():
        new_applicant = Applicants(
            email = form.email.data,
            surname = form.surname.data,
            given_name = form.given_name.data,
            timezone = form.timezone.data)
        try:
            # Add new applicant.
            db.session.add(new_applicant)
            db.session.commit()
            flash('Successfully added applicant!', 'success')
            return redirect(url_for('employer.dashboard'))
        except Exception as the_exception:
            db.session.rollback()
            current_app.logger.exception(the_exception)
            flash('Unable to add applicant.  Please try again!', 'danger')
    return render_template("employer/add_applicant.html", form=form)

@bp.route('/applicant/assign', methods=['GET', 'POST'])
def assign_quiz():
    """Route to assign an applicant a quiz"""
    # Make applicant choices list.
    applicants_query = db.session.query(Applicants).all()
    applicants_choices = []
    for applicant in applicants_query:
        applicants_choices.append((applicant.id, f"{applicant.surname}, {applicant.given_name} ({applicant.email})"))
    # Make quiz choices list.
    quizzes_query = db.session.query(Quizzes).all()
    quizzes_choices = []
    for quiz in quizzes_query:
        quizzes_choices.append((quiz.id, f"{quiz.name}"))
    # Instantiate Form.
    form = AssignQuiz()
    form.quiz.choices = form.quiz.choices + quizzes_choices
    form.applicant.choices = form.applicant.choices + applicants_choices
    #TODO:  Add the actual user id to created_by_id.
    if form.validate_on_submit():
        # Generate unique URL/ PIN.
        unique_url, url_pin = generate_quiz_url_and_pin()
        # Create assignment.
        new_assignment = Assignments(
            time_limit_seconds = Quizzes.query.get(int(form.quiz.data)).default_time_limit_seconds,
            expiry = form.expiry.data.replace(tzinfo=dt.timezone.utc),
            url = unique_url,
            url_pin = url_pin,
            assigned_by_id = 1,
            quiz_id = int(form.quiz.data),
            applicant_id = int(form.applicant.data))
        try:
            db.session.add(new_assignment)
            db.session.commit()
            flash("Quiz assigned!", 'success')
            return redirect(url_for('employer.dashboard'))
        except Exception as the_exception:
            db.session.rollback()
            flash("Unable to assign quiz!", 'danger')
            current_app.logger.exception(the_exception)
    return render_template("employer/assign_quiz.html", form=form)

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
                'name': f"{assignment.applicant.given_name} {assignment.applicant.surname}",
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
        current_app.logger.exception(e)
        return jsonify({'error': "There was an error fetching the requested data.  Please see the error log for more information."}), 500