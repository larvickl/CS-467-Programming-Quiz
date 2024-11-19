from flask import Flask
from seed_data import run_seed

def register_cli_commands(app: Flask):
    @app.cli.command("seed-db")
    def seed_db():
        """Seed the database with example data."""
        run_seed()
        print("Database seeding completed.")
