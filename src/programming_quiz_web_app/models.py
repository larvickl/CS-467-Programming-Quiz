import datetime as dt
import sqlalchemy.types as types
from sqlalchemy.dialects.mysql import TEXT, MEDIUMTEXT, LONGTEXT
from sqlalchemy.orm import Mapped
from typing import Optional, List
from programming_quiz_web_app import db, login_manager
from flask_login import UserMixin

class TZDateTime(types.TypeDecorator):
    """A database column type that enforces correct time zones.  Aware datetimes
    are first converted to UTC and then have the tzinfo removed before committing
    to the database.  Naive datetimes are rejected.  The UTC time zone is added to
    all results retrieved from the database."""
    impl = types.DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """This method will reject naive datetimes and convert aware datetimes to
        UTC before committing to the database as a UTC naive datetime."""
        if value is not None:
            if not value.tzinfo or value.tzinfo.utcoffset(value) is None:
                raise TypeError("tzinfo is required")
            value = value.astimezone(dt.timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        """This method will convert datetimes from the database to aware UTC datetimes."""
        if value is not None:
            value = value.replace(tzinfo=dt.timezone.utc)
        return value


# The UsersPermissions association table.
users_permissions = db.Table(
    "UsersPermissions",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("Users.id"), primary_key=True),
    db.Column("permission_id", db.ForeignKey("Permissions.id"), primary_key=True)
)

class Users(db.Model, UserMixin):
    """The schema for the Users table."""
    __tablename__ = 'Users'
    # Columns.
    id: Mapped[int] = db.mapped_column(db.Integer, primary_key=True, unique=True, index=True)
    email: Mapped[str] = db.mapped_column(db.String(300), unique=True, index=True)
    password_hash: Mapped[str] = db.mapped_column(db.String(300))
    surname: Mapped[str] = db.mapped_column(db.String(100), index=True)
    given_name: Mapped[str] = db.mapped_column(db.String(100))
    account_state: Mapped[str] = db.mapped_column(db.String(45), index=True)
    account_created: Mapped[dt.datetime] = db.mapped_column(TZDateTime)
    last_login: Mapped[Optional[dt.datetime]] = db.mapped_column(TZDateTime)
    token: Mapped[Optional[str]] = db.mapped_column(TEXT)
    # Relationships.
    quizzes: Mapped[List["Quizzes"]] = db.relationship("Quizzes", back_populates="created_by")
    assignments: Mapped[List["Assignments"]] = db.relationship("Assignments", back_populates="assigned_by")
    permissions: Mapped[List["Permissions"]] = db.relationship(secondary=users_permissions, back_populates="users")

    def get_id(self) -> int:
        """Return the id for a row of the Users table.

        Returns
        -------
        int
            The user's ID.
        """
        return self.id   


class Permissions(db.Model):
    """The schema for the Permissions table."""
    __tablename__ = 'Permissions'
    # Columns.
    id: Mapped[int] = db.mapped_column(db.Integer(), unique=True, primary_key=True)
    name: Mapped[str] = db.mapped_column(db.String(100), unique=True, index=True)
    # Relationships.
    users: Mapped[List["Users"]] = db.relationship(secondary=users_permissions, back_populates="permissions")


class Quizzes(db.Model):
    """The schema for the Quizzes table."""
    __tablename__ = 'Quizzes'
    # Columns.
    id: Mapped[int] = db.mapped_column(db.Integer(), unique=True, primary_key=True)
    name: Mapped[str] = db.mapped_column(db.String(300), unique=True, index=True)
    description: Mapped[Optional[str]] = db.mapped_column(MEDIUMTEXT)
    default_time_limit_seconds: Mapped[int] = db.mapped_column(db.Integer())
    time_created: Mapped[dt.datetime] = db.mapped_column(TZDateTime, index=True, default=dt.datetime.now(dt.timezone.utc))
    # Foreign keys.
    created_by_id: Mapped[int] = db.mapped_column(
        db.Integer(),
        db.ForeignKey("Users.id", ondelete='RESTRICT', onupdate="CASCADE"))
    # Relationships.
    created_by: Mapped["Users"] = db.relationship("Users", back_populates="quizzes")
    assignments: Mapped[List["Assignments"]] = db.relationship("Assignments", back_populates="quiz")
    choice_questions: Mapped[List["ChoiceQuestions"]] = db.relationship("ChoiceQuestions", back_populates="quiz", order_by="ChoiceQuestions.id")
    free_response_questions: Mapped[List["FreeResponseQuestions"]] = db.relationship("FreeResponseQuestions", back_populates="quiz", order_by="FreeResponseQuestions.id")
    # Methods
    def get_ordered_questions(self):
        """Get all questions ordered by "order".

            Returns
            -------
            list[ChoiceQuestions, FreeResponseQuestions]
                A list containing the ordered questions.
        """
        def get_order(entry: ChoiceQuestions | FreeResponseQuestions) -> int:
            """A function to get the order of a ChoiceQuestion or a FreeResponseQuestion for sorting.

            Parameters
            ----------
            entry : ChoiceQuestions | FreeResponseQuestions
                The item to get the order of.

            Returns
            -------
            int
                The question order.
            """
            return entry.order
        
        # Get all questions.
        all_questions = self.choice_questions + self.free_response_questions
        all_questions.sort(key=get_order)
        return all_questions


class FreeResponseQuestions(db.Model):
    """The schema for the FreeResponseQuestions table."""
    __tablename__ = 'FreeResponseQuestions'
    id: Mapped[int] = db.mapped_column(db.Integer(), unique=True, primary_key=True)
    title: Mapped[str] = db.mapped_column(db.String(300))
    body: Mapped[str] = db.mapped_column(MEDIUMTEXT)
    solution: Mapped[str] = db.mapped_column(MEDIUMTEXT)
    possible_points: Mapped[float] = db.mapped_column(db.Double)
    order: Mapped[int] = db.mapped_column(db.Integer(), index=True)
    # Foreign keys.
    quiz_id: Mapped[int] = db.mapped_column(
        db.Integer(),
        db.ForeignKey("Quizzes.id", ondelete='CASCADE', onupdate="CASCADE"))
    # Relationships.
    quiz: Mapped["Quizzes"] = db.relationship("Quizzes", back_populates="free_response_questions")


class ChoiceQuestions(db.Model):
    """The schema the the ChoiceQuestions table."""
    __tablename__ = 'ChoiceQuestions'
    id: Mapped[int] = db.mapped_column(db.Integer(), unique=True, primary_key=True)
    question_type: Mapped[str] = db.mapped_column(db.String(45))
    title: Mapped[str] = db.mapped_column(db.String(300))
    body: Mapped[str] = db.mapped_column(MEDIUMTEXT)
    auto_grade: Mapped[bool] = db.mapped_column(db.Boolean())
    possible_points: Mapped[float] = db.mapped_column(db.Double)
    order: Mapped[int] = db.mapped_column(db.Integer(), index=True)
    # Foreign keys.
    quiz_id: Mapped[int] = db.mapped_column(
        db.Integer(),
        db.ForeignKey("Quizzes.id", ondelete='CASCADE', onupdate="CASCADE"))
    # Relationships.
    quiz: Mapped["Quizzes"] = db.relationship("Quizzes", back_populates="choice_questions")
    options: Mapped[List["Options"]] = db.relationship("Options", back_populates="question")


class Options(db.Model):
    """The schema for the Options table."""
    __tablename__ = 'Options'
    id: Mapped[int] = db.mapped_column(db.Integer(), unique=True, primary_key=True)
    option_text: Mapped[str] = db.mapped_column(MEDIUMTEXT)
    option_weight: Mapped[int] = db.mapped_column(db.Integer())
    order: Mapped[int] = db.mapped_column(db.Integer(), index=True)
    # Foreign keys.
    question_id: Mapped[int] = db.mapped_column(
        db.Integer(),
        db.ForeignKey("ChoiceQuestions.id", ondelete='CASCADE', onupdate="CASCADE"))
    # Relationships.
    question: Mapped["ChoiceQuestions"] = db.relationship("ChoiceQuestions", back_populates="options")


class Assignments(db.Model):
    """The schema for the Assignments table."""
    __tablename__ = 'Assignments'
    # Columns.
    id: Mapped[int] = db.mapped_column(db.Integer(), unique=True, primary_key=True)
    time_limit_seconds: Mapped[int] = db.mapped_column(db.Integer())
    expiry: Mapped[dt.datetime] = db.mapped_column(TZDateTime)
    start_time: Mapped[Optional[dt.datetime]] = db.mapped_column(TZDateTime)
    submit_time: Mapped[Optional[dt.datetime]] = db.mapped_column(TZDateTime)
    score: Mapped[Optional[float]] = db.mapped_column(db.Double)
    url: Mapped[Optional[str]] = db.mapped_column(db.String(191), unique=True)
    url_pin: Mapped[Optional[str]] = db.mapped_column(db.String(10))
    # Foreign keys.
    assigned_by_id: Mapped[int] = db.mapped_column(
        db.Integer(),
        db.ForeignKey("Users.id", ondelete='RESTRICT', onupdate="CASCADE"))
    quiz_id: Mapped[int] = db.mapped_column(
        db.Integer(),
        db.ForeignKey("Quizzes.id", ondelete='RESTRICT', onupdate="CASCADE"))
    applicant_id: Mapped[int] = db.mapped_column(
        db.Integer(),
        db.ForeignKey("Applicants.id", ondelete='RESTRICT', onupdate="CASCADE"))
    # Relationships.
    applicant: Mapped["Applicants"] = db.relationship("Applicants", back_populates="assignments")
    assigned_by: Mapped["Users"] = db.relationship("Users", back_populates="assignments")
    quiz: Mapped["Quizzes"] = db.relationship("Quizzes", back_populates="assignments")
    answers: Mapped[List["Answers"]] = db.relationship("Answers", back_populates="assignment")
    # Methods
    def is_graded(self) -> bool:
        """Return True if all questions graded, False otherwise.

        Returns
        -------
        bool
            True if all questions graded, False otherwise
        """
        for answer in self.answers:
            if answer.awarded_points is None:
                return False
        return True
    
    def get_results(self) -> dict[str, int | float]:
        """Get the results of the quiz.

        Returns
        -------
        dict[str, int | float]
            Get the results of the quiz.
        """
        results = {
            "ungraded_count": 0,
            "total_score": 0,
            "possible_points":0,
            "possible_points_graded_only":0,
        }
        for answer in self.answers:
            results["possible_points"] += answer.possible_points
            # If the question is not yet graded.
            if answer.awarded_points is None:
                results["ungraded_count"] += 1
            else:  # The question is graded.
                results["possible_points_graded_only"] += answer.possible_points
                results["total_score"] += answer.awarded_points
        return results
                


class Answers(db.Model):
    """The schema for the Answers table."""
    __tablename__ = 'Answers'
    id: Mapped[int] = db.mapped_column(db.Integer(), unique=True, primary_key=True)
    question_type: Mapped[str] = db.mapped_column(db.String(45))
    question_title: Mapped[str] = db.mapped_column(db.String(300))
    question: Mapped[str] = db.mapped_column(LONGTEXT)
    question_solution: Mapped[str] = db.mapped_column(MEDIUMTEXT)
    answer: Mapped[Optional[str]] = db.mapped_column(MEDIUMTEXT)
    possible_points: Mapped[float] = db.mapped_column(db.Double)
    awarded_points: Mapped[Optional[float]] = db.mapped_column(db.Double)
    question_id: Mapped[int] = db.mapped_column(db.Integer())
    # Foreign keys.
    assignment_id: Mapped[int] = db.mapped_column(
        db.Integer(),
        db.ForeignKey("Assignments.id", ondelete='CASCADE', onupdate="CASCADE"))
    # Relationship.
    assignment: Mapped["Assignments"] = db.relationship("Assignments", back_populates="answers")


class Applicants(db.Model):
    """The schema for the Applicants table."""
    __tablename__ = 'Applicants'
    id: Mapped[int] = db.mapped_column(db.Integer(), unique=True, primary_key=True)
    email: Mapped[str] = db.mapped_column(db.String(300), unique=True, index=True)
    surname: Mapped[str] = db.mapped_column(db.String(100), index=True)
    given_name: Mapped[str] = db.mapped_column(db.String(100))  
    timezone: Mapped[str] = db.mapped_column(db.String(100))
    # Relationship.
    assignments: Mapped[List["Assignments"]] = db.relationship("Assignments", back_populates="applicant")

@login_manager.user_loader
def load_user(id: int | str) -> Users | None:
    """Return a user given the user's ID.

    Parameters
    ----------
    id : int | str
        The user's ID.

    Returns
    -------
    Users | None
        The user with the given ID, or None if no such user can be found.
    """
    return Users.query.get(int(id))