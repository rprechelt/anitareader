"""
This provides the Dataset class to load and access ANITA data.
"""
import os.path as path
from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    Hashable,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Union,
    cast,
)

import numpy as np
import uproot
import xarray as xr

import anitareader.data as data
import anitareader.defaults as defaults
import anitareader.files as files
import anitareader.trees as trees

__all__ = ["AnitaDataset"]


class AnitaDataset(ABC, Iterable[xr.Dataset]):
    """
    Load and access multiple runs of data from different ANITA flights.
    """

    def __init__(
        self,
        flight: int = 4,
        runs: Optional[List[int]] = None,
        filetypes: Optional[List[str]] = None,
        branches: Optional[Mapping[str, List[str]]] = None,
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
        filetypes: List[str]
            The list of filetypes to load.
        branches: Dict[str, List[str]]
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
        self._filetypes = filetypes if filetypes else defaults.file_types[flight]

        # the list of branches that we are loading
        self._branches = branches if branches else defaults.branches[flight]

        # initialize an empty set of iterators
        self._iterators: Optional[List[Any]] = None

        # a cache to support reading
        self._cache = uproot.cache.ArrayCache(cachesize)

    def __iter__(self) -> Iterator[xr.Dataset]:
        """
        Iterate over chunks of events contained in this dataset.
        """
        # if we are already iterating
        if self._iterators is not None:
            return self
        else:
            return self.iterate()

    def __next__(self) -> xr.Dataset:
        """
        Return the next chunk of events from the dataset as a DataFrame.
        """
        # try and get the next chunk
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

    def iterate(
        self, entrysteps: int = 2000, runs: Optional[List[int]] = None, **kwargs: Any
    ) -> Iterator[xr.Dataset]:
        """
        """

        # check that we have some filetypes
        if len(self._filetypes) == 0:
            raise ValueError(f"No filetypes specified to load.")

        # initialize iterators to an empty list
        # this is where we store the iterators for the various files
        self._iterators = []

        # loop over the requested file types
        for file_type in self._filetypes:

            # create the list of filenames for this filetype
            file_names = self._get_filenames(file_type, runs)

            # the tree name associated with this file
            tree_name = trees.names[file_type]

            # and the branches that we load
            branches = self._branches[file_type]

            # we wrap this to catch if a run cannot be found
            try:

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
            except FileNotFoundError:
                raise FileNotFoundError(f"Unable to load data for runs: {runs}.")

            # and add this iterator to our list
            self._iterators.append(iterator)

        # and return the joined data frames
        return self

    def __create_dataframe(
        self, filetype: str, branch_data: Mapping[Hashable, Any]
    ) -> xr.Dataset:
        """
        """

        # call into the flight-specific routines to parse the data
        # into a dictionary of xr.DataArray's
        arrays = self._create_arrays(filetype, branch_data)

        # and finally create the Dataset from these DataArray
        dataset = xr.Dataset(cast(Mapping[Hashable, Any], arrays))

        # now create the panda's dataframe
        return dataset

    @abstractmethod
    def _create_arrays(
        self, filetype: str, branch_data: Mapping
    ) -> Dict[str, xr.DataArray]:
        """
        """

    def __next_dataframe(self) -> xr.Dataset:
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

        # extract the first file as the primary data frame
        df = self.__create_dataframe(self._filetypes[0], next(self._iterators[0]))

        # if we only have one requested filetype, then we are done
        if len(self._filetypes) == 1:
            return df

        # otherwise we continue to merge in the other ROOT files

        # now loop over the rest of the filetypes
        # for each filetype, we add its columns to the pre-existing xr.Dataset
        # using eventNumber as the merging index
        for filetype, iterator in zip(self._filetypes[1:], self._iterators[1:]):
            df.update(self.__create_dataframe(filetype, next(iterator)))

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

    @property
    def numentries(self) -> Dict[int, int]:
        """
        Calculate the number of events in each run.

        This uses the first-defined filetype, opens the ROOT
        headers, and then calculates the number of entries in the tree.
        The return dictionary takes the run number as keys and has
        the number of entries as values.

        Returns
        -------
        event_count: Dict[int, int]
            The number of entries in each run that we loaded.

        """

        # default, use the head file
        if 'head' in self._filetypes:
            ftype = 'head'
        else:  # otherwise just use the first one
            ftype = self._filetypes[0]

        # the dictionary where we store the results
        N = {}

        # loop over the filenames associated with this filetype
        for run, fname in zip(self._runs, self._get_filenames(ftype)):

            # open the file with uproot
            with uproot.open(fname) as f:

                # load the first tree from the file
                tree = f[f.keys()[0]]

                # and save the number of entries
                N[run] = tree.numentries

        # and return the result
        return N

    def _get_filenames(self, filetype: str, runs: Optional[List[int]] = None) -> List[str]:
        """
        Return the list of run filenames for a given `filetype`.
        """

        # use the given runs, or use the local variable
        run_list = runs if runs else self._runs

        # loop over the run numbers for this data set
        file_names: List[str] = [self._get_filename(i, filetype) for i in run_list]

        return file_names

    def _get_filename(self, run: int, filetype: str) -> str:
        """
        """

        # get the filename type
        fname = files.names[self.flight][filetype]

        # and create the full path
        return path.join(
            f"{self.data_directory}", *(f"run{run}", f"{fname}{run}.root"),
        )

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
            f"    File Types: {self._filetypes}\n"
            f"    Directory: {data.get_directory(self.flight)}\n"
        )

        return msg
