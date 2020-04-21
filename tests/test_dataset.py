"""
Perform tests on the the anitareader.dataset module.
"""
import numpy as np

from anitareader import Dataset


def test_read_basic_data() -> None:
    """
    Check that I can successfully a full file of header info.
    """

    # the number of chunks we have read
    nchunks = 0

    # loop over the dataset
    for events in Dataset(4, filetypes=["timedGpsEvent"]):

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
    for events in Dataset(4, filetypes=["timedGpsEvent", "calibratedWaveform"]):

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

        # make sure that we have unique waveforms for each entry
        assert events["waveforms"][0] is not events["waveforms"][10]

        # check that the waveform dimensions match
        assert events["waveforms"][0].shape == (16, 3, 2, 260)

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


def test_read_chunks() -> None:
    """
    Check that I can I change the size of each chunk
    while reading.
    """

    # loop over the dataset 100 events at a time
    for events in Dataset(4).iterate(entrysteps=100):

        # check that event is a DataFrame
        assert events.eventNumber.shape[0] == 100
        break

    # loop over the dataset 1000 events at a time
    for events in Dataset(4).iterate(entrysteps=1000):

        # check that event is a DataFrame
        assert events.eventNumber.shape[0] == 1000
        break

    # create a dataset
    d = Dataset(4, filetypes=["timedGpsEvent"])

    # loop over the dataset a whole file at a time
    for events in d.iterate(entrysteps=float("inf")):

        # check that event is a DataFrame
        assert events.eventNumber.shape[0] > 200_000
        break


def test_reset_runs() -> None:
    """
    Check that I can I change the size of each chunk
    while reading.
    """

    # get the loaded run
    loaded_run = None
    loaded_events = None

    # create a dataset
    d = Dataset(4, filetypes=["timedGpsEvent"])

    print("BLURGH")

    # loop over the dataset 100 events at a time
    for events in d.iterate(entrysteps=100):

        print("BLAH!")
        # get the current_run
        loaded_run = events.run.data[0]
        print(events)

        # and some events
        loaded_events = events.eventNumber.data
        break

    print(loaded_run)

    # and now explicitly change the run
    d.runs = loaded_run

    # loop again
    for events in d.iterate(entrysteps=100):

        # and check that the run matches
        assert events.run.data[0] == loaded_run

        # and that the event numbers are the same
        assert np.all(np.isclose(events.eventNumber.data, loaded_events))
        break
