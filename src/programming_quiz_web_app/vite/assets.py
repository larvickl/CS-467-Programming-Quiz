import json
import os
from flask import current_app
from typing import Callable
from programming_quiz_web_app.vite import bp

@bp.app_context_processor
def add_context() -> dict[str, bool | Callable[[str], str]]:
    """Make context processors to determine the path to the correct asset file depending
    on the current Vite mode and to determine if Vite is in production mode or not.

    Returns
    -------
    dict[str, bool | Callable[[str], str]]
        A dictionary containing the context processors.

    Raises
    ------
    OSError
        If in production mode and if the manifest.json file does not exist.
    KeyError
        If in production mode and if the requested asset is not in the manifest.json file.
    """
    # Get VITE config.
    vite_mode = current_app.config["VITE_MODE"]
    vite_origin = current_app.config["VITE_ORIGIN"]
    project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vite-flask-integration")

    # Check if in production mode
    is_vite_production = True if vite_mode.lower() == "production" else False

    def get_development_asset(file_path: str) -> str:
        """Return the path to the asset in development mode.

        Parameters
        ----------
        file_path : str
            The path to the asset's source (i.e., .tsx) file.

        Returns
        -------
        str
            The path to the development asset.
        """
        return f"{vite_origin}/assets/{file_path}"

    def get_production_asset(file_path: str) -> str:
        """Return the path to the compiled asset in production mode.

        Parameters
        ----------
        file_path : str
            The path to the asset's source (i.e. .tsx) file.

        Returns
        -------
        str
            The path to the compiled asset.

        Raises
        ------
        OSError
            If the manifest.json file does not exist.
        KeyError
            If the requested asset is not in the manifest.json file.
        """
        # Load the manifest file.
        assets_compiled_path = os.path.join(project_path, "assets_compiled")
        manifest_path = os.path.join(assets_compiled_path, "manifest.json")
        try:
            with open(manifest_path, "r") as fd:
                manifest = json.load(fd)
        except OSError as the_exception:
            raise OSError(f"Manifest file not found.") from the_exception
        # Return path to the production asset.
        try:
            return f"/assets/{manifest[file_path]['file']}"
        except KeyError as the_exception:
            raise KeyError(f"Asset: {file_path} not found.") from the_exception
    
    return {
        "vite_asset": get_production_asset if is_vite_production else get_development_asset,
        "is_vite_production": is_vite_production,
    }
