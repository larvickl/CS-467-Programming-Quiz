import subprocess
import click
from programming_quiz_web_app.vite import bp, project_path

bp.cli.short_help = "Methods to interact with Vite."

@bp.cli.command()
def run():
    """Run the Vite development server."""
    subprocess.run(["npm", "run", "dev"], cwd=project_path)

@bp.cli.command()
def build():
    """Build the Vite assets for production."""
    subprocess.run(["npm", "run", "build"], cwd=project_path)

@bp.cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def npm(args):
    """Run NPM commands."""
    subprocess.run(["npm", *args], cwd=project_path)