"""Key Analyst module. Wrapper for the main program."""
from Key.key_predictor import KeyPredictor


class KeyAnalyst:
    """Key Analyst class."""

    def predict_key(self, file_path: str) -> tuple[str, int]:
        """Predicts the key of an audio file. 
        Returning its key and a confidence score."""
        predictor = KeyPredictor(file_path)
        key, confidence = predictor.run_prediction()
        confidence = round(confidence)
        return key, confidence
