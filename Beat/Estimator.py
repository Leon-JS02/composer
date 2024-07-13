import numpy as np

class Estimator:

    """Reduces the likelihood of the estimation being half or double-time tempo"""
    def normalise_bpm(self, bpm):
        if bpm > 160: bpm /= 2
        elif bpm < 60: bpm *= 2
        return round(bpm)
        
    """Naively calculates a BPM estimate, given an array of onset times"""
    def naive_estimate_bpm(self, onset_times):
        # Calculate inter-onset intervals
        IoIs = np.diff(onset_times)
        # Calculate average IoI
        mean_IoI = round(np.mean(IoIs),3)
        # Approximate BPM (assuming every onset = downbeat)
        estimated_bpm = round(60/mean_IoI)
        return self.normalise_bpm(estimated_bpm)
    
    """Calculates a BPM estimate based on the most common inter-onset-interval, given an array of onset times"""
    def interval_based_estimate_bpm(self, onset_times):
        inter_onset_arrivals = np.diff(onset_times)
        inter_onset_arrivals = np.around(inter_onset_arrivals, 3)
        occurrences = dict()
        for ioi in inter_onset_arrivals:
            occurrences[ioi] = occurrences.get(ioi, 0) + 1
        max_key = max(occurrences, key=occurrences.get)
        estimate = 60/max_key
        return self.normalise_bpm(estimate)

    