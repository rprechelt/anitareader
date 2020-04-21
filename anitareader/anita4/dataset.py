"""
A package providing the ANITA4Dataset class.
"""
import re
from typing import Any, Dict, List, Mapping, Tuple

import numpy as np
import xarray as xr
from cachetools import cached

from anitareader.dataset import AnitaDataset


class Anita4Dataset(AnitaDataset):
    """
    Load and access ROOTified ANITA-4 data.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """
        Create an ANITA4Dataset instance.

        See documentation for Dataset.
        """
        super().__init__(*args, **kwargs)

    @cached(cache={})
    @staticmethod
    def channels() -> List[str]:
        """
        Return the channel ordering for ANITA4.

        Returns
        -------
        channels: List[str]
            Return the in-order list of channels
            for calibratedWaveformFile's for ANITA4.
        """

        # the channels list
        channel_ids = []

        # loop over the phi sectors
        for phi in range(1, 17):

            # and loop over the ring
            for ring in ["T", "M", "B"]:

                # and then the polarization
                for pol in ["H", "V"]:

                    # and add this channel to our list
                    channel_ids.append(f"{phi:02}{ring}{pol}")

        # and return the channels list
        return channel_ids

    def _create_arrays(
        self, filetype: str, branch_data: Mapping
    ) -> Dict[str, xr.DataArray]:
        """
        """

        # the dictionary where we store the created DataArray's
        arrays: Dict[str, xr.DataArray] = {}

        # we loop over the keys and valuse of this dictionary
        # and dispatch to the appropriate methods
        for key, val in branch_data.items():

            # check if this is an ANITA4 calibrated waveform
            if re.search(r"^[a-zA-z]*\[16\]\[3\]\[2\]\[260\]$", key):
                self._convert_calibrated_waveforms(key, branch_data, arrays)
            # check if this is a channel scalar quantity
            elif re.search(r"^[a-zA-z]*\[16\]\[3\]\[2\]\[260\]$", key):
                self._convert_calibrated_scalar(key, branch_data, arrays)
            else:
                self._convert_scalar(key, branch_data, arrays)

        # and return the newly created DataArray's
        return arrays

    def _convert_calibrated_waveforms(
        self, key: str, branch_data: Mapping, arrays: Dict[str, xr.DataArray]
    ) -> None:
        """
        """

        # extract the event number from the dictionary
        eventNumber = branch_data["eventNumber"]

        # and get the phi sectors, rings, and pols
        phis, rings, pols = self._phi_ring_pol()

        # and create the standard time offset assuming 2.6 GSa/s
        times = np.arange(260) / 2.6  # in ns

        # create the DataArray
        xarr = xr.DataArray(
            branch_data[key],
            coords={
                "eventNumber": eventNumber,
                "phi": phis,
                "ring": rings,
                "pol": pols,
                "time": times,
            },
            dims=["eventNumber", "phi", "ring", "pol", "time"],
        )

        # and add this to the arrays dictionary in-place
        arrays["waveforms"] = xarr

    def _convert_calibrated_scalar(
        self, key: str, branch_data: Mapping, arrays: Dict[str, xr.DataArray]
    ) -> None:
        """
        """

        # extract the event number from the dictionary
        eventNumber = branch_data["eventNumber"]

        # and get the phi sectors, rings, and pols
        phis, rings, pols = self._phi_ring_pol()

        # create the DataArray
        xarr = xr.DataArray(
            branch_data[key],
            coords={
                "eventNumber": eventNumber,
                "phi": phis,
                "ring": rings,
                "pol": pols,
            },
            dims=["eventNumber", "phi", "ring", "pol"],
        )

        # extract the branch name sans square brackets
        name = key[0 : key.index("[")]  # noqa

        # and add this to the arrays dictionary in-place
        arrays[name] = xarr

    def _convert_scalar(
        self, key: str, branch_data: Mapping, arrays: Dict[str, xr.DataArray]
    ) -> None:
        """
        """

        # extract the event number from the dictionary
        eventNumber = branch_data["eventNumber"]

        # create the DataArray
        xarr = xr.DataArray(
            branch_data[key], coords={"eventNumber": eventNumber}, dims=["eventNumber"],
        )

        # and add this to the arrays dictionary in-place
        arrays[key] = xarr

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
