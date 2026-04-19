import cv2
import numpy as np
from tensorflow.keras.models import load_model # type: ignore
from spellchecker import SpellChecker

class RecognitionEngine:
    def __init__(self, alpha_path, num_path, draw_path, class_path):
        self.spell = SpellChecker()
        self.alpha_labels = {i: chr(65+i) for i in range(26)}
        self.num_labels = {i: str(i) for i in range(10)}
        
        try:
            self.alpha_model = load_model(alpha_path)
            self.num_model = load_model(num_path)
            self.draw_model = load_model(draw_path)
            with open(class_path, 'r') as f:
                self.draw_labels = [line.strip() for line in f.readlines()]
            print("All AI Models Loaded")
        except Exception as e:
            print(f"Model Error: {e}")

    def predict_drawing(self, canvas_th):
        cnts, _ = cv2.findContours(canvas_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts: return "NONE"
        x, y, w, h = cv2.boundingRect(np.concatenate(cnts))
        roi = cv2.dilate(canvas_th[y:y+h, x:x+w], np.ones((5,5), np.uint8), iterations=1)
        return self._preprocess_and_predict(roi, self.draw_model, self.draw_labels, padding=80)

    def predict_text(self, canvas_th, mode="ALPHA"):
        cnts, _ = cv2.findContours(canvas_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts: return "", ""
        
        boxes = sorted([cv2.boundingRect(c) for c in cnts if cv2.contourArea(c) > 50], key=lambda b: b[0])
        model = self.alpha_model if mode == "ALPHA" else self.num_model
        labels = self.alpha_labels if mode == "ALPHA" else self.num_labels
        
        raw_word = ""
        for x, y, w, h in boxes:
            roi = canvas_th[y:y+h, x:x+w]
            raw_word += str(self._preprocess_and_predict(roi, model, labels))
        
        corrected = ""
        if mode == "ALPHA" and len(raw_word) > 1:
            corrected = self.spell.correction(raw_word.lower()) or raw_word
            
        return raw_word, corrected.upper()

    def _preprocess_and_predict(self, roi, model, labels, padding=40):
        h, w = roi.shape
        size = max(w, h) + padding
        padded = np.zeros((size, size), dtype=np.uint8)
        padded[(size-h)//2:(size-h)//2+h, (size-w)//2:(size-w)//2+w] = roi
        final = cv2.resize(padded, (28,28)).astype("float32") / 255.0
        pred = model.predict(final.reshape(1, 28, 28, 1), verbose=0)
        
        if isinstance(labels, list): return labels[np.argmax(pred)]
        return labels[np.argmax(pred)]