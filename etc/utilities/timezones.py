import zoneinfo
from ftplib import FTP

def get_iana_backward() -> str:
    """Download the IANA backward file via FTP.

    Returns
    -------
    str
        The IANA backward file.
    """
    def dummy_callback(line):
        """A Simple Dummy Callback to prevent ftp.retrlines from printing to the terminal.

        Parameters
        ----------
        line : str
            The last line read.
        """
        return
    # Connect to FTP server and download file.
    ftp = FTP('ftp.iana.org')
    ftp.login()
    ftp.cwd("tz")
    ftp.cwd("data")
    # Get backward file.
    backward = ftp.retrlines('RETR backward', callback=dummy_callback)
    return backward

def parse_depreciated_zones(backward: str) -> set[str]:
    """Parse the IANA backward file for depreciated timezones.

    Parameters
    ----------
    backward : str
        _description_

    Returns
    -------
    set[str]
        _description_
    """
    # Time zones to exclude .
    depreciated_zones = {"GMT", "Factory", "build/etc/localtime", "Universal", "W-SU", "WET", "Zulu"}
    backward_lines = backward.splitlines()
    for line in backward_lines:
        line = line.strip()
        # Parse each line to find time zones to exclude.
        if line.startswith("Link"):
            line_dict = line.split()
            if len(line_dict) >= 3:
                depreciated_zones.add(line_dict[2].strip())
    return depreciated_zones

def find_available_current_zones(depreciated_zones: set[str]) -> list[tuple[str, str]]:
    """Find all timezones installed locally that are not included in "depreciated_zones" set.

    Parameters
    ----------
    depreciated_zones : set[str]
        The set of depreciated timezones to exclude.

    Returns
    -------
    list[tuple[str, str]]
        A list containing tuples where the first element of the tuple is the timezone's
        name and the second string is its display name.
    """
    # get sorted list of all available, not excluded time zones.
    all_zones = list(zoneinfo.available_timezones() - depreciated_zones)
    all_zones.sort()
    zone_lst = []
    # Reverse the sign in the display names for Etc/GMT* timezones.
    for zone in all_zones:
        if zone.startswith("Etc/GMT-"):
            display_name = zone.replace("-", "+")
        elif zone.startswith("Etc/GMT+"):
            display_name = zone.replace("+", "-")
        else:
            display_name = zone
        display_name = display_name.replace("_", " ").replace("Etc/", "")
        zone_lst.append((zone, display_name))
    return zone_lst

def get_timezones() -> list[tuple[str, str]]:
    """Get all timezones that are not depreciated and installed locally.

    Returns
    -------
    list[tuple[str, str]]
        A list containing tuples where the first element of the tuple is the timezone's
        name and the second string is its display name.
    """
    backward = get_iana_backward()
    depreciated_zones = parse_depreciated_zones(backward)
    available_zones = find_available_current_zones(depreciated_zones)
    return available_zones

def make_timezones_file_list() -> None:
    """Make a file containing all timezones that are not depreciated and installed locally."""
    zone_lst = get_timezones()
    # Make string to write.
    zones_str = "all_time_zones = (\n"
    for zone in zone_lst:
        zones_str  = zones_str + f"    {str(zone)},\n"
    zones_str = zones_str + ")"
    # Write timezones to file.
    with open("timezone_list.py", "w") as fp:
        fp.write(zones_str)

if __name__ == "__main__":
    make_timezones_file_list()