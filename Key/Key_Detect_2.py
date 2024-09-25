import json

import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import numpy as np
import scipy.linalg
import scipy.stats



class KeyPredictor:
    """Class to predict the key of a given audio file."""

    def __init__(self, filepath):
        self.major_profile = np.array(
            [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        self.minor_profile = np.array(
            [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
        self.y, self.sr = librosa.load(filepath)

    def butter_lowpass_filter(self, cutoff, data, order):
        """Applies a Butterworth lowpass filter to a signal"""
        nyquist = self.sr * 0.5
        cutoff_normalised = cutoff / nyquist
        b, a = butter(order, cutoff_normalised, btype='low', analog=False)
        return filtfilt(b, a, data)

    def get_chromagram(self):
        """Returns a signal's chromagraph."""
        return librosa.feature.chroma_stft(y=self.y, sr=self.sr)

    def visualise_pitch_class_distribution(self, pitch_class_distribution, pitch_classes):
        """Uses matplotlib to visualise an audio file's PCD."""
        plt.bar(pitch_classes, pitch_class_distribution)
        plt.title('Pitch Class Distribution')
        plt.xlabel('Pitch Class')
        plt.ylabel('Energy')
        plt.show()

    def predict_key(self, pitch_class_distribution):
        """Performs the key prediction of a pitch class distribution."""
        zscored = scipy.stats.zscore(pitch_class_distribution)
        majors = scipy.linalg.circulant(
            scipy.stats.zscore(self.major_profile)).T
        minors = scipy.linalg.circulant(
            scipy.stats.zscore(self.minor_profile)).T
        # Cross product of z-scores = correlation function
        major_similarity = majors.dot(zscored)
        minor_similarity = minors.dot(zscored)
        # Returns the most likely major and minor key, and their respective similarities
        return np.argmax(major_similarity), np.max(major_similarity), np.argmax(minor_similarity), np.max(minor_similarity)

    def run_prediction(self):
        """Runs a key prediction of the assigned signal."""
        self.y = self.butter_lowpass_filter(1400, self.y, 4)
        chromagram_filtered = self.get_chromagram()
        pitch_class_distribution = np.sum(chromagram_filtered, axis=1)
        # Normalises the distribution
        pitch_class_distribution /= np.max(pitch_class_distribution)
        pitch_classes = ['C', 'C#', 'D', 'D#', 'E',
                         'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        # self.plot_pitch_class_distribution(pitch_class_distribution, pitch_classes)
        major_key, major_similarity, minor_key, minor_similarity = self.predict_key(
            pitch_class_distribution)

        if major_similarity > minor_similarity:
            key = pitch_classes[major_key] + " Maj"
            similarity = major_similarity
        else:
            key = pitch_classes[minor_key] + " Min"
            similarity = minor_similarity

        # Returns the key (tonality and mode) and its similarity a 'confidence' rating as a percentage
        confidence = (similarity/12)*100
        return key, confidence


def run_test(title, gt_key):
    root = ""
    predictor = KeyPredictor(root + title)
    key, _ = predictor.run_prediction()
    return key == gt_key


def run_tests(test_data):
    correct = 0
    wrong = []
    for title, key in test_data.items():
        if run_test(title, key):
            correct += 1
        else:
            wrong.append(title)
    return (correct/len(test_data.items())) * 100, wrong


def test_all():
    root = ""
    with open(root + "test_data.json", "r") as f:
        test_data = json.load(f)

    accuracy, wrong = run_tests(test_data)
    wrong = ', '.join(wrong)
    print("First match accuracy testing.")
    print(f'Accuracy: {round(accuracy)}%\nIncorrect classifications: {wrong}')
