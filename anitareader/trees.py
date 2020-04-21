"""
"""

__all__ = ["names"]

# the keys to this dict are the filetypes and
# the keys are the trees contained in each file
names = {
    "avgSurfHk": "avgSurfHkTree",
    "calEvent": "eventTree",
    "calibratedWaveform": "events",
    "calibratedEventInfo": "calInfoTree",
    "event": "eventTree",
    "gpsEvent": "adu5PatTree",
    "gpu": "gpuTree",
    "head": "headTree",
    "hk": "hkTree",
    "monitor": "monitorTree",
    "prettyHk": "prettyHkTree",
    "rawScaler": "rawScalerTree",
    "rtlSpectrum": "rtlTree",
    "sshk": "hkTree",
    "sumTurfRate": "sumTurfRateTree",
    "surfHk": "surfHkTree",
    "timedGpsEvent": "adu5PatTree",
    "timedHead": "headTree",
    "ttt": "tttTree",
    "tuffStatus": "tuffTree",
    "turfRate": "turfRateTree",
}
