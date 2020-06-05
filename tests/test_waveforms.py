"""
Test that I can directly load waveforms using
a WaveformReader instance.
"""
import numpy as np

from anitareader.data import available_runs
from anitareader.waveforms import WaveformReader

# get the run number that we use for all tests
try:
    run = available_runs(4)[0]
except _ as _:
    raise RuntimeError(f"No ANITA runs available for testing.")

# the flight numbers that we test
flights = [4]


def test_create_waveform_reader() -> None:
    """
    Check that I can create a Waveforms() instance.
    """
    # loop over the flights
    for flight in flights:
        WaveformReader(run, flight=flight)


def test_access_waveforms() -> None:
    """
    Check that I can get a chunk of data from a WaveformReader
    """

    # loop over the flights
    for flight in flights:

        # create the reader
        reader = WaveformReader(run, flight=flight)

        # we ask for a small number of events
        N = 10

        # the number of chunks that we read
        Nchunks = 9

        # store the event numbers for all events
        events = np.zeros(N * Nchunks)

        # we read multiple chunks
        for i in np.arange(Nchunks):

            # ask for 10 events
            waveforms = reader.next(N)

            # make sure we got the right number of events
            assert waveforms.shape[0] == N

            # make sure every waveform is non-zero
            assert np.all(np.sum(np.abs(waveforms.values), axis=(1, 2, 3, 4)) > 0)

            # store the eventNumbers's
            events[i * N : (i + 1) * N] = waveforms.eventNumber

        # and check that we got continuous event numbers
        assert np.all(np.diff(events) == 1)
