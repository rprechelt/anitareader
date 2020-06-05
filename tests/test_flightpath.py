"""
Test anitareader/flightpath.py
"""
import pytest

import anitareader.flightpath as flightpath


def test_anita3():
    """
    Check that we load the ANITA3 flight.
    """

    # load the data
    flight = flightpath.load_flight(3)

    # and check that we can access some key variables
    flight.realTime
    flight.latitude
    flight.longitude
    flight.pitch
    flight.roll

    # check that dictionary style access works too
    flight["realTime"]
    flight["latitude"]

    # and check that we some reasonable number of events
    assert flight.realTime.data.shape[0] > 30_000


def test_anita4():
    """
    Check that we load the ANITA4 flight.
    """

    # load the data
    flight = flightpath.load_flight(4)

    # and check that we can access some key variables
    flight.realTime
    flight.latitude
    flight.longitude
    flight.pitch
    flight.roll

    # check that dictionary style access works too
    flight["realTime"]
    flight["latitude"]

    # and check that we some reasonable number of events
    assert flight.realTime.data.shape[0] > 30_000


def test_bad_flight():
    """
    Check that a bad flight number raises an exception.
    """
    with pytest.raises(ValueError):
        flightpath.load_flight(0)
