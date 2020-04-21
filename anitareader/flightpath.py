"""
This module provides methods to load the flightpath
data of various ANITA flights. This loads the flightpath
into an xarray Dataset.
"""
import os.path as path

import uproot
import xarray as xr

from anitareader.data import LOCAL_DATA


def load_flight(flight: int) -> xr.Dataset:
    """
    Load the flightpath for a given version of ANITA (currently 3/4).

    The returned Dataset has *at least* the following fields:

        realTime:  the time of each entry in unix time.
        altitude:  the payload altitude in m.
        latitude:  the payload latitude in degrees.
        longitude: the payload longitude in degrees.
        heading:   the payload heading in degrees.

    For ANITA3 and ANITA4, it also contains

        pitch: the payload pitch in degrees.
        roll:  the payload roll in degrees.

    Parameters
    ----------
    flight: int
        The flight number to load.

    Returns
    -------
    flightpath: xr.Dataset
        An xarray Dataset indexed by realTime.
    """

    # check for a valid version
    if flight not in [3, 4]:
        raise ValueError(f"We currently only support ANITA3 and ANITA4 (got: {flight})")

    # construct the filename for this flight
    filename = path.join(LOCAL_DATA, *("flightpaths", f"anita{flight}.root"))

    # open the ROOT file
    f = uproot.open(filename)

    # extract the arrays from the adu5PatTree
    data = f["adu5PatTree"].arrays(namedecode="utf-8")

    # create the xaray dataset indexed by realTime
    dataset = xr.Dataset({"realTime": data.pop("realTime")})

    # assign the rest of the TBranch's to the dataset
    dataset = dataset.assign(
        {k: xr.DataArray(v, dims=["realTime"]) for k, v in data.items()}
    )

    # and we are done
    return dataset
