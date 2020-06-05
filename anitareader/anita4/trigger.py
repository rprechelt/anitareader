"""
Provides methods to check for A4 trigger types.
"""

import xarray as xr


def is_RF(trigtype: xr.DataArray) -> xr.DataArray:
    """
    Check for an RF trigger.

    Parameters
    ----------
    trigtype: xr.DataArray
        An array of trigger types.

    Returns
    -------
    RF: xr.DataArray[bool]
        A Boolean array - True if RF trigger.

    """
    # check for RF triggers
    rf: xr.DataArray = trigtype & (1 << 0)

    return rf.astype(bool)


def is_minbias(trigtype: xr.DataArray) -> xr.DataArray:
    """
    Check for a minimum bias trigger.

    For ANITA4, this is a either a ADU5, G12, or soft trigger.

    Parameters
    ----------
    trigtype: xr.DataArray
        An array of trigger types.

    Returns
    -------
    minbias: xr.DataArray[bool]
        A Boolean array - True if min bias trigger
    """
    # check for a minbias trigger
    minbias: xr.DataArray = is_ADU5(trigtype) | is_G12(trigtype) | is_soft(trigtype)

    return minbias


def is_ADU5(trigtype: xr.DataArray) -> xr.DataArray:
    """
    Check for an ADU5 trigger.

    Parameters
    ----------
    trigtype: xr.DataArray
        An array of trigger types.

    Returns
    -------
    ADU5: xr.DataArray[bool]
        A Boolean array - True if ADU5 trigger.

    """
    # check for an ADU5 trigger
    adu5: xr.DataArray = trigtype & (1 << 1)

    return adu5.astype(bool)


def is_G12(trigtype: xr.DataArray) -> xr.DataArray:
    """
    Check for an G12 trigger.

    Parameters
    ----------
    trigtype: xr.DataArray
        An array of trigger types.

    Returns
    -------
    G12: xr.DataArray[bool]
        A Boolean array - True if G12 trigger.

    """
    # check for a G12 trigger
    G12: xr.DataArray = trigtype & (1 << 2)

    return G12.astype(bool)


def is_soft(trigtype: xr.DataArray) -> xr.DataArray:
    """
    Check for an soft trigger.

    Parameters
    ----------
    trigtype: xr.DataArray
        An array of trigger types.

    Returns
    -------
    soft: xr.DataArray[bool]
        A Boolean array - True if soft trigger.

    """
    # check for a soft trigger
    soft: xr.DataArray = trigtype & (1 << 3)

    return soft.astype(bool)
