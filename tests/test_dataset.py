import pandas as pd
from anitareader import Dataset
from anitareader.waveforms import Waveforms


def test_read_basic_data() -> None:
    """
    Check that I can successfully a full file of header info.
    """

    # the number of chunks we have read
    nchunks = 0

    # loop over the dataset
    for events in Dataset(4, file_types=["timedGpsEvent"]):

        # check that event is a DataFrame
        assert isinstance(events, pd.DataFrame)

        # check that it contains some standard columns
        assert events["run"] is not None
        assert events["realTime"] is not None
        assert events["latitude"] is not None

        # and check that each column is the same size
        assert events["run"].size == events["latitude"].size

        # increment the number of chunks
        nchunks += 1

        # if we have read three chunks, we assume that things are working
        if nchunks == 3:
            break


def test_read_waveforms() -> None:
    """
    Check that I can successfully read header and waveform files
    """

    # the number of chunks we have read
    nchunks = 0

    # loop over the dataset
    for events in Dataset(4, file_types=["timedGpsEvent", "calEvent"]):

        # check that event is a DataFrame
        assert isinstance(events, pd.DataFrame)

        # check that it contains some standard columns
        assert events["run"] is not None
        assert events["realTime"] is not None
        assert events["latitude"] is not None

        # make sure I can also access by attributes
        assert events.run is not None
        assert events.realTime is not None
        assert events.latitude is not None

        # and check that each column is the same size
        assert events["run"].size == events["latitude"].size

        # check that we have waveforms stored in the waveform column
        assert isinstance(events["waveforms"][0], Waveforms)

        # make sure that we have unique waveforms for each entry
        assert events["waveforms"][0] is not events["waveforms"][10]

        # check that the waveform dimensions match
        assert events["waveforms"][0].array.shape == (108, 260)

        # and make sure I can convert waveforms to a nice string
        assert isinstance(str(events["waveforms"][10]), str)

        # increment the number of chunks
        nchunks += 1

        # if we have read three chunks, we assume that things are working
        if nchunks == 2:
            break


def test_read_default() -> None:
    """
    Check that I can successfully read header and timedGpsEvent
    info using the default Dataset settings.
    """

    # the number of chunks we have read
    nchunks = 0

    # loop over the dataset
    for events in Dataset(4):

        # check that event is a DataFrame
        assert isinstance(events, pd.DataFrame)

        # check that it contains some standard columns
        assert events["run"] is not None
        assert events["realTime"] is not None
        assert events["latitude"] is not None

        # and contains data from the headFile
        assert events["trigType"] is not None

        # and check that each column is the same size
        assert events["run"].size == events["trigType"].size

        # increment the number of chunks
        nchunks += 1

        # if we have read three chunks, we assume that things are working
        if nchunks == 2:
            break
