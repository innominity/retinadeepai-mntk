from retinadeepai.models import RetinaImageCropTypeOCT
from .results import DetectionResult

class DetectionMethod:
    
    def __init__(self) -> None:
        self.encoder = self.get_encoder()

    def get_encoder(self) -> dict:
        """Получение encoder для модели детекции

        Returns:
            dict: Словарь с метками, которые может прогнозировать модель (key - код прогноза модели RetinaImageCropTypeOCT.model_code, value - RetinaImageCropTypeOCT.name) 
        """
        return {
            0: 'retina_horizontal',
        }
    
    def _get_model(self):
        pass

    def _predict(self):
        pass
    
    def compute_prediction(self, image) -> list[DetectionResult]:
        return []