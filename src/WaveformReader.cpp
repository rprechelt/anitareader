#include "WaveformReader.hpp"
#include <stdexcept>

#include "RawAnitaHeader.h"
#include "AnalysisWaveform.h"
#include "UsefulAnitaEvent.h"

namespace py = pybind11;
using namespace anitareader;

auto WaveformReader::next(NumpyArray &waveforms) -> int {

  // this function assumes that the caller has checked that
  // there are still waveforms remaining in the file.
  // This function will gladly read past the end of the
  // run if asked for (although I do some basic checking
  // to ensure that that shouldn't happen).

  // while I'm normally all for safety, this function is
  // only going to be called in low-level code from the
  // anitareader library so we should optimize for
  // performance. Therefore, we use an array accessor
  // that doesn't have any bounds checking
  auto r = waveforms.mutable_unchecked<5>();

  // we record the event ID so we can return the
  // last event ID to anitareader.py to perform
  // some sane error checking.
  int evno = 0;

  // loop over the number of requested events
  for (ssize_t event = 0; event < r.shape(0); ++event) {

    // extract the event number
    evno = dataset_.header()->eventNumber;

    // get the useful anita event - here is where the calibration is performed.
    auto useful{dataset_.useful()};

    // these loops do NO ERROR CHECKING. If the array
    // that you pass in does not have the right number of
    // rings and polarizations, then you will get garbage.

    // now we loop over every phi, ring, pol
    for (ssize_t phi = 0; phi < r.shape(1); phi++) {

      // and loop over the rings
      for (auto &ring : {AnitaRing::kTopRing, AnitaRing::kMiddleRing,
                         AnitaRing::kBottomRing}) {

        // and loop over the polarizations - hpol then vpol
        for (auto &pol : {AnitaPol::kHorizontal, AnitaPol::kVertical}) {

          // get the graph for this channel
          auto gr{useful->getGraph(ring, phi, pol)};

          // and convert this into an AnalysisWaveform
          auto *waveform{AnalysisWaveform::makeWf(gr, false)};

          // get the number of samples in this waveform
          // r.shape(4) should always be at least 260
          const int N{std::min(waveform->even()->GetN(), int(r.shape(4)))};

          // get a reference to the evenly sampled waveform
          auto *signal{waveform->even()->GetY()};

          // now loop over the samples filling in the data
          for (ssize_t sample = 0; sample < N; sample++) {
            r(event, phi, ring, pol, sample) = signal[sample];
          } // END: sample loop

          // and free up some memory
          delete waveform;
          delete gr;

        } // END: pol loop
      }   // END: ring loop
    }     // END: phi loop


    // load the next event
    dataset_.next();

    // if we have changed runs for some reason, return
    // although this behaviour might change in the future
    // so don't rely on it.
    if (dataset_.getCurrRun() != this->run_) {

      // update to the new run
      this->run_ = dataset_.getCurrRun();

      // and return the last event number that we loaded.
      return evno;
      
    } // END: if (dataset_.getCurrRun() != this->run_) {

  } // END: loop over events


  // and return the last event number that we read
  return evno;
    
} // END: next()
