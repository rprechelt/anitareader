"""
Provide tests of the anitareader.data module.
"""
import pytest
import anitareader.data as data


def test_get_directory() -> None:
    """
    Check that get_directory works.
    """

    # check that the data for invalid flights does not work
    for i in [0, -1, 5]:
        with pytest.raises(ValueError):
            assert data.get_directory(i)

    # check that a string is returned for all valid flights
    for i in [1, 2, 3, 4]:
        assert isinstance(data.get_directory(i), str)


def test_is_available() -> None:
    """
    Check that is_available works.
    """

    # check that the data for invalid flights does not work
    for i in [0, -1, 5]:
        with pytest.raises(ValueError):
            assert data.is_available(i)

    # check that a string is returned for all valid flights
    for i in [1, 2, 3, 4]:
        assert isinstance(data.is_available(i), bool)


def test_available_runs() -> None:
    """
    Check that available_runs works. This assumes that there
    is atleast one run of ANITA-4 data available in the test environment.
    """

    # check that the data for invalid flights does not work
    for i in [0, -1, 5]:
        with pytest.raises(ValueError):
            assert data.available_runs(i)

    # check that a string is returned for all valid flights
    for i in [1, 2, 3, 4]:
        assert isinstance(data.available_runs(i), list)

    # and that the string is not empty for ANITA-4
    assert len(data.available_runs(4)) != 0


def test_direct_access() -> None:
    """
    Check that we can directly access the location of ANITA data
    """

    # just accessing a non-existent will cause the tests to fail
    data.ANITA1_DATA
    data.ANITA2_DATA
    data.ANITA3_DATA
    data.ANITA4_DATA
    data.LOCAL_DATA
