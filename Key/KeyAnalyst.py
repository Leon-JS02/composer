from Key.Key_Detect_2 import KeyPredictor

class KeyAnalyst:
    def predict_key(self, file_path):
        predictor = KeyPredictor(file_path)
        key, confidence = predictor.run_prediction()
        confidence = round(confidence)
        return key, confidence