from flask import render_template, flash, redirect, url_for, request, current_app
from programming_quiz_web_app.employer import bp
import datetime as dt
from programming_quiz_web_app.models import *
from programming_quiz_web_app.employer.forms import QuizDetailsForm, AddFreeResponseQuestion, AddTrueFalseQuestion, AddChoiceQuestion
from programming_quiz_web_app.employer.forms import AddApplicant
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
    recent_applicants = Applicants.query.order_by(Applicants.id.desc()).limit(8).all()
    for applicant in recent_applicants:
        recent_activities.append({
            'description': f"Candidate {applicant.given_name} {applicant.surname} added...",
        })

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
        recent_activities=recent_activities,
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
        # Create a new quiz instance
        #TODO:  Add the actual user id to created_by_id.
        new_quiz = Quizzes(
            name = form.quiz_title.data,
            description = form.quiz_description.data,
            default_time_limit_seconds = int(form.default_time_limit_seconds.data),
            created_by_id = 21)
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