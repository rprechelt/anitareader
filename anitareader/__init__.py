"""
A pure Python reader for ANITA ROOT data.
"""
from typing import Any

from .anita4 import Anita4Dataset
from .dataset import AnitaDataset

__version__ = "0.0.1"


def Dataset(flight: int, *args: Any, **kwargs: Any) -> AnitaDataset:
    """
    Construct a Dataset for a given flight.
    """
    if flight == 4:
        return Anita4Dataset(flight, *args, **kwargs)
    else:
        raise ValueError(f"anitareader currently only supports ANITA4.")
