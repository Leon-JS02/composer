import librosa
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.ndimage import filters

class OnsetDetector:
    def __init__(self) -> None:
        pass
    
    def plot_peaks(self, novelty, time, onsets):
       plt.figure()
       plt.plot(time, novelty)
       plt.plot(time[onsets], novelty[onsets], 'r.', markersize=10)
       plt.xlabel('Time (s)')
       plt.ylabel('Frequency Change')
       plt.title('Spectral Novelty Function with Onsets')
       plt.show()

    def peak_pick(self, x, median_len=16, offset_rel=0.05, sigma=4.0):
        """Uses Gaussian smoothing and adaptive local thresholding 
        to find peaks in a signal"""
        offset = x.mean() * offset_rel
        x = filters.gaussian_filter1d(x, sigma=sigma)
        threshold_local = filters.median_filter(x, size=median_len) + offset
        peaks = []
        for i in range(1, x.shape[0] - 1):
            if x[i - 1] < x[i] and x[i] > x[i + 1]:
                if x[i] > threshold_local[i]:
                    peaks.append(i)
        peaks = np.asarray(peaks)
        return peaks


    def detect_spectral_onsets(self, sig, sr, gamma=100):
        """Detects onsets as peaks in a spectral novelty function, logarithmically compressed by gamma"""
        sig = np.asarray(sig)
        window_size = 1024
        hop_length = 512
        X = librosa.stft(sig, n_fft=1024, hop_length=hop_length, 
                         win_length=window_size, window='hann')
        # Logarithmically compresses the spectrogram by scale of gamma
        X = np.log(1 + gamma * np.abs(X))
        # Take the discrete difference and sum for a novelty function
        X = np.diff(X, n = 1)
        # Half wave rectification
        X[X < 0] = 0
        novelty_fun = np.sum(X, axis = 0)
        novelty_fun = np.concatenate((novelty_fun, np.array([0])))
        time = np.arange(0, len(novelty_fun) * hop_length / sr, hop_length / sr)
        onsets = self.peak_pick(novelty_fun)
        #self.plot_peaks(novelty_fun, time, onsets)
        return onsets, time

    def produce_click_track(self, onsets, sr=22050, freq=800):
        """Takes a list of seconds in which onsets occur, creates a click track"""
        onset_samples = [round(x * sr) for x in onsets]
        click_duration = int(0.1 * sr)  
        click_track = np.zeros(onset_samples[-1] + click_duration)
        tone = np.sin(2 * np.pi * freq * np.arange(click_duration) / sr)
        for onset_sample in onset_samples:
            if onset_sample + click_duration < len(click_track):
                click_track[onset_sample:onset_sample + click_duration] = tone
        
        sf.write("test.wav", click_track, sr)
