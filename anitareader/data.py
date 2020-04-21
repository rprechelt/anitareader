"""
This module searches for ANITA flight data and for local anitareader data.
"""
import glob
import os
import os.path as path
import re
from typing import List

__all__ = ["get_directory", "is_available", "available_runs"]

# this is the anitareader/data directory
LOCAL_DATA = path.join(path.dirname(path.dirname(__file__)), "data")

# try and get the directory where data is stored.
ANITA1_DATA = os.getenv("ANITA1_ROOT_DATA")
ANITA2_DATA = os.getenv("ANITA2_ROOT_DATA")
ANITA3_DATA = os.getenv("ANITA3_ROOT_DATA")
ANITA4_DATA = os.getenv("ANITA4_ROOT_DATA")


def get_directory(flight: int) -> str:
    """
    Return the directory containing ROOT data for a given flight.

    If the appropriate environment variables are not set, this
    return the empty string ("").

    Parameters
    ----------
    flight: int
        The flight number to return.

    Returns
    ----------
    path: str
        The absolute path to the directory containing flight ROOT data.

    Raises
    ------
    ValueError
        If the flight number is not valid.

    """
    if flight == 1:
        return ANITA1_DATA or ""
    elif flight == 2:
        return ANITA2_DATA or ""
    elif flight == 3:
        return ANITA3_DATA or ""
    elif flight == 4:
        return ANITA4_DATA or ""
    else:
        raise ValueError(f"{flight} is not a valid flight number.")


def is_available(flight: int) -> bool:
    """
    Check whether data from the given flight is available on this local system.

    Parameters
    ----------
    flight: int
        The flight number of the desired data.

    Returns
    -------
    available: bool
        True if this flight data is available.

    Raises
    ------
    ValueError
        If passed invalid flight number.
    """

    if flight == 4:
        if not ANITA4_DATA or not path.exists(ANITA4_DATA):
            return False
    elif flight == 3:
        if not ANITA3_DATA or not path.exists(ANITA3_DATA):
            return False
    elif flight == 2:
        if not ANITA2_DATA or not path.exists(ANITA2_DATA):
            return False
    elif flight == 1:
        if not ANITA1_DATA or not path.exists(ANITA1_DATA):
            return False
    else:
        raise ValueError(f"{flight} is not a valid flight number.")

    # if we get here, then the data is present.
    return True


def available_runs(flight: int) -> List[int]:
    """
    Load the list of available runs for this flight.

    This method does not safely check that the files are available.

    Parameters
    ----------
    flight: int
        The flight data to check.

    Returns
    -------
    runs: List[int]
        The available list of run numbers.
    """

    # get the data directory for this flight
    directory = get_directory(flight)

    # get the list of run directories
    directories = glob.glob(path.join(directory, "run*"))

    # and extract the runs from these directories
    runs = [int(re.sub(r"\D", "", path.basename(d))) for d in directories]

    # and return the available runs
    return runs
