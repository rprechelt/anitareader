"""
"""
import numpy as np

__all__ = ["Waveforms"]


class Waveforms:
    """
    An object-wrapper around ANITA waveforms.

    This allows for storage inside the cells of a Pandas dataframe
    and also provides some utility functions for accessing data.
    """

    def __init__(self, wvfms: np.ndarray):
        """
        Create an object-wrapper around an array of waveforms.
        """
        self.array = wvfms

    def __str__(self) -> str:
        """
        Return a string representation.
        """

        # get the number of channels
        nchan = self.array.shape[0]
        wlength = self.array.shape[1]

        # and insert them into a nice Waveform string
        return f"Waveforms(nchan={nchan}, length={wlength})"
