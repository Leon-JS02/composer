"""Module and class to estimate the tempo of an audio file."""

import numpy as np


class Estimator:
    """Estimator class - performs onset detection and BPM estimation of an audio file."""

    def normalise_bpm(self, bpm: float) -> int:
        """Reduces the likelihood of the estimation being half or double-time tempo"""
        if bpm > 160:
            bpm /= 2
        elif bpm < 60:
            bpm *= 2
        return round(bpm)

    def naive_estimate_bpm(self, onset_times: list[float]) -> int:
        """Naively calculates a BPM estimate, given an array of onset times"""
        inter_onset_intervals = np.diff(onset_times)
        mean_interval = round(np.mean(inter_onset_intervals), 3)
        estimated_bpm = round(60/mean_interval)
        return self.normalise_bpm(estimated_bpm)

    def interval_based_estimate_bpm(self, onset_times: list[float]) -> int:
        """Calculates a BPM estimate based on the most common inter-onset-interval, 
        given an array of onset times"""
        inter_onset_arrivals = np.diff(onset_times)
        inter_onset_arrivals = np.around(inter_onset_arrivals, 3)
        occurrences = {}
        for ioi in inter_onset_arrivals:
            occurrences[ioi] = occurrences.get(ioi, 0) + 1
        max_key = max(occurrences, key=occurrences.get)
        estimate = 60/max_key
        return self.normalise_bpm(estimate)
