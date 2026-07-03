import cv2
import numpy as np
from ..vision import filters

class ImageEngine:
    def __init__(self):
        self.original_image = None
        self.processed_image = None

    def load_image(self, path):
        self.original_image = cv2.imread(path)
        if self.original_image is None:
            return None
        return self.original_image.shape

    def process(self, brightness=0, contrast=0, threshold=0, gamma=1.0, 
                grayscale=False, blur_type=None, blur_strength=3):
        if self.original_image is None:
            return None
            
        # 1. Ajustes Básicos (Brillo/Contraste)
        img = filters.apply_brightness_contrast(self.original_image, brightness, contrast)
        
        # 2. Gamma
        if gamma != 1.0:
            invGamma = 1.0 / gamma
            table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            img = cv2.LUT(img, table)
        
        # 3. Conversión a Grayscale (si se solicita o si se va a binarizar)
        if grayscale or threshold > 0:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 4. Aplicar Blur (Pre-procesamiento)
        if blur_type == "gaussian":
            k = blur_strength if blur_strength % 2 != 0 else blur_strength + 1
            img = cv2.GaussianBlur(img, (k, k), 0)
        elif blur_type == "median":
            k = blur_strength if blur_strength % 2 != 0 else blur_strength + 1
            img = cv2.medianBlur(img, k)

        # 5. Binarización
        if threshold > 0:
            # Si no era gris ya, lo convertimos
            if len(img.shape) == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
            
        # 6. Asegurar salida BGR para el motor de renderizado de FreeCAD
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            
        self.processed_image = img
        return self.processed_image
