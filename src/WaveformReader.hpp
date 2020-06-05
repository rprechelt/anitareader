#pragma once

#include "AnitaDataset.h"
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace anitareader {

  namespace py = pybind11;

/**
 * Read Waveforms from eventFile's into NumPy arrays.
 */
class WaveformReader {

  // using NumpyArray = py::array_t<float, py::array::c_style | py::array::forcecast>;
  using NumpyArray = py::array_t<float>;

  /*
   * The current run we have loaded.
   */
  unsigned int run_;

  /*
   * An instance of an AnitaDataset reader.
   */
  AnitaDataset dataset_;

public:
  /*
   * Create a new WaveformReader for the given run.
   */
  WaveformReader(const int run)
      : run_(run),
        dataset_(run, false, WaveCalType::kDefault,
                 AnitaDataset::ANITA_ROOT_DATA, AnitaDataset::kNoBlinding){};

  /*
    * A virtual destructor.
    */
  virtual
  ~WaveformReader() {};

  /*
   * Return the next N waveforms from the dataset.
   *
   * @param N    The number of events to load
   * @param waveforms    The NumPy array to store the events into.
   */
  auto
  next(NumpyArray& waveforms) -> int;


}; // END: class WaveformReader

} // namespace anitareader
