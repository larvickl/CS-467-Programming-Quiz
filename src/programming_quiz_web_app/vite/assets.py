import json
import os
from flask import current_app
from typing import Callable
from programming_quiz_web_app.vite import bp, project_path

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
            The HTML to load the development asset.
        """
        asset_path = f"{vite_origin}/assets/{file_path}"
        return f'<script type="module" src="{asset_path}"></script>'

    def get_production_asset(file_path: str) -> str:
        """Return the path to the compiled asset in production mode.

        Parameters
        ----------
        file_path : str
            The path to the asset's source (i.e. .tsx) file.

        Returns
        -------
        str
            The HTML to load the development asset (JS and CSS).

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
        asset_html = ""
        try:
            with open(manifest_path, "r") as fd:
                manifest = json.load(fd)
        except OSError as the_exception:
            raise OSError(f"Manifest file not found.") from the_exception
        # Return path to the production assets.
        try:
            # Add CSS file(s) to HTML.
            if "css" in manifest[file_path].keys():
                for css_file in manifest[file_path]["css"]:
                    asset_css_path = f"/assets/{css_file}"
                    asset_html = asset_html + f'\n<link rel="stylesheet" href="{asset_css_path}">'
            # Add Script to HTML.
            asset_script_path = f"/assets/{manifest[file_path]['file']}"
            asset_html = asset_html + f'\n<script type="module" src="{asset_script_path}"></script>'
        except KeyError as the_exception:
            raise KeyError(f"Asset: {file_path} not found.") from the_exception
        return asset_html
    
    return {
        "vite_asset": get_production_asset if is_vite_production else get_development_asset,
        "is_vite_production": is_vite_production,
    }
