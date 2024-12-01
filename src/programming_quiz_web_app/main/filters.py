from programming_quiz_web_app.main import bp

@bp.app_template_filter("format_time_interval")
def format_time_interval(time_seconds: int) -> str:
    """Format an integer number of seconds as a string.

    Parameters
    ----------
    time_seconds : int
        total seconds.

    Returns
    -------
    str
        The formatted time string.
    """
    # Calculate the time units.
    days, remainder = divmod(time_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    # Format the string.
    formatted_string = ""
    if seconds > 0:
        formatted_string = f"{int(seconds)} second{'s' if seconds != 1 else ''}"
    if minutes > 0:
        formatted_string = f"{int(minutes)} minute{'s' if minutes != 1 else ''}{', ' if len(formatted_string) > 0 else ''}" + formatted_string
    if hours > 0:
        formatted_string = f"{int(hours)} hour{'s' if hours != 1 else ''}{', ' if len(formatted_string) > 0 else ''}" + formatted_string
    if days > 0:
        formatted_string = f"{int(days)} day{'s' if days != 1 else ''}{', ' if len(formatted_string) > 0 else ''}" + formatted_string
    return formatted_string