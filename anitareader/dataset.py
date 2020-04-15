"""
This provides the Dataset class to load and access ANITA data.
"""
import os.path as path
from typing import List, Optional, Any, Dict, Union
import uproot
import numpy as np
import pandas as pd
import anitareader.data as data
import anitareader.trees as trees
import anitareader.files as files
import anitareader.defaults as defaults
from anitareader.waveforms import Waveforms

__all__ = ["Dataset"]


class Dataset:
    """
    Load and access multiple runs of data from different ANITA flights.
    """

    def __init__(
        self,
        flight: int = 4,
        runs: Optional[List[int]] = None,
        file_types: Optional[List[str]] = None,
        branches: Dict[int, List[str]] = None,
        cachesize: str = "1GB",
    ):
        """
        Load runs from a given flight.

        Parameters
        ----------
        flight: int
            The flight number to load.
        runs: List[int]
            The list of runs to load.
        file_types: List[str]
            The list of filetypes to load.
        branches: Dict[int, List[str]]
            The branches to load for each filetype.
        cachesize: str
            The cachesize to use for reading.

        Returns
        -------
        events: ChunkedArray
            A lazily-loaded array view into the ANITA dataset.

        Raises
        ------
        ValueError
            If the dataset for the requested flight is not available.

        """

        # save the requested flight
        self.flight = flight

        # and the data directory for this flight
        self.data_directory = data.get_directory(self.flight)

        # set the requested runs or get defaults
        self._runs = runs if runs else data.available_runs(flight)

        # save the requested filesn
        self._file_types = file_types if file_types else defaults.file_types[flight]

        # the list of branches that we are loading
        self._branches = branches if branches else defaults.branches[flight]

        # initialize an empty set of iterators
        self._iterators: Optional[List[Any]] = None

        # a cache to support reading
        self._cache = uproot.cache.ArrayCache(cachesize)

    def __iter__(self):
        """
        Iterate over chunks of events contained in this dataset.
        """
        # if we are already iterating
        if self._iterators is not None:
            return self
        else:
            return self.iterate()

    def __next__(self) -> pd.DataFrame:
        """
        Return the next chunk of events from the dataset as a DataFrame.
        """
        # try and get the next chunkd
        try:
            next_chunk = self.__next_dataframe()

            # return the next chunk
            return next_chunk

        # if we have finished iterating
        except StopIteration as stop:
            # reset our iterators
            self._iterators = None

            # and re-raise the exception so that the loop stops
            raise stop

    def iterate(self, entrysteps: int = 1000, **kwargs: Any) -> pd.DataFrame:
        """
        """
        # initialize iterators to an empty list
        # this is where we store the iterators for the various files
        self._iterators = []

        # loop over the requested file types
        for file_type in self._file_types:

            # get the name of this file_type
            name = files.names[self.flight][file_type]

            # create the list of filenames for this filetype
            file_names = [
                path.join(f"{self.data_directory}", *(f"run{i}", f"{name}{i}.root"),)
                for i in self._runs
            ]

            # the tree name associated with this file
            tree_name = trees.names[file_type] + "Tree"

            # and the branches that we load
            branches = self._branches[file_type]

            print(f"entrysteps: {entrysteps}")

            # create the iterator for this filetype
            iterator = uproot.iterate(
                file_names,
                tree_name,
                branches=branches,
                namedecode="utf-8",
                entrysteps=entrysteps,
                basketcache=self._cache,
                **kwargs,
            )

            # and add this iterator to our list
            self._iterators.append(iterator)

        # and return the joined data frames
        return self

    @staticmethod
    def __create_dataframe(branch_data: Dict[str, Any]) -> pd.DataFrame:
        """
        """

        # loop over all of the keys contained in this tree
        for key in branch_data.keys():

            # check if we have found waveform data
            if key == "data[108][260]":

                # we have! extract a reference to the data
                wvfm_data = branch_data[key]

                # Now wrap the entries in Waveform structs
                wvfms = [
                    Waveforms(wvfm_data[i, ...]) for i in np.arange(wvfm_data.shape[0])
                ]

                # add those waveforms to our branch struct
                branch_data["waveforms"] = wvfms

                # and delete the old branch data
                del branch_data[key]

                # and we are done since there's only one waveform array per file
                break

        # now create the panda's dataframe
        return pd.DataFrame(branch_data)

    def __next_dataframe(self) -> pd.DataFrame:
        """
        """

        # check that this is being called after __iter__()
        if self._iterators is None:
            raise RuntimeError(
                (
                    "__next__() was called before __init__(). "
                    "Dataset's must be iterated through."
                )
            )

        # return next(self.iterators[0]), next(self.iterators[1])
        # extract the first file as the primary data frame
        df = self.__create_dataframe(next(self._iterators[0]))

        # now loop over and join the rest of the data frames
        # using eventNumber as a key
        for iterator in self._iterators[1:]:
            df = df.merge(
                self.__create_dataframe(next(iterator)),
                on="eventNumber",
                copy=False,
                suffixes=("", "_dup"),
            )

        # we now have some duplicated columns, so let's drop those (inplace!)
        df.drop(list(df.filter(regex="_dup$")), axis=1, inplace=True)

        # and we are done
        return df

    @property
    def runs(self) -> List[int]:
        """
        Return the list of runs currently loaded by this dataset.
        """
        return self._runs

    @runs.setter
    def runs(self, runs: Union[int, List[int]]) -> None:
        """
        Change the runs contained in this dataset.
        """

        # provide some basic type-conversions here
        if isinstance(runs, list):
            self._runs = runs
        elif isinstance(runs, np.ndarray):
            self._runs = runs
        else:
            # otherwise make it a list
            self._runs = [runs]

        # and reset the iterators as we have to start again
        self._iterators = None

    def __repr__(self) -> str:
        """
        The string representation of this Dataset.

        Parameters
        ----------
        None

        Returns
        -------
        repr: str
        A human-readable string representation of this Dataset.
            """

        msg = (
            f"Dataset:\n"
            f"    Flight: {self.flight}\n"
            f"    No. Runs: {len(self._runs)}\n"
            f"    File Types: {self._file_types}\n"
            f"    Directory: {data.get_directory(self.flight)}\n"
        )

        return msg
