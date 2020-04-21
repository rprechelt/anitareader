"""
Test trigger types for ANITA4.
"""
import numpy as np
import anitareader
import anitareader.anita4.trigger as trigger


def test_triggers():
    """
    Check that we a mixture of trigger types.
    """

    # create the dataset
    d = anitareader.Dataset(4, filetypes=["head"])

    # loop over the events
    for events in d.iterate(entrysteps=np.float("inf")):

        # check that there are some RF triggers
        assert trigger.is_RF(events.trigType).sum() > 0

        # and some min-bias triggers
        assert trigger.is_minbias(events.trigType).sum() > 0

        # check for individual G12 and ADU5 eventstriggers
        assert trigger.is_ADU5(events.trigType).sum() > 0
        assert trigger.is_G12(events.trigType).sum() > 0

        # and check for soft triggers
        assert trigger.is_soft(events.trigType).sum() > 0

        # and we only check this once
        break
