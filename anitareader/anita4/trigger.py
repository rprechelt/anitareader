import numpy as np


def is_RF(trigtype: np.ndarray) -> np.ndarray:
    """
    Check for an RF trigger.

    Parameters
    ----------
    trigtype: np.ndarray
        An array of trigger types.

    Returns
    -------
    RF: np.ndarray[bool]
        A Boolean array - True if RF trigger.

    """
    # check for RF triggers
    rf: np.ndarray = np.asarray(trigtype & (1 << 0), dtype=bool)

    return rf


def is_minbias(trigtype: np.ndarray) -> np.ndarray:
    """
    Check for a minimum bias trigger.

    For ANITA4, this is a either a ADU5 or a G12 trigger.

    Parameters
    ----------
    trigtype: np.ndarray
        An array of trigger types.

    Returns
    -------
    minbias: np.ndarray[bool]
        A Boolean array - True if min bias trigger
    """
    # check for a minbias trigger
    minbias: np.ndarray = np.logical_or(is_ADU5(trigtype), is_G12(trigtype))

    return minbias


def is_ADU5(trigtype: np.ndarray) -> np.ndarray:
    """
    Check for an ADU5 trigger.

    Parameters
    ----------
    trigtype: np.ndarray
        An array of trigger types.

    Returns
    -------
    ADU5: np.ndarray[bool]
        A Boolean array - True if ADU5 trigger.

    """
    # check for an ADU5 trigger
    adu5: np.ndarray = np.asarray(trigtype & (1 << 1), dtype=bool)

    return adu5


def is_G12(trigtype: np.ndarray) -> np.ndarray:
    """
    Check for an G12 trigger.

    Parameters
    ----------
    trigtype: np.ndarray
        An array of trigger types.

    Returns
    -------
    G12: np.ndarray[bool]
        A Boolean array - True if G12 trigger.

    """
    # check for a G12 trigger
    G12: np.ndarray = np.asarray(trigtype & (1 << 2), dtype=bool)

    return G12


def is_soft(trigtype: np.ndarray) -> np.ndarray:
    """
    Check for an soft trigger.

    Parameters
    ----------
    trigtype: np.ndarray
        An array of trigger types.

    Returns
    -------
    soft: np.ndarray[bool]
        A Boolean array - True if soft trigger.

    """
    # check for a soft trigger
    soft: np.ndarray = np.asarray(trigtype & (1 << 3), dtype=bool)

    return soft
