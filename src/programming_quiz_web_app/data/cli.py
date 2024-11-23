from programming_quiz_web_app.data import bp
from programming_quiz_web_app.data.seed_data import run_seed

bp.cli.short_help = "Methods to interact with database data."

@bp.cli.command("seed-db")
def seed_db():
    """Seed the database with example data."""
    run_seed()
    print("Database seeding completed.")
