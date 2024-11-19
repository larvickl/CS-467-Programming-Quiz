from programming_quiz_web_app import db
import datetime as dt
from programming_quiz_web_app.models import Users, Quizzes, FreeResponseQuestions, ChoiceQuestions, Options, Assignments, Applicants


def seed_data():
    """
    Sets up example data.
    """
    try:
        # Start up database session.
        db.session.begin()

        # Create example users.
        user1 = Users(
            email="john.doe@example.com",
            password_hash="hashedpassword123",
            surname="Doe",
            given_name="John",
            account_state="active",
            account_created=dt.datetime.now(dt.timezone.utc),
            last_login=None
        )

        user2 = Users(
            email="jane.smith@example.com",
            password_hash="hashedpassword456",
            surname="Smith",
            given_name="Jane",
            account_state="active",
            account_created=dt.datetime.now(dt.timezone.utc),
            last_login=None
        )

        # Create example quizzes.
        quiz1 = Quizzes(
            name="Example Quiz 1",
            description="A quiz example 1.",
            default_time_limit_seconds=3600,
            time_created=dt.datetime.now(dt.timezone.utc),
            created_by_id=None
        )

        quiz2 = Quizzes(
            name="Example Quiz 2",
            description="A quiz example 2.",
            default_time_limit_seconds=1800,
            time_created=dt.datetime.now(dt.timezone.utc),
            created_by_id=None
        )

        # Add quizzes and users to get their IDs for relationships.
        db.session.add_all([user1, user2, quiz1, quiz2])
        db.session.flush()

        quiz1.created_by_id = user1.id
        quiz2.created_by_id = user2.id

        # Create example free response questions.
        fr_question1 = FreeResponseQuestions(
            title="Explain the concept of recursion.",
            body="What is recursion in programming? Provide an example in any language to illustrate your explanation.",
            solution="Recursion is a method of solving problems where the solution depends on solving smaller instances of the same problem.",
            possible_points=10.0,
            order=1,
            quiz_id=quiz1.id
        )

        fr_question2 = FreeResponseQuestions(
            title="Understanding RESTful APIs",
            body="What is a RESTful API? Explain its core principles.",
            solution=(
                "A RESTful API (Representational State Transfer) is an architectural style for designing networked applications. "
                "Its core principles include stateless communication, a uniform interface, and the use of standard HTTP methods (GET, POST, PUT, DELETE) for CRUD operations. "
            ),
            possible_points=8.0,
            order=2,
            quiz_id=quiz1.id
        )

        fr_question3 = FreeResponseQuestions(
            title="HTTP Methods",
            body="Describe the differences between GET and POST HTTP methods. Provide examples of when to use each.",
            solution="GET is used to retrieve data from a server and should not change server state. POST is used to send data to the server, often to create or update resources.",
            possible_points=5.0,
            order=1,
            quiz_id=quiz2.id
        )

        fr_question4 = FreeResponseQuestions(
            title="Time Complexity Analysis",
            body="What is time complexity? Analyze the time complexity of the following function:\n\n def find_max(arr):\n    max_val = arr[0]\n    for num in arr:\n        if num > max_val:\n            max_val = num\n    return max_val",
            solution="Time complexity is a measure of the computational effort needed as the size of the input grows. The time complexity for this function is O(n).",
            possible_points=7.0,
            order=2,
            quiz_id=quiz2.id
        )


        # Create example multiple choice questions and options.
        mc_question1 = ChoiceQuestions(
            question_type="multiple-choice",
            title="What is Flask?",
            body="Select the correct definition of Flask.",
            auto_grade=True,
            possible_points=5,
            order=3,
            quiz_id=quiz1.id
        )
        options1 = [
            Options(option_text="A Python web framework.", option_weight=1, order=1, question=mc_question1),
            Options(option_text="A JavaScript library.", option_weight=0, order=2, question=mc_question1)
        ]

        mc_question2 = ChoiceQuestions(
            question_type="true-false",
            title="Python is a statically-typed programming language.",
            body="Indicate whether the statement is True or False.",
            auto_grade=True,
            possible_points=5,
            order=3,
            quiz_id=quiz2.id
        )
        options2 = [
            Options(option_text="True", option_weight=0, order=1, question=mc_question2),
            Options(option_text="False", option_weight=1, order=2, question=mc_question2)
        ]

        mc_question3 = ChoiceQuestions(
            question_type="multiple-choice",
            title="What does the len() function return in Python?",
            body="Choose the correct explanation of the len() function in Python.",
            auto_grade=True,
            possible_points=5,
            order=4,
            quiz_id=quiz1.id
        )
        options3 = [
        Options(option_text="The number of elements in an iterable.", option_weight=1, order=1, question=mc_question3),
        Options(option_text="The data type of an object.", option_weight=0, order=2, question=mc_question3),
        Options(option_text="The memory address of an object.", option_weight=0, order=3, question=mc_question3)
        ]

        mc_question4 = ChoiceQuestions(
            question_type="multiple-choice",
            title="Which HTTP method is used to update an existing resource in a web application?",
            body="Select the HTTP method typically used to update an existing resource.",
            auto_grade=True,
            possible_points=5,
            order=5,
            quiz_id=quiz1.id
        )
        options4 = [
        Options(option_text="GET", option_weight=0, order=1, question=mc_question4),
        Options(option_text="POST", option_weight=0, order=2, question=mc_question4),
        Options(option_text="PUT", option_weight=1, order=3, question=mc_question4)
        ]

        mc_question5 = ChoiceQuestions(
            question_type="true-false",
            title="Python is a statically-typed programming language.",
            body="Decide if the statement is True or False.",
            auto_grade=True,
            possible_points=5,
            order=3,
            quiz_id=quiz2.id
        )
        options5 = [
        Options(option_text="True", option_weight=0, order=1, question=mc_question5),
        Options(option_text="False", option_weight=1, order=2, question=mc_question5)
        ]

        mc_question6 = ChoiceQuestions(
            question_type="true-false",
            title="Flask includes built-in support for database models.",
            body="Decide if the statement is True or False.",
            auto_grade=True,
            possible_points=5,
            order=4,
            quiz_id=quiz2.id
        )
        options6 = [
        Options(option_text="True", option_weight=0, order=1, question=mc_question6),
        Options(option_text="False", option_weight=1, order=2, question=mc_question6)
        ]

        # Add all questions and options.
        db.session.add_all([fr_question1,fr_question2,fr_question3, fr_question4])
        db.session.add_all([mc_question1, mc_question2, mc_question3, mc_question4, mc_question5, mc_question6])
        db.session.add_all(options1)
        db.session.add_all(options2)
        db.session.add_all(options3)
        db.session.add_all(options4)
        db.session.add_all(options5)
        db.session.add_all(options6)

        # Create example assignments.
        assignment1 = Assignments(
            time_limit_seconds=3600,
            expiry=dt.datetime(2024, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc),
            start_time=dt.datetime(2024, 11, 20, 10, 0, 0, tzinfo=dt.timezone.utc),
            submit_time=None,
            score=None,
            url=url_generation('quiz.assignment', assignment_id=1, _external=True),
            url_pin="ABC123",
            assigned_by_id=user1.id,
            quiz_id=quiz1.id
        )

        assignment2 = Assignments(
            time_limit_seconds=5400,
            expiry=dt.datetime(2024, 12, 25, 23, 59, 59, tzinfo=dt.timezone.utc),
            start_time=dt.datetime(2024, 11, 22, 15, 30, 0, tzinfo=dt.timezone.utc),
            submit_time=dt.datetime(2024, 11, 22, 16, 45, 0, tzinfo=dt.timezone.utc),
            score=85.5,
            url=url_generation('quiz.assignment', assignment_id=2, _external=True),
            url_pin="DEF456",
            assigned_by_id=user2.id,
            quiz_id=quiz2.id
        )
        db.session.add_all([assignment1,assignment2])

        # Create example applicants.
        applicant1 = Applicants(
            email="james.brown@example.com",
            surname="Brown",
            given_name="James",
            timezone="America/New_York"
        )

        applicant2 = Applicants(
            email="emily.lee@example.com",
            surname="Lee",
            given_name="Emily",
            timezone="America/Seattle"
        )

        db.session.add_all([applicant1, applicant2])

        # Commit changes to the database.
        db.session.commit()
        print("Data added successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")

def run_seed():
    seed_data()
