import librosa

from Beat.OnsetDetector import OnsetDetector
from Beat.Estimator import Estimator

class TempoEstimator:
    def __init__(self):
        self.onset_detector = OnsetDetector()
        self.estimator = Estimator()
        
    def predict_bpm(self, file_path):
        """Predicts BPM in two stages: Onset detection, and estimation"""
        y, sr = librosa.load(file_path)
        onsets, time = self.onset_detector.detect_spectral_onsets(y, sr, gamma=100)
        onset_times = time[onsets]
        bpm = self.estimator.interval_based_estimate_bpm(onset_times)
        self.onset_detector.produce_click_track(onset_times)
        return bpm, onset_times
    
