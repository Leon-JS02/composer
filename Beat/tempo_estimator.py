"""Module for tempo estimation. Combines classes from onset_detector
and estimator."""

import librosa

from Beat.onset_detector import OnsetDetector
from Beat.estimator import Estimator


class TempoEstimator:
    """TempoEstimator class. Performs the two stages of
    onset detection and estimation."""

    def __init__(self):
        self.onset_detector = OnsetDetector()
        self.estimator = Estimator()

    def predict_bpm(self, file_path: str) -> tuple[int, list[float]]:
        """Predicts BPM in two stages: Onset detection, and estimation"""
        y, sr = librosa.load(file_path)
        onsets, time = self.onset_detector.detect_spectral_onsets(
            y, sr, gamma=100)
        onset_times = time[onsets]
        bpm = self.estimator.interval_based_estimate_bpm(onset_times)
        self.onset_detector.produce_click_track(onset_times)
        return bpm, onset_times
