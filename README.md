# anitareader

![License](https://img.shields.io/github/license/rprechelt/anitareader?logoColor=brightgreen)
![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)
[![Code style:black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python reader for ANITA flight data.

`anitareader` provides fast access to ROOT-ified ANITA flight data including calibrated event waveforms.


By default, `anitareader` lazily loads ANITA
flight data into [XArray](http://xarray.pydata.org/en/stable/)
[Datasets](http://xarray.pydata.org/en/stable/data-structures.html#dataset) to allow for multi-dimensional selection, easy analysis, and plotting.

## Installation

To install `anitareader`, you will need `git`, [git-lfs](https://git-lfs.github.com/), and Python >= 3.6. All three should be available in the package manager of any modern OS.
It is tested on macOS 10.14, ubuntu 18.04, ubuntu 16.04, Fedora 29, and Fedora 30.

`anitareader` also requires a working installation of AnitaTools. See the [anitaBuildTool](https://github.com/anitaNeutrino/anitaBuildTool) for 
instructions on how to install AnitaTools. `ANITA_UTIL_INSTALL_DIR` should point to a working AnitaTools or AnitaTools must be installed on your path.

The below instructions are assuming that `python` refers to Python 3.\*. If `python` still refers to a decrepit Python 2.\*, please replace `python` with `python3` and `pip` with `pip3`.

If you wish to install `anitareader` without access to the source (for
development or inspection),  `anitareader` can be directly installed via
`pip`.

    git+git://github.com/rprechelt/anitareader.git#egg=anitareader

If you wish to develop `anitareader`, the recommended method of installation is to first clone the package

    $ git clone https://github.com/rprechelt/anitareader
	
and then change into the cloned directory and install using `pip`

    $ cd anitareader
	$ pip install --user -e .


## Usage

Accessing data from any given flight is done through a `Dataset` instance.

    from anitareader import Dataset
    
    # create a Dataset for ANITA-4
    dataset = Dataset(4)
    
Since ANITA flight data is larger-than-memory (several TB's), the entire dataset
cannot be accessed at once. The `Dataset` object allows for easily iterating
through chunks of the dataset that are *lazily loaded* as they are needed.
Memory used in the previous chunk is immediately discarded upon moving to the
next chunk to minimize memory consumption. 
    
    # we loop over the chunks of events
    for events in dataset:
    
        # `events` is an XArray Dataset containing a "chunk"
        # of events (1000, by default).
        
        # Properties can be accessed as attributes or keys
        events["eventNumber"] == events.eventNumber  # True!
        
        # the properties match the names of the TBranch's stored
        # in the ROOT-ified ANITA data.
        
If you only need to access the dataset *once*, we **strongly recommend**
creating the `Dataset` in the loop expression so that excess memory can be
automatically freed when the loop is finished.

    # loop over the event chunks
    for events in Dataset(4):
        # do stuff with events here!

The list of runs to access is provided as a `runs` argument to the dataset constructor

    # only load run 100
    for events in Dataset(4, runs=[100]):
        pass
        
By default, `anitareader` loads the `headFile`, `timedGpsEventFile`, and
`eventFile` for a given run - this provides access to payload information,
trigger information, and event waveforms. If you only need a specific file 
from the ANITA dataset, or you want to load additional files, they can
be passed to the dataset constructor.

    # only load the headFile and the timedGpsEvent file
    for events in Dataset(4, filetypes=["head", "timedGpsEvent"]):
        pass
        
To control which branches are loaded for each filetype, a dictionary
mapping filetype to a list of branch names can be provided as a `branches` argument
to the dataset constructor.
    
    # only load the `headFile` and the `timedGpsEvent` file
    for events in Dataset(4,
                          filetypes=["head"],
                          branches={"head": ["run", "realTime"]}):
        pass

The default branches loaded for each file type are:

    # check the defaults for each branch
    import anitareader.defaults as defaults
    
    defaults.file_types   # the default files for each flight
    
    defaults.branches  # the default branches for each file type
    
