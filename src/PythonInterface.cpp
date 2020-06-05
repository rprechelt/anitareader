#include <pybind11/pybind11.h>
#include "WaveformReader.hpp"

namespace py = pybind11;
using namespace anitareader;

// create our Python module
PYBIND11_MODULE(_anitareader, m) {

  // add a docstring
  m.doc() = "Directly read ANITA event files into NumPy arrays";

  // create a wrapper for the WaveformReader
  py::class_<WaveformReader>(m, "WaveformReader")
    .def(py::init<const int>())
    .def("next", &WaveformReader::next, py::arg().noconvert(),
         "Return the next N wavforms from the current run.");

}
