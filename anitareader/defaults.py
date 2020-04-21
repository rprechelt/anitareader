"""
This module provides the default branches and
filenames associated with each ANITA dataset.
"""

__all__ = ["file_types", "branches"]

# the default files loaded for each flight
file_types = {4: ["head", "timedGpsEvent", "calibratedWaveform"]}

# the default branches for each flight and filetype
branches = {
    4: {
        "calibratedWaveform": ["run", "eventNumber", "data[16][3][2][260]"],
        "calEvent": ["run", "eventNumber", "data[108][260]", "mean[108]", "rms[108]"],
        "head": ["run", "eventNumber", "realTime", "trigType"],
        "timedGpsEvent": [
            "run",
            "eventNumber",
            "realTime",
            "payloadTime",
            "payloadTimeUs",
            "timeOfDay",
            "latitude",
            "longitude",
            "altitude",
            "heading",
            "pitch",
            "roll",
        ],
    }
}
