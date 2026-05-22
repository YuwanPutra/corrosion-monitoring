import numpy as np
from PIL import Image

ISO_RATES = {
    "C1": 0.65, "C2": 13, "C3": 37, 
    "C4": 65, "C5": 140, "CX": 450
}

class CorrosionAI:
    def __init__(self, model_path=None):
        self.model = None
        if model_path:
            # Real implementation would be: self.model = tf.keras.models.load_model(model_path)
            pass

    def analyze_image(self, image_path):
        """
        Processes an image and returns a corrosion percentage.
        For this prototype, returns a simulated value.
        """
        try:
            img = Image.open(image_path).convert('RGB')
            # In a real model, we would resize and normalize:
            # img = img.resize((224, 224))
            # img_array = np.array(img) / 255.0
            # prediction = self.model.predict(np.expand_dims(img_array, axis=0))
            
            # Simulation: Return 45.0 for the demo
            return 45.0
        except Exception as e:
            print(f"Error processing image: {e}")
            return 0.0

def calculate_life(level, percentage, thickness=85):
    rate = ISO_RATES.get(level, 37)
    base_life = thickness / rate
    # Percentage represents how much of the functional life is consumed/damaged
    return base_life * (1 - (percentage / 100))

def get_status_action(percentage):
    if percentage <= 40:
        return "Aman", "text-success", "Inspeksi Rutin Sesuai Periode"
    elif percentage <= 80:
        return "Waspada", "text-warning", "Intensitas Inspeksi Ditingkatkan"
    else:
        return "Kritis", "text-danger", "Perbaiki Segera"
