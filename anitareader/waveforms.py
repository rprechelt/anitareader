import os.path as op
from typing import List, Tuple

import numpy as np
import uproot
import xarray as xr

import _anitareader
import anitareader.data as data

__all__ = ["WaveformReader"]


class WaveformReader:
    """
    Load waveforms from ANITA event files using a WaveformReader.
    """

    def __init__(self, run: int, flight: int = 4):
        """
        Create an object to access ANITA waveforms.

        Parameters
        -----------
        run: int
             The run to load waveforms from.
        """

        # set the flight that we load
        self.flight = flight

        # setup for the next run.
        self.__new_run(run)

    def next(self, N: int) -> xr.DataArray:
        """
        Load the next `N` waveforms into a XArray Dataset.

        Parameters
        ----------
        N: int
            The maximum number of events to load.

        Returns
        -------
        waveforms: xr.DataArray
            An xarray DataArray containing calibrated waveforms.
        """

        # and get the phi sectors, rings, and pols for this payload
        phis, rings, pols = self._phi_ring_pol()

        # and get the length of the waveforms loaded for this flight
        wvfm_size = self.waveform_length

        # allocate memory to store the waveforms
        # this *MUST* be in float32 or you will pull your hair out.
        # and Satan himself will conspire to make you crazy.
        waveforms = np.zeros(
            (N, len(phis), len(rings), len(pols), wvfm_size), dtype=np.float32
        )

        # read the next events from the waveform reader
        # this fills in `waveforms` with calibrate data
        # and returns the last event number that was loaded.
        last_event = self.reader.next(waveforms)

        # check that the returned event number is in the next
        # batch of requested event numbers.
        if last_event not in self.event_numbers[self.evidx : self.evidx + N]:
            raise RuntimeError(f"The WaveformReader is out of sync. Fatal error...")

        # find the index of the last_event number
        last_index = np.nonzero(
            self.event_numbers[self.evidx : self.evidx + N] == last_event
        )[0]

        # if we didn't find the number of events, that is the error
        if last_index.size == 0:
            raise RuntimeError(f"Unable to find latest event number in event list.")

        # this is  the number of loaded events
        Nloaded = last_index[0] + 1

        # discard any memory that wasn't written to
        waveforms = waveforms[0:Nloaded, ...]

        # create the time array
        # TODO: Get from the reader so that we can support other payloads
        times = np.arange(waveforms.shape[-1]) / self.samplerate  # in ns

        # create the DataArray
        xarr = xr.DataArray(
            waveforms,
            coords={
                "eventNumber": self.event_numbers[self.evidx : self.evidx + Nloaded],
                "phi": phis,
                "ring": rings,
                "pol": pols,
                "time": times,
            },
            dims=["eventNumber", "phi", "ring", "pol", "time"],
        )

        # add some units
        xarr.attrs["units"] = "mV"
        xarr.time.attrs["units"] = "ns"

        # and increment the event index
        self.evidx += Nloaded

        # TODO: check if we are at the next run.

        # and return the calibrated waveform
        return xarr

    def __new_run(self, run: int) -> None:

        # save the current run
        self._run = run

        # and load the events for this run
        self.event_numbers = self.__load_events()

        # create a WaveformReader instance for this run.
        # this is a C++ class that interfaces with ANITA Tools
        self.reader = _anitareader.WaveformReader(run)

        # reset our counters
        self.evidx = 0

    def __load_events(self) -> np.ndarray:
        """
        Load the full list of eventNumbers for the specified run.

        Parameters
        ----------

        Returns
        -------
        events: np.ndarray
            A NumPy array containing event numbers.
        """

        # get the filename that we are going to load
        filename = self.__get_filename()

        # open the file with uproot
        with uproot.open(filename) as f:

            # access the events tree
            tree = f[b"eventTree"]

            # and load the eventNumbers into an array
            events = tree.array(b"eventNumber")

        # and we are done
        return events

    def __get_filename(self) -> str:
        """
        Return the filename for events in the specified run.

        We prefer calEventFile's but will fall back to
        regular eventFile's as needed.

        Parameters
        ----------

        Returns
        -------
        filename: str
            The full path to the file to load.
        """

        # the directory where we store data for this flight
        data_directory = data.get_directory(self.flight)

        # loop over the filetype - try for calEventFile first
        for ftype in ["calEventFile", "eventFile"]:

            # create the filename
            fname = op.join(
                f"{data_directory}", *(f"run{self._run}", f"{ftype}{self._run}.root")
            )

            # if it exists
            if op.exists(fname):
                return fname  # yay! we found a file

        # if we got here, we don't have any event files
        raise FileNotFoundError(f"Unable to find an event file for run {self._run}")

    @property
    def run(self) -> int:
        """
        Return the currently loaded run.
        """
        return self._run

    @run.setter
    def run(self, run: int) -> None:
        """
        Change the run that we load from.

        Parameters
        ----------
        run: int
            The new run that we load from.
        """

        # and reinitialize the reader to the new run
        self.__new_run(run)

    @property
    def samplerate(self) -> float:
        """
        Get the sample rate of this flight in GSa/s.

        Parameters
        ----------

        Returns
        -------
        The sample rate in GSa/s.
        """
        if self.flight == 4:
            return 2.6
        else:
            raise ValueError(f"Unknown sample rate for flight: {self.flight}")

    @property
    def waveform_length(self) -> float:
        """
        Get the length of waveforms for this flight.

        Parameters
        ----------

        Returns
        -------
        The length of loaded waveforms for this flight.
        """
        if self.flight == 4:
            return 260
        else:
            raise ValueError(f"Unknown waveform length for flight: {self.flight}")

    @staticmethod
    def _phi_ring_pol() -> Tuple[np.ndarray, List[str], List[str]]:
        """
        """
        # get the phi sectors
        phis = np.arange(1, 17)

        # the rings
        rings = ["T", "M", "B"]

        # and the pols
        pols = ["H", "V"]

        return phis, rings, pols
